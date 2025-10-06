# app/services/qa_service.py
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from flask import current_app
import re
import string

# Global variables for lazy loading
_qa_model = None
_qa_tokenizer = None
_qa_pipeline = None

def _load_qa_model():
    """Load the DistilBERT Q&A model from Hugging Face"""
    global _qa_model, _qa_tokenizer, _qa_pipeline
    
    if _qa_model is None or _qa_tokenizer is None:
        try:
            # Get model name from config (with fallback for testing outside Flask context)
            model_name = 'distilbert-base-cased-distilled-squad'  # Default
            
            try:
                from flask import current_app
                model_name = getattr(current_app.config, 'QA_MODEL', model_name)
                current_app.logger.info(f"Loading Q&A model: {model_name}...")
            except RuntimeError:
                # Working outside of application context (e.g., testing)
                print(f"Loading Q&A model: {model_name}...")
            
            _qa_tokenizer = AutoTokenizer.from_pretrained(model_name)
            _qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            
            # Create a pipeline for easier use
            _qa_pipeline = pipeline(
                "question-answering",
                model=_qa_model,
                tokenizer=_qa_tokenizer,
                return_all_scores=True,
                device=-1  # Use CPU
            )
            
            # Set model to evaluation mode
            _qa_model.eval()
            
            try:
                from flask import current_app
                current_app.logger.info("Q&A model loaded successfully!")
            except RuntimeError:
                print("Q&A model loaded successfully!")
            
        except Exception as e:
            try:
                from flask import current_app
                current_app.logger.error(f"Error loading Q&A model: {str(e)}")
            except RuntimeError:
                print(f"Error loading Q&A model: {str(e)}")
            raise e
    
    return _qa_model, _qa_tokenizer, _qa_pipeline

def preprocess_text(text):
    """Enhanced text preprocessing for better Q&A performance"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Fix common transcription issues
    text = re.sub(r'\b(\w+)\1+\b', r'\1', text)  # Remove repeated words
    text = re.sub(r'[^\w\s.,!?;:()-]', '', text)  # Remove special chars
    
    # Capitalize sentences properly
    sentences = text.split('.')
    processed_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            processed_sentences.append(sentence)
    
    return '. '.join(processed_sentences)

def preprocess_question(question):
    """Enhanced question preprocessing"""
    if not question:
        return ""
    
    question = question.strip()
    
    # Ensure question ends with question mark
    if not question.endswith('?'):
        question += '?'
    
    # Capitalize first letter
    if question:
        question = question[0].upper() + question[1:]
    
    return question

def smart_chunking(text, question, max_length=None, overlap=None):
    """Intelligent chunking that considers question context"""
    # Use config values if not provided, with fallbacks for outside Flask context
    if max_length is None:
        try:
            from flask import current_app
            max_length = getattr(current_app.config, 'QA_CHUNK_SIZE', 350)
        except RuntimeError:
            max_length = 350
    
    if overlap is None:
        try:
            from flask import current_app
            overlap = getattr(current_app.config, 'QA_CHUNK_OVERLAP', 75)
        except RuntimeError:
            overlap = 75
    
    words = text.split()
    
    if len(words) <= max_length:
        return [text]
    
    # Extract keywords from question for better chunking
    question_words = set(question.lower().split()) - set(['what', 'when', 'where', 'who', 'why', 'how', 'is', 'are', 'was', 'were', 'the', 'a', 'an'])
    
    chunks = []
    start = 0
    
    while start < len(words):
        end = min(start + max_length, len(words))
        chunk_words = words[start:end]
        
        # Try to end chunk at sentence boundary
        chunk_text = ' '.join(chunk_words)
        if end < len(words):  # Not the last chunk
            last_period = chunk_text.rfind('.')
            last_exclamation = chunk_text.rfind('!')
            last_question = chunk_text.rfind('?')
            
            sentence_end = max(last_period, last_exclamation, last_question)
            if sentence_end > len(chunk_text) * 0.7:  # If sentence boundary is in last 30%
                chunk_text = chunk_text[:sentence_end + 1]
                # Recalculate end position
                end = start + len(chunk_text.split())
        
        chunks.append(chunk_text)
        
        if end >= len(words):
            break
        
        start = end - overlap
    
    return chunks

def calculate_answer_quality(answer, question, context):
    """Calculate answer quality based on multiple factors"""
    if not answer or len(answer.strip()) < 3:
        return 0.0
    
    score = 0.0
    
    # Length penalty for very short answers
    if len(answer) < 10:
        score -= 0.2
    
    # Bonus for answers that contain question keywords
    question_words = set(re.findall(r'\w+', question.lower()))
    answer_words = set(re.findall(r'\w+', answer.lower()))
    keyword_overlap = len(question_words.intersection(answer_words))
    if keyword_overlap > 0:
        score += 0.1 * keyword_overlap
    
    # Penalty for generic answers
    generic_phrases = ['i don\'t know', 'not sure', 'unclear', 'maybe', 'possibly']
    if any(phrase in answer.lower() for phrase in generic_phrases):
        score -= 0.3
    
    # Bonus for complete sentences
    if answer.endswith('.') or answer.endswith('!'):
        score += 0.1
    
    return max(0.0, min(1.0, score))

def answer_question(transcript, question, max_answer_length=None):
    """
    Enhanced Q&A function with better answer selection and confidence scoring
    
    Args:
        transcript (str): The text to search for answers
        question (str): The question to answer
        max_answer_length (int): Maximum length of the answer
    
    Returns:
        dict: Contains answer, confidence score, and metadata
    """
    try:
        # Get config values with fallbacks for outside Flask context
        if max_answer_length is None:
            try:
                from flask import current_app
                max_answer_length = getattr(current_app.config, 'QA_MAX_ANSWER_LENGTH', 200)
            except RuntimeError:
                max_answer_length = 200
        
        try:
            from flask import current_app
            confidence_threshold = getattr(current_app.config, 'QA_CONFIDENCE_THRESHOLD', 0.05)
        except RuntimeError:
            confidence_threshold = 0.05
        
        # Load the model and pipeline
        model, tokenizer, pipeline = _load_qa_model()
        
        # Preprocess inputs
        transcript = preprocess_text(transcript)
        question = preprocess_question(question)
        
        if not transcript or not question:
            return {
                'answer': "I couldn't process your question. Please make sure both the transcript and question are valid.",
                'confidence': 0.0,
                'source_text': ""
            }
        
        # Log processing info (with context safety)
        try:
            from flask import current_app
            current_app.logger.info(f"Processing question: {question}")
        except RuntimeError:
            print(f"Processing question: {question}")
        
        # Use smart chunking for better context
        chunks = smart_chunking(transcript, question)
        
        try:
            from flask import current_app
            current_app.logger.info(f"Created {len(chunks)} chunks for processing")
        except RuntimeError:
            print(f"Created {len(chunks)} chunks for processing")
        
        all_answers = []
        
        for i, chunk in enumerate(chunks):
            try:
                # Use the pipeline for better results
                results = pipeline(
                    question=question,
                    context=chunk,
                    max_answer_len=max_answer_length,
                    top_k=3,  # Get top 3 answers
                    doc_stride=128,
                    max_question_len=64,
                    max_seq_len=512
                )
                
                # Process results from pipeline
                for result in results:
                    answer = result['answer'].strip()
                    confidence = result['score']
                    
                    if len(answer) >= 3:  # Minimum answer length
                        # Calculate additional quality score
                        quality_bonus = calculate_answer_quality(answer, question, chunk)
                        adjusted_confidence = confidence + quality_bonus
                        
                        all_answers.append({
                            'answer': answer,
                            'confidence': adjusted_confidence,
                            'original_confidence': confidence,
                            'source_chunk': chunk,
                            'chunk_index': i
                        })
                
            except Exception as e:
                try:
                    from flask import current_app
                    current_app.logger.warning(f"Error processing chunk {i}: {str(e)}")
                except RuntimeError:
                    print(f"Warning: Error processing chunk {i}: {str(e)}")
                continue
        
        if not all_answers:
            return {
                'answer': "I couldn't find an answer to your question in the transcript. Try asking about specific topics mentioned in the conversation.",
                'confidence': 0.0,
                'source_text': ""
            }
        
        # Sort answers by adjusted confidence
        all_answers.sort(key=lambda x: x['confidence'], reverse=True)
        best_answer = all_answers[0]
        
        # Additional validation using config threshold
        if best_answer['original_confidence'] < confidence_threshold:
            return {
                'answer': "I found some potential answers but I'm not confident about them. Could you try rephrasing your question more specifically?",
                'confidence': 0.0,
                'source_text': ""
            }
        
        # Post-process the answer
        final_answer = post_process_answer(best_answer['answer'], question)
        
        # Prepare source text
        source_start = max(0, best_answer['source_chunk'].find(final_answer) - 50)
        source_end = min(len(best_answer['source_chunk']), 
                        best_answer['source_chunk'].find(final_answer) + len(final_answer) + 50)
        source_text = best_answer['source_chunk'][source_start:source_end]
        
        try:
            from flask import current_app
            current_app.logger.info(f"Best answer found with confidence: {best_answer['original_confidence']:.3f}")
        except RuntimeError:
            print(f"Best answer found with confidence: {best_answer['original_confidence']:.3f}")
        
        return {
            'answer': final_answer,
            'confidence': min(best_answer['original_confidence'], 0.95),  # Cap confidence at 95%
            'source_text': source_text.strip()
        }
        
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.error(f"Error in Q&A processing: {str(e)}")
        except RuntimeError:
            print(f"Error in Q&A processing: {str(e)}")
        return {
            'answer': f"Sorry, I encountered an error while processing your question. Please try again.",
            'confidence': 0.0,
            'source_text': ""
        }

def post_process_answer(answer, question):
    """Post-process the answer for better readability"""
    if not answer:
        return answer
    
    # Remove incomplete sentences at the end
    sentences = answer.split('.')
    if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
        answer = '.'.join(sentences[:-1]) + '.'
    
    # Ensure proper capitalization
    if answer and not answer[0].isupper():
        answer = answer[0].upper() + answer[1:]
    
    # Add period if missing
    if answer and not answer.endswith(('.', '!', '?')):
        answer += '.'
    
    return answer.strip()

def generate_suggested_questions(transcript, max_questions=5):
    """
    Generate simple suggested questions for any transcript
    
    Args:
        transcript (str): The transcript text
        max_questions (int): Maximum number of questions to generate
    
    Returns:
        list: List of suggested questions
    """
    try:
        # Always return these two specific questions
        return [
            "What is the main topic discussed here?",
            "What are the important details discussed here?"
        ]
        
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.error(f"Error generating suggested questions: {str(e)}")
        except RuntimeError:
            print(f"Error generating suggested questions: {str(e)}")
        return [
            "What is the main topic discussed here?",
            "What are the important details discussed here?"
        ]


class QAService:
    """
    Q&A Service class that wraps all Q&A functionality
    """
    
    def __init__(self):
        """Initialize the QA service"""
        # The model will be loaded lazily when first needed
        pass
    
    def answer_question(self, question, transcript, max_answer_length=None):
        """
        Answer a question based on the transcript
        
        Args:
            question (str): The question to answer
            transcript (str): The transcript text to search for answers
            max_answer_length (int): Maximum length of the answer
            
        Returns:
            dict: Dictionary containing answer, confidence, and other metadata
        """
        return answer_question(transcript, question, max_answer_length)
    
    def generate_suggested_questions(self, transcript, max_questions=5):
        """
        Generate suggested questions based on transcript content
        
        Args:
            transcript (str): The transcript text
            max_questions (int): Maximum number of questions to generate
            
        Returns:
            list: List of suggested questions
        """
        return generate_suggested_questions(transcript, max_questions)
    
    def preprocess_text(self, text):
        """
        Preprocess text for better Q&A performance
        
        Args:
            text (str): Text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        return preprocess_text(text)
    
    def preprocess_question(self, question):
        """
        Preprocess question for better matching
        
        Args:
            question (str): Question to preprocess
            
        Returns:
            str: Preprocessed question
        """
        return preprocess_question(question)
# Q&A Feature Documentation

## 🤖 AI-Powered Question Answering

The Speech Recognition app now includes an intelligent Q&A feature that allows you to ask questions about your transcribed content using advanced AI.

### ✨ Features

- **Smart Question Answering**: Uses DistilBERT model trained on SQuAD dataset
- **Confidence Scoring**: Shows how confident the AI is about each answer
- **Suggested Questions**: Automatically generates relevant questions based on content
- **Q&A History**: Saves all your questions and answers for future reference
- **Source Attribution**: Shows which part of the transcript the answer came from

### 🚀 How to Use

1. **Transcribe Audio**: Upload and transcribe your audio file as usual
2. **Access Q&A**: Click the "Ask Questions" button on the result page
3. **Ask Questions**: Type your question or use suggested questions
4. **Get Answers**: Receive AI-generated answers with confidence scores
5. **Review History**: View all previous Q&A sessions

### 💡 Tips for Better Results

- **Be Specific**: Ask clear, specific questions about the content
- **Use Keywords**: Include important terms from the transcript
- **Check Confidence**: Higher confidence scores indicate more reliable answers
- **Try Variations**: Rephrase questions if the first attempt doesn't work well

### 🎯 Question Examples

**Good Questions:**
- "What was the main topic discussed?"
- "When did this event happen?"
- "Who was mentioned in the conversation?"
- "What was the conclusion reached?"

**Less Effective:**
- "Tell me everything"
- "What do you think?"
- Very general or abstract questions

### 🛠️ Technical Details

- **Model**: DistilBERT-base-cased-distilled-squad
- **Context Limit**: Handles long transcripts by chunking
- **Response Time**: First query may take longer (model loading)
- **Storage**: Model requires ~250MB disk space

### 🔧 Setup Instructions

1. Run the setup script:
   ```bash
   python setup_qa_feature.py
   ```

2. Or manually install dependencies:
   ```bash
   pip install sentence-transformers==2.2.2
   python migrations/add_qa_sessions.py
   ```

### 🔍 Troubleshooting

**Q&A giving poor or irrelevant answers:**

1. **Check transcript quality:**
   ```python
   # Run debug script to analyze your specific case
   python debug_qa.py
   ```

2. **Question format matters:**
   - ❌ "Tell me about everything"
   - ✅ "What was the sales increase percentage?"
   - ❌ "What do you think about..."  
   - ✅ "Who mentioned the budget?"

3. **Use specific keywords from transcript:**
   - Include exact names, numbers, or terms mentioned
   - Ask about concrete facts rather than opinions

4. **Configuration tuning:**
   Environment variables you can set:
   ```bash
   # Lower threshold for more lenient answers (default: 0.05)
   QA_CONFIDENCE_THRESHOLD=0.02
   
   # Adjust chunk size for better context (default: 350)
   QA_CHUNK_SIZE=300
   
   # Increase overlap for better continuity (default: 75)
   QA_CHUNK_OVERLAP=100
   
   # Try different model (optional)
   QA_MODEL=deepset/roberta-base-squad2
   ```

**Model Loading Issues:**
- Ensure stable internet connection for first download
- Check available disk space (~250MB required)
- Clear browser cache and restart application

**Performance Issues:**
- First query loads the model (one-time delay of 30-60 seconds)
- Subsequent queries should be much faster (2-5 seconds)
- For very long transcripts, consider breaking into smaller segments

**Testing and Debugging:**
```bash
# Run comprehensive test
python test_qa_feature.py

# Interactive debugging session
python debug_qa.py

# Check model performance
python -c "from app.services.qa_service import answer_question; print(answer_question('Test text', 'Test question?'))"
```

### 🔐 Privacy & Security

- All processing happens locally (after model download)
- Q&A sessions are stored in your private database
- No external API calls required for inference
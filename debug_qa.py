# debug_qa.py
"""
Debugging script to diagnose Q&A performance issues
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def initialize_flask_context():
    """Initialize Flask application context for testing"""
    try:
        from app import create_app
        app = create_app()
        return app.app_context()
    except Exception as e:
        print(f"Warning: Could not initialize Flask context: {e}")
        print("Running in standalone mode...")
        return None

def debug_qa_performance():
    """Debug Q&A performance with detailed analysis"""
    
    # Initialize Flask context if possible
    app_context = initialize_flask_context()
    
    try:
        if app_context:
            app_context.push()
        
        from app.services.qa_service import answer_question, preprocess_text, smart_chunking
        
        print("🔍 Q&A Performance Debug Tool")
        print("=" * 50)
        
        # Get user input
        print("\nPlease paste your transcript:")
        transcript = input().strip()
        if not transcript:
            transcript = "Sample transcript for testing. John said hello to Mary at 3 PM yesterday in the office."
        
        print("\nPlease enter your question:")
        question = input().strip()
        if not question:
            question = "Who said hello?"
        
        print(f"\n📊 Debug Analysis:")
        print(f"Original transcript length: {len(transcript)} characters")
        print(f"Original question: '{question}'")
        
        # Test preprocessing
        processed_transcript = preprocess_text(transcript)
        print(f"\nAfter preprocessing:")
        print(f"Processed transcript length: {len(processed_transcript)} characters")
        print(f"Sample: {processed_transcript[:200]}{'...' if len(processed_transcript) > 200 else ''}")
        
        # Test chunking
        chunks = smart_chunking(processed_transcript, question)
        print(f"\nChunking analysis:")
        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            print(f"Chunk {i+1}: {chunk[:100]}{'...' if len(chunk) > 100 else ''}")
        
        # Test Q&A
        print(f"\n🤖 Running Q&A...")
        result = answer_question(transcript, question)
        
        print(f"\nResults:")
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']:.3f}")
        if result['source_text']:
            print(f"Source: {result['source_text']}")
        
        # Analysis and recommendations
        print(f"\n💡 Analysis:")
        if result['confidence'] < 0.1:
            print("❌ Very low confidence - the model couldn't find a good answer")
            print("Recommendations:")
            print("- Check if your question relates to content in the transcript")
            print("- Try rephrasing your question more specifically")
            print("- Ensure transcript quality is good")
        elif result['confidence'] < 0.3:
            print("⚠️ Low confidence - answer might not be reliable")
            print("Recommendations:")
            print("- Try asking more specific questions")
            print("- Break complex questions into simpler parts")
        elif result['confidence'] < 0.7:
            print("✅ Moderate confidence - answer is likely correct")
        else:
            print("🎉 High confidence - answer is very likely correct")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if app_context:
            app_context.pop()

def interactive_qa_session():
    """Interactive Q&A session for testing"""
    
    # Initialize Flask context if possible
    app_context = initialize_flask_context()
    
    try:
        if app_context:
            app_context.push()
        
        from app.services.qa_service import answer_question, generate_suggested_questions
        
        print("🎯 Interactive Q&A Testing Session")
        print("=" * 40)
        
        # Get transcript
        print("Please paste your transcript (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        transcript = "\n".join(lines)
        if not transcript.strip():
            print("No transcript provided. Using sample...")
            transcript = """
            Welcome to our team meeting. We discussed the project timeline today.
            Alice mentioned that the development phase will take 3 months.
            Bob suggested we hire 2 additional developers for the frontend work.
            The budget for this project is $100,000 and the deadline is December 31st.
            We agreed to meet again next Friday to review progress.
            """
        
        print(f"\n📄 Transcript loaded ({len(transcript)} characters)")
        
        # Generate suggested questions
        suggestions = generate_suggested_questions(transcript)
        print(f"\n💡 Suggested questions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        # Interactive Q&A loop
        print(f"\n🤖 Ask questions about the transcript (type 'quit' to exit):")
        while True:
            question = input("\nYour question: ").strip()
            if question.lower() in ['quit', 'exit', 'stop']:
                break
            
            if not question:
                continue
            
            result = answer_question(transcript, question)
            print(f"\n🤖 Answer: {result['answer']}")
            print(f"📊 Confidence: {result['confidence']:.2f}")
            
            if result['confidence'] < 0.2:
                print("💡 Try rephrasing your question or asking about specific details mentioned in the transcript.")
        
        print("👋 Thanks for testing!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if app_context:
            app_context.pop()

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Debug specific Q&A performance")
    print("2. Interactive Q&A session")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        debug_qa_performance()
    elif choice == "2":
        interactive_qa_session()
    else:
        print("Running debug analysis...")
        debug_qa_performance()
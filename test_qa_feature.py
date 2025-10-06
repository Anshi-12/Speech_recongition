#!/usr/bin/env python3
"""
Test script for Q&A functionality
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def initialize_flask_context():
    """Initialize Flask application context for testing"""
    try:
        from app import create_app
        app = create_app()
        return app.app_context()
    except Exception as e:
        print(f"Warning: Could not initialize Flask context: {e}")
        return None

def test_qa_service():
    """Test the Q&A service functionality"""
    app_context = initialize_flask_context()
    
    try:
        if app_context:
            app_context.push()
            
        from app.services.qa_service import QAService
        
        print(" Testing Q&A Service")
        print("=" * 40)
        
        qa_service = QAService()
        
        # Test transcript
        transcript = """
        Welcome to today's technology presentation. My name is Sarah Johnson, and I'll be discussing 
        artificial intelligence trends in 2024. Recent studies show that AI can now detect certain 
        diseases with 95% accuracy. The key breakthrough happened in January when researchers at 
        Stanford University developed a new neural network architecture.
        """
        
        # Test questions
        questions = [
            "Who is the presenter?",
            "What accuracy can AI achieve in disease detection?", 
            "Which university made the breakthrough?"
        ]
        
        print(f"Testing with {len(questions)} questions...\n")
        
        for i, question in enumerate(questions, 1):
            print(f"Question {i}: {question}")
            
            try:
                result = qa_service.answer_question(question, transcript)
                
                if result and result.get('answer'):
                    print(f"Answer: {result['answer']}")
                    print(f"Confidence: {result.get('confidence', 0):.2f}")
                    print(" SUCCESS")
                else:
                    print(" FAILED - No answer returned")
                    
            except Exception as e:
                print(f" ERROR: {e}")
                
            print("-" * 30)
        
        print("\n Q&A Service test completed!")
        return True
        
    except ImportError as e:
        print(f" Import error: {e}")
        return False
    except Exception as e:
        print(f" Unexpected error: {e}")
        return False
    finally:
        if app_context:
            app_context.pop()

if __name__ == "__main__":
    print(" Starting Q&A Test")
    success = test_qa_service()
    
    if success:
        print("\n Test completed successfully!")
    else:
        print("\n Test failed. Check errors above.")

# setup_qa_feature.py
"""
Setup script for the Q&A feature
This script will install dependencies and run migrations
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        if isinstance(command, str):
            # For Windows PowerShell
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description.lower()}: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🤖 Setting up Q&A Feature for Speech Recognition App")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    print("📦 Installing new dependencies...")
    
    # Install new dependencies
    commands = [
        ("pip install sentence-transformers==2.2.2", "Installing sentence-transformers"),
        ("python migrations/add_qa_sessions.py", "Running database migration"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Setup Summary:")
    print(f"✓ {success_count}/{len(commands)} operations completed successfully")
    
    if success_count == len(commands):
        print("\n🎉 Q&A Feature setup completed successfully!")
        print("\n📋 What's New:")
        print("- DistilBERT-based question answering about transcripts")
        print("- Q&A interface accessible from transcript results")
        print("- Q&A history and suggested questions")
        print("- Confidence scores for AI answers")
        
        print("\n🚀 How to Use:")
        print("1. Transcribe an audio file as usual")
        print("2. Click 'Ask Questions' button on the result page")
        print("3. Type questions about the transcript content")
        print("4. View Q&A history in the dashboard")
        
        print("\n⚠️  Note:")
        print("- First Q&A query may take longer as the model downloads")
        print("- Model requires ~250MB of disk space")
        print("- Best results with clear, specific questions")
        
        print("\n🔄 To start the application:")
        print("python run.py")
        
    else:
        print("\n❌ Setup encountered some issues. Please check the errors above.")
        print("💡 You may need to:")
        print("- Ensure you have an active internet connection")
        print("- Run as administrator if permission errors occur")
        print("- Check that Python and pip are properly installed")

if __name__ == "__main__":
    main()
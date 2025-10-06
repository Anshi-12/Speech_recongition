# migrations/add_qa_sessions.py
"""
Database migration script to add qa_sessions table
Run this script after installing the new dependencies
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Add the parent directory to Python path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.qa_session import QASession

def migrate_database():
    """Create the qa_sessions table"""
    app = create_app()
    
    with app.app_context():
        print("Creating qa_sessions table...")
        
        # Create the table
        db.create_all()
        
        print("qa_sessions table created successfully!")
        print("Migration completed.")

if __name__ == '__main__':
    migrate_database()
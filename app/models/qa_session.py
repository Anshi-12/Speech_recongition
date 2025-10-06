# app/models/qa_session.py
from datetime import datetime
from app import db


class QASession(db.Model):
    """Q&A Session model for storing questions and answers about transcripts"""
    __tablename__ = 'qa_sessions'

    id = db.Column(db.Integer, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)  # Store model confidence
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recording = db.relationship('Recording', backref='qa_sessions')
    user = db.relationship('User', backref='qa_sessions')

    def __init__(self, recording_id, user_id, question, answer, confidence_score=None):
        self.recording_id = recording_id
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.confidence_score = confidence_score

    def to_dict(self):
        """Convert Q&A session to dictionary."""
        return {
            'id': self.id,
            'recording_id': self.recording_id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<QASession {self.id}: {self.question[:50]}...>'
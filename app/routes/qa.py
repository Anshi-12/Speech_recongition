# app/routes/qa.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.recording import Recording
from app.models.qa_session import QASession
from app.services.qa_service import answer_question, generate_suggested_questions
from app import db

qa_bp = Blueprint('qa', __name__, url_prefix='/qa')

@qa_bp.route('/recording/<int:recording_id>')
@login_required
def qa_interface(recording_id):
    """Display Q&A interface for a specific recording"""
    recording = Recording.query.get_or_404(recording_id)
    
    # Ensure the user can only access their own recordings
    if recording.user_id != current_user.id:
        flash('You do not have permission to access this recording', 'danger')
        return redirect(url_for('main.history'))
    
    # Get previous Q&A sessions for this recording
    qa_sessions = QASession.query.filter_by(
        recording_id=recording_id,
        user_id=current_user.id
    ).order_by(QASession.created_at.desc()).all()
    
    # Generate suggested questions
    suggested_questions = generate_suggested_questions(recording.transcription or recording.text)
    
    return render_template('qa/interface.html',
                         recording=recording,
                         qa_sessions=qa_sessions,
                         suggested_questions=suggested_questions)

@qa_bp.route('/ask', methods=['POST'])
@login_required
def ask_question():
    """Process a question and return an answer"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        recording_id = data.get('recording_id')
        question = data.get('question', '').strip()
        
        if not recording_id or not question:
            return jsonify({'error': 'Recording ID and question are required'}), 400
        
        # Get the recording
        recording = Recording.query.get_or_404(recording_id)
        
        # Ensure the user can only access their own recordings
        if recording.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403
        
        # Get the transcript
        transcript = recording.transcription or recording.text
        if not transcript:
            return jsonify({'error': 'No transcript available for this recording'}), 400
        
        # Process the question
        result = answer_question(transcript, question)
        
        # Save the Q&A session to database
        qa_session = QASession(
            recording_id=recording_id,
            user_id=current_user.id,
            question=question,
            answer=result['answer'],
            confidence_score=result['confidence']
        )
        
        db.session.add(qa_session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'confidence': result['confidence'],
            'source_text': result['source_text'],
            'qa_session_id': qa_session.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

@qa_bp.route('/history/<int:recording_id>')
@login_required
def qa_history(recording_id):
    """Get Q&A history for a recording"""
    recording = Recording.query.get_or_404(recording_id)
    
    # Ensure the user can only access their own recordings
    if recording.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    qa_sessions = QASession.query.filter_by(
        recording_id=recording_id,
        user_id=current_user.id
    ).order_by(QASession.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'qa_sessions': [session.to_dict() for session in qa_sessions]
    })

@qa_bp.route('/delete/<int:qa_session_id>', methods=['DELETE'])
@login_required
def delete_qa_session(qa_session_id):
    """Delete a Q&A session"""
    qa_session = QASession.query.get_or_404(qa_session_id)
    
    # Ensure the user can only delete their own Q&A sessions
    if qa_session.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    try:
        db.session.delete(qa_session)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Q&A session deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting Q&A session: {str(e)}'}), 500

@qa_bp.route('/suggestions/<int:recording_id>')
@login_required
def get_suggestions(recording_id):
    """Get suggested questions for a recording"""
    recording = Recording.query.get_or_404(recording_id)
    
    # Ensure the user can only access their own recordings
    if recording.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    transcript = recording.transcription or recording.text
    if not transcript:
        return jsonify({'error': 'No transcript available'}), 400
    
    suggested_questions = generate_suggested_questions(transcript)
    
    return jsonify({
        'success': True,
        'suggestions': suggested_questions
    })
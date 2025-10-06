# app/config.py
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}  # Added from new implementation

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True

    # Flask-Login settings
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    
    # Whisper model settings (from new implementation)
    WAV2VEC2_MODEL = os.environ.get('WAV2VEC2_MODEL') or 'facebook/wav2vec2-large-960h-lv60-self'
    
    # Q&A model settings
    QA_MODEL = os.environ.get('QA_MODEL') or 'distilbert-base-cased-distilled-squad'
    QA_CONFIDENCE_THRESHOLD = float(os.environ.get('QA_CONFIDENCE_THRESHOLD', '0.05'))
    QA_MAX_ANSWER_LENGTH = int(os.environ.get('QA_MAX_ANSWER_LENGTH', '200'))
    QA_CHUNK_SIZE = int(os.environ.get('QA_CHUNK_SIZE', '350'))
    QA_CHUNK_OVERLAP = int(os.environ.get('QA_CHUNK_OVERLAP', '75'))
    
    @staticmethod
    def init_app(app):
        """Initialize application"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.dirname(basedir), 'dev.db')
    LOG_LEVEL = 'DEBUG'  # Added from new implementation


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.dirname(basedir), 'test.db')
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'test_uploads')


class ProductionConfig(Config):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.dirname(basedir), 'app.db')
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
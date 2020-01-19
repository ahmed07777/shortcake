import os
from app import create_app
from config import config

app = create_app(os.getenv('FLASK_CONFIG') or config['default'])

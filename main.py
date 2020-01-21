import os
from app import create_app
from app.db import db
from app.models import ShortURL
from config import config

app = create_app(os.getenv('FLASK_CONFIG') or config['default'])
with app.app_context():
    db.create_all()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'ShortURL': ShortURL
    }

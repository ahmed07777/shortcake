'''This module contains the database object instantiation only.'''

from flask_sqlalchemy import SQLAlchemy

# TODO does this have to be in its own file?
db = SQLAlchemy()

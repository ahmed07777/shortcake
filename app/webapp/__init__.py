'''The blueprint for the web interface.

Includes all routes used by the web interface, as well as associated
html templates and static files.
'''

from flask import Blueprint
from . import routes


bp = Blueprint('webapp', __name__)
routes.register(bp)

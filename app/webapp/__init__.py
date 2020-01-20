from flask import Blueprint
from . import routes


bp = Blueprint('webapp', __name__)
routes.register(bp)

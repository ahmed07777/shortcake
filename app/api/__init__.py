'''The blueprint for the REST API.

Contains all routes related to the API endpoints.
'''

from flask import Blueprint
from . import routes

bp = Blueprint('api', __name__)
routes.register(bp)

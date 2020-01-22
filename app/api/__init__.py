from flask import Blueprint
from . import routes

bp = Blueprint('api', __name__)
routes.register(bp)

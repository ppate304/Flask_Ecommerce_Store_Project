from flask import Blueprint 

bp = Blueprint('auth', __name__, url_prefix='')

from .import routes

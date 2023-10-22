# This is the authentication blueprint
from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
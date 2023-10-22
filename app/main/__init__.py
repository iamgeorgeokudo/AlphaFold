from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors  # this is a relative import form the current package

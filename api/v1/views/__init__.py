#!/usr/bin/python3
""" Init """
from flask import Blueprint


app_views = Blueprint('test', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *

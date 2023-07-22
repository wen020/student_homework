from flask import Blueprint, request, jsonify, session
from .models import User
import json
from . import db
from . import responseCode

studentViews = Blueprint('studentViews', __name__)
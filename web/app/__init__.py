from flask import Flask
from .src.dbmanager import BibleDB

app = Flask(__name__)
bible_db = BibleDB()

app.config['APPLICATION_ROOT'] = "/parabible"

from . import views, api

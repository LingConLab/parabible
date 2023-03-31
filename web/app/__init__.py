from flask import Flask
from flask_bootstrap import Bootstrap
from dbmanager import BibleDB

app = Flask(__name__)
bible_db = BibleDB()

app.config['APPLICATION_ROOT'] = "/parabible"

bootstrap = Bootstrap(app)
from app import views, api
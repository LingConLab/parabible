from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['APPLICATION_ROOT'] = "/parabible"

bootstrap = Bootstrap(app)
from app import views
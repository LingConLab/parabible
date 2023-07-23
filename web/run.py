#!flask/bin/python
from app.app import app
from app.api import *
from app.views import *

if __name__ == "__main__":
    app.run(debug = True, port=5001)

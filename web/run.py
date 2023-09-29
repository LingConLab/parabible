#!flask/bin/python

# env variables are loaded using docker compose file inside docker
# debugging is happening outside of container and we still want to load our env variables
# here we load them 
import logging
#logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('conf.env'))

from app.app import app
from app.api import *
from app.views import *

if __name__ == "__main__":
    app.run(debug = True, port=5001)

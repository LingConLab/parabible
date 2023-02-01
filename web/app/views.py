from app import app
from dbmanager import bible_db
from flask import render_template, request
import logging
from pprint import pformat
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/library', methods=['post', 'get'])
def library():
    if request.method == 'POST':
        texts = request.form.get('text_choose')
        print(texts)
    text_list = bible_db.get_text_list()
    logger.debug(pformat(text_list))
    if len(text_list) > 0:
        return render_template(
            "library.html",
            book_list={"Bible": [
                f"{x['closest_iso_639_3']}, {x['year_short']} \"{x['vernacular_title']}\""
                for x in bible_db.get_text_list()
            ]}
        )
    else:
        return render_template(
            "library.html",
            book_list={"Bible": ["Recieved 0 texts from the database. Is DB inited?"]}
        )
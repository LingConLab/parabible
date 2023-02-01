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

@app.route('/library', methods=['get'])
def library():    
    text_list = bible_db.get_text_list()
    logger.debug(f"SELECED texts: {text_list}")
    if text_list:
        return render_template(
            "library.html",
            book_list={"Bible": text_list}
        )
    else:
        return render_template(
            "library.html",
            book_list={"Bible": [
                {
                    "vernacular_title": "Recieved 0 texts from the database. Is DB inited?",
                    "id": 0
                }
            ]}
        )

@app.route('/corpus', methods=['post', 'get'])
def corpus():
    if request.method == 'POST':
        recieved = [int(i) for i, _ in request.form.items()]
        logger.debug(f"/corpus recieved ids: {recieved}")
        verses = [
            bible_db.get_verse(
                book_id=40,chapter_id=1,verse_id=1,
                translation_id=i
            )
            for i in recieved
        ]
        
    return render_template("corpus.html", verses = verses)
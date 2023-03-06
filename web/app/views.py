from app import app
from dbmanager import BibleDB
from flask import render_template, request
import logging
from re import sub as regex_sub
from pprint import pformat
import os

from .src import get_iso_lang_name

bible_db = BibleDB()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/library', methods=['get'])
def library():    
    text_list = bible_db.get_text_list()
    for t in text_list:
        t['closest_iso_639_3'] = get_iso_lang_name(t['closest_iso_639_3'])
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
        text_ids = [int(i) for i, _ in request.form.items() if str.isalnum(i)]; logger.debug(f"/corpus recieved ids: {text_ids}")
        texts_meta = [ bible_db.get_text_meta(i) for i in text_ids ]

        verse_ids = regex_sub(f'\s', '', request.form["ids_input"])
        verse_ids = [tuple(map(int, str_id.split(','))) for str_id in verse_ids.split(';')]
        logger.debug(verse_ids)

        for meta in texts_meta:
            meta["verses"] = {}
            for verse_id in verse_ids:
                meta["verses"][verse_id] = bible_db.get_verse(verse_id, meta["id"])

        return render_template(
            "corpus.html",
            texts_meta = texts_meta,
            verse_ids = verse_ids,
            b_ids = bible_db.get_verse_unique_ids("book_id"),
            ch_ids = bible_db.get_verse_unique_ids("chapter_id"),
            v_ids = bible_db.get_verse_unique_ids("verse_id")
        )

    elif request.method == 'GET':
        return render_template(
            "corpus.html",
            text_ids = []
        )

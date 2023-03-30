from app import app
from dbmanager import BibleDB
from flask import render_template, request
import logging
from re import sub as regex_sub
from pprint import pformat
import os
from collections import defaultdict

from .src import get_book_name, get_iso_lang_name

bible_db = BibleDB()
language_format_options = {
    'closest_iso_639_3': {
        'frontend_name': 'Closest ISO 639-3'
    },
    'iso_15924': {
        'frontend_name': 'ISO 15924'
    }, 
    'lang_name': {
        'frontend_name': 'Literal language name'
    }
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/testapi')
def testapi():
    texts = [None] * 3
    texts[0] = """But see, amid the mimic rout
   A crawling shape intrude!
A blood-red thing that writhes from out
   The scenic solitude!
It writhes!- it writhes!- with mortal pangs
   The mimes become its food,
And seraphs sob at vermin fangs
   In human gore imbued."""
    texts[1] = """That motley drama- oh, be sure
   It shall not be forgot!
With its Phantom chased for evermore,
   By a crowd that seize it not,
Through a circle that ever returneth in
   To the self-same spot,
And much of Madness, and more of Sin,
   And Horror the soul of the plot."""
    texts[2] = """Lo! 'tis a gala night
   Within the lonesome latter years!
An angel throng, bewinged, bedight
   In veils, and drowned in tears,
Sit in a theatre, to see
   A play of hopes and fears,
While the orchestra breathes fitfully
   The music of the spheres.
Mimes, in the form of God on high,
   Mutter and mumble low,
And hither and thither fly-
   Mere puppets they, who come and go
At bidding of vast formless things
   That shift the scenery to and fro,
Flapping from out their Condor wings
   Invisible Woe!"""
    id = int(request.args['id'])
    return texts[id]

@app.route('/test')
def testpage():
    return render_template("test.html")

@app.route('/library', methods=['get'])
def library():
    book_ids = bible_db.get_verse_unique_ids("book_id")
    book_ids_with_names = [(x, get_book_name(x)) for x in book_ids]
    return render_template(
        "library.html",
        book_ids = book_ids_with_names,
        chapter_ids = bible_db.get_verse_unique_ids("chapter_id"),
        verse_ids = bible_db.get_verse_unique_ids("verse_id"),
        lang_formats = language_format_options.items(),
    )

@app.route('/api/get/langs')
def api_get_langs():
    return_d = {}
    format = request.args.get('format', default=list(language_format_options.keys())[0], type=str)
    if not format in language_format_options:
        format = list(language_format_options.keys())[0]
          
    if format == 'lang_name':
        lang_list = bible_db.get_langs_list('closest_iso_639_3')
        return_d['val_format'] = 'closest_iso_639_3'
        return_d['lang_list'] = [ { 'label': get_iso_lang_name(x), 'val': x } for x in lang_list ]
    else:
        # just raw format as it is
        return_d['val_format'] = format
        lang_list = bible_db.get_langs_list(format)
        return_d['lang_list'] = [ { 'label': x, 'val': x } for x in lang_list ]

    return return_d

@app.route('/api/get/translations')
def api_get_translations():
    return_d = {}
    format = request.args.get('format', default=None, type=str)
    lang = request.args.get('lang', default=None, type=str)
    if not lang or not format:
        return f"<h1>Error 400</h1> 'lang' and 'format' arguments are both required", 400
    if not format in language_format_options:
        format = list(language_format_options.keys())[0]
        
    return_d['translations_list'] = bible_db.get_text_list(format, lang)

    return return_d

@app.route('/corpus', methods=['post', 'get'])
def corpus():
    if request.method == 'POST':
        # Get text meta
        text_ids = [ int(i) for i, _ in request.form.items() if str.isalnum(i) ]
        texts_meta = [ bible_db.get_text_meta(i) for i in text_ids ]
        # Expand text meta
        for i in range(len(texts_meta)):
            texts_meta[i]["lang_name"] = get_iso_lang_name(texts_meta[i]["closest_iso_639_3"])
        # Clear and process verse ids input
        verse_ids_clean_str = regex_sub(f'[^0-9.]+', ' ', request.form["verse_ids_input"])
        verse_ids = filter(lambda x: x != '', verse_ids_clean_str.split(' '))

        # Get translation lines from the db
        verse_lines = []
        for verse_id in verse_ids:
            book_id, chapter_id, verse_id = map(int, verse_id.split('.'))
            readable_id = f"{get_book_name(book_id)} {chapter_id}.{verse_id}"
            verse_data = {
                "id": readable_id,
                "translations": []
            }

            for text_id in text_ids:
                verse_data["translations"].append(
                    bible_db.get_verse(
                        (book_id, chapter_id, verse_id),
                        text_id
                    )
                )

            verse_lines.append(verse_data)

        return render_template(
            "corpus.html",
            texts_meta = texts_meta,
            verse_lines = verse_lines
        )

    elif request.method == 'GET':
        return render_template(
            "corpus.html",
            text_ids = []
        )

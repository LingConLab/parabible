from app import app, bible_db
from flask import render_template, request
import logging
from re import sub as regex_sub

from .src import get_book_name, get_iso_lang_name, get_book_ids, language_format_options

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/library', methods=['get'])
def library():
    book_ids = get_book_ids()
    book_ids_with_names = [ (x, get_book_name(x)) for x in book_ids ]
    return render_template(
        "library.html",
        book_ids = book_ids_with_names,
        lang_formats = language_format_options.items(),
    )

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

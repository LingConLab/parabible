from . import app, bible_db
from flask import render_template
import logging

from .src import get_book_name, get_book_ids, language_format_options

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/search', methods=['get'])
def library():
    book_ids = get_book_ids()
    book_ids_with_names = [ (x, get_book_name(x)) for x in book_ids ]
    return render_template(
        "search.html",
        book_ids = book_ids_with_names,
        lang_formats = language_format_options.items(),
    )

@app.route('/nothing', methods=['get', 'post'])
def corpus():
    return "This thing that you just pressed does nothing ... yet :)"

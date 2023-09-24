from .app import app
from flask import render_template, request
import logging

from .src.file_handling import file_data
from . import translations

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        "home.html",
        lang_cookie = request.cookies.get('lang') if request.cookies.get('lang') else translations.default_lang,
        translation_base = translations.translations_base,
        translation = translations.translations_home
    )

@app.route('/search', methods=['get'])
def library():
    book_ids = file_data.get_book_ids()
    book_ids_with_names = [ (x, file_data.get_book_title(x)) for x in book_ids ]
    return render_template(
        "search.html",
        lang_cookie = request.cookies.get('lang') if request.cookies.get('lang') else translations.default_lang,
        translation_base = translations.translations_base,
        translation = translations.translations_search,
        book_ids = book_ids_with_names,
        lang_formats = translations.language_format_options.items(),
    )

@app.route('/nothing', methods=['get', 'post'])
def corpus():
    return "This thing that you just pressed does nothing ... yet :)"

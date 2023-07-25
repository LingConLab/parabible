from flask import request

from .app import app
from .src.file_handling import file_data
from .src.dbmanager import BibleDB
from . import const

bible_db = BibleDB()

@app.route('/api/get/book_title_abbrs')
def api_get_book_abbrs():
    """Get book title abbriveations

    Returns: json object
        dict: { int: str }
    """
    return_d = file_data.get_book_abbrivs()
    return return_d

@app.route('/api/get/translation_meta')
def api_get_translation_meta():
    """Get meta of a translation by id

    Query Args:
        id (int): id of the translation

    Returns: json object
        dict: {
            'closest_iso_639_3': str,
            'copyright_long': str,
            'copyright_short': str,
            'english_title': str,
            'id': str,
            'iso_15924': str,
            'notes': str,
            'url': str,
            'vernacular_title': str,
            'year_long': str,
            'year_short': str
        }
    """
    return_d = {}
    translation_id = request.args.get('id', default=None, type=int)
    if not translation_id:
        return f"<h1>Error 400</h1> int 'id' argument is required", 400
    return_d = bible_db.get_translation_meta(translation_id)
    return return_d

@app.route('/api/get/book_ids')
def api_get_books():
    """Get ids of books that have at least one translated verse for the given translation.

    Query Args:
        translation_id (int): id(s) of translation(s)
        mode (str): "all" or "any"
            if "all" option is passed, return ids of books that contain translated verses in ALL translations
            if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

    Returns: json object
        dict: {
            'books': List[int]
        }
    """
    mode_options = ["any", "all"]
    return_d = {}

    translation_id_list = request.args.getlist('translation_id', type=int)
    mode = request.args.get('mode', default=None, type=str)

    if not translation_id_list or not mode:
        return f"<h1>Error 400</h1> Both 'mode' and 'translation_id' arguments are required", 400
    if not mode in mode_options:
        return f"<h1>Error 400</h1> 'mode' must be equal to one of these options {mode_options}", 400
    
    return_d['books'] = bible_db.get_books(translation_id_list, mode)
    return return_d

@app.route('/api/get/chapter_ids')
def api_get_chapters():
    """Get ids of chapters in a given book that have at least one translated verse in ALL or AT LEAST ONE given translation(s).

    Query Args:
        translation_id (int): id(s) of translation(s)
        book_id (int): id of the book
        mode (str): "all" or "any"
            if "all" option is passed, return ids of books that contain translated verses in ALL translations
            if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

    Returns: json object
        dict: {
            'chapters': List[int]
        }
    """
    mode_options = ["any", "all"]
    return_d = {}

    translation_id_list = request.args.getlist('translation_id', type=int)
    book_id = request.args.get('book_id', default=None, type=int)
    mode = request.args.get('mode', default=None, type=str)

    if not book_id or not translation_id_list or not mode:
        return f"<h1>Error 400</h1> All arguments 'book_id', 'translation_id' and 'mode' are required", 400
    if not mode in mode_options:
        return f"<h1>Error 400</h1> 'mode' must be equal to one of these options {mode_options}", 400
    if not book_id in file_data.get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {file_data.get_book_ids()}", 400
    
    return_d['chapters'] = bible_db.get_chapters(translation_id_list, book_id, mode)
    return return_d

@app.route('/api/get/verse_ids')
def api_get_verse_ids():
    """Get ids of verses in a given book and chapter that are translated in ALL or AT LEAST ONE given translation(s).

    Query Args:
        translation_id (int): id(s) of translation(s)
        book_id (int): id of the book
        chapter_id (int): id of the book
        mode (str): "all" or "any"
            if "all" option is passed, return ids of books that contain translated verses in ALL translations
            if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

    Returns: json object
        dict: {
            'verses': List[int]
        }
    """
    mode_options = ["any", "all"]
    return_d = {}

    translation_id_list = request.args.getlist('translation_id', type=int)
    book_id = request.args.get('book_id', default=None, type=int)
    chapter_id = request.args.get('chapter_id', default=None, type=int)
    mode = request.args.get('mode', default=None, type=str)

    if not book_id or not chapter_id or not translation_id_list or not mode:
        return f"<h1>Error 400</h1> All arguments 'book_id', 'chapter_id', 'translation_id' and 'mode' are required", 400
    if not mode in mode_options:
        return f"<h1>Error 400</h1> 'mode' must be equal to one of these options {mode_options}", 400
    if not book_id in file_data.get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {file_data.get_book_ids()}", 400
    
    return_d['verses'] = bible_db.get_verse_ids(translation_id_list, book_id, chapter_id, mode)
    return return_d

@app.route('/api/get/langs')
def api_get_langs():
    """Get list of languages in a specific format.

    Query Args:
        format (str): The format of the language's "label" in the returned dict.
            one of the following: ["iso_15924", "closest_iso_639_3", "lang_name"]

    Returns: json object
        dict: {
            "lang_list": List[
                dict: {
                    "label": str, 
                    "val": str
                }
            ],
            "val_format": str
        }

    Each language in a list is represented
    by a dictionary with keys "label" and "val".
    The format of the "val" is stored in "val_format".
    """
    return_d = {}
    format = request.args.get('format', default=list(const.language_format_options.keys())[0], type=str)
    if not format in const.language_format_options:
        format = list(const.language_format_options.keys())[0]
          
    if format == 'lang_name':
        lang_list = bible_db.get_langs_list('closest_iso_639_3')
        return_d['val_format'] = 'closest_iso_639_3'
        return_d['lang_list'] = [ { 'label': file_data.get_iso_lang_name(x), 'val': x } for x in lang_list ]
        return_d['lang_list'].sort(key=lambda x: x['label'])
    else:
        # just raw format as it is
        return_d['val_format'] = format
        lang_list = bible_db.get_langs_list(format)
        return_d['lang_list'] = [ { 'label': x, 'val': x } for x in lang_list ]

    return return_d

@app.route('/api/get/translations_by_lang')
def api_get_translations():
    """Get list of translation's meta in a specific language

    Query Args:
        format (str): format of the `lang` argument
            one of the following: ["iso_15924", "closest_iso_639_3", "lang_name"]
        lang (str): language name/iso

    Returns: json object
        dict: {
            "translations_list": List[
                List[
                    int: id of a translation,
                    str: Closest iso 639-3 tag,
                    str: Translation literal name,
                    str: Year of the translation's creation
                ]
            ]
        }

    Each translation in a list is represented
    by a list with four elements. 
    """
    return_d = {}
    format = request.args.get('format', default=None, type=str)
    lang = request.args.get('lang', default=None, type=str)
    if not lang or not format:
        return f"<h1>Error 400</h1> 'lang' and 'format' arguments are both required", 400
    if not format in const.language_format_options:
        format = list(const.language_format_options.keys())[0]
        
    return_d['translations_list'] = bible_db.get_text_list(format, lang)

    return return_d

@app.route('/api/get/verse')
def api_db_verse():
    return_d = {}
    book_id = request.args.get('book_id', default=None, type=int)
    chapter = request.args.get('chapter', default=None, type=int)
    verse = request.args.get('verse', default=None, type=int)
    translation_id = request.args.get('translation_id', default=None, type=int)

    if book_id is None:
        return f"<h1>Error 400</h1> 'book_id' argument is required", 400
    if chapter is None:
        return f"<h1>Error 400</h1> 'chapter' argument is required", 400
    if verse is None:
        return f"<h1>Error 400</h1> 'verse' argument is required", 400
    if translation_id is None:
        return f"<h1>Error 400</h1> 'translation_id' argument is required", 400

    return_d["verse"] = bible_db.get_verse((book_id, chapter, verse), translation_id)

    return return_d

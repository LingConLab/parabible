from flask import request

from . import app, bible_db
from .src.file_handling import file_data
from . import const

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
    return_d = bible_db.get_text_meta(translation_id)
    return return_d

@app.route('/api/get/chapter_ids')
def api_get_chapters():
    """Get ids of chapters in a specific book

    Query Args:
        book_id (int): id of the book

    Returns: json object
        dict: {
            'chapters': list[int]
        }
    """
    return_d = {}
    book_id = request.args.get('book_id', default=None, type=int)
    if not book_id:
        return f"<h1>Error 400</h1> int 'book_id' argument is required", 400
    if not book_id in file_data.get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {file_data.get_book_ids()}", 400
    return_d['chapters'] = file_data.get_chapters_ids(book_id)
    return return_d

@app.route('/api/get/verse_ids')
def api_get_verse_ids():
    """Get ids of verses in a specific chapter of a specific book

    Query Args:
        book_id (int): id of the book
        chapter_id (int): id of the book

    Returns: json object
        dict: {
            'verses': list[int]
        }
    """
    return_d = {}
    book_id = request.args.get('book_id', default=None, type=int)
    chapter_id = request.args.get('chapter_id', default=None, type=int)
    if not book_id or not chapter_id:
        return f"<h1>Error 400</h1> int arguments 'book_id' and 'chapter_id' are required", 400
    if not book_id in file_data.get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {file_data.get_book_ids()}", 400
    valid_chapters = file_data.get_chapters_ids(book_id)
    if not str(chapter_id) in valid_chapters:
        return f"<h1>Error 400</h1> 'chapter_id' ({chapter_id}) does not exist in this book (id={book_id} name=\"{file_data.get_book_title(book_id)}\"). Existing chapters: {valid_chapters}", 400
    
    return_d['verses'] = file_data.get_verses_ids(book_id, chapter_id)
    return return_d

@app.route('/api/get/langs')
def api_get_langs():
    """Get list of languages in a specific format.

    Query Args:
        format (str): The format of the language's "label" in the returned dict.
            one of the following: ["iso_15924", "closest_iso_639_3", "lang_name"]

    Returns: json object
        dict: {
            "lang_list": list[
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
            "translations_list": list[
                list[
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

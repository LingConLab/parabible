from flask import request

from app import app, bible_db
from .src import language_format_options, get_iso_lang_name, get_book_ids, get_book_name

@app.route('/api/get/chapters')
def api_get_chapters():
    return_d = {}
    book_id = request.args.get('book_id', default=None, type=int)
    if not book_id:
        return f"<h1>Error 400</h1> int 'book_id' argument is required", 400
    if not book_id in get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {get_book_ids()}", 400
    return_d['chapters'] = bible_db.get_chapters(book_id)
    return return_d

@app.route('/api/get/verses')
def api_get_verses():
    return_d = {}
    book_id = request.args.get('book_id', default=None, type=int)
    chapter_id = request.args.get('chapter_id', default=None, type=int)
    if not book_id or not chapter_id:
        return f"<h1>Error 400</h1> int arguments 'book_id' and 'chapter_id' are required", 400
    if not book_id in get_book_ids():
        return f"<h1>Error 400</h1> 'book_id' value ({book_id}) is invalid. Valid ids: {get_book_ids()}", 400
    valid_chapters = bible_db.get_chapters(book_id)
    if not chapter_id in valid_chapters:
        return f"<h1>Error 400</h1> 'chapter_id' ({chapter_id}) does not exist in this book (id={book_id} name=\"{get_book_name(book_id)}\"). Existing chapters: {valid_chapters}", 400
    
    return_d['verses'] = bible_db.get_verses(book_id, chapter_id)
    return return_d

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
        return_d['lang_list'].sort(key=lambda x: x['label'])
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
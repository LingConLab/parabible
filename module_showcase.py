from pprint import pprint
from web.dbmanager import bible_db
import logging
logging.basicConfig(format='  [%(levelname)s]:\t%(message)s', level=logging.DEBUG)

def load_data(f_name):
    from json import load
    with open(f"parser/bible_json/{f_name}", 'r', encoding='utf-8') as f:
        return load(f)

files = [
    "bul-x-bible-1940.json",
    "bul-x-bible-modern.json",
    "bul-x-bible-newworld.json",
    "bul-x-bible-veren.json",
    "eng-x-bible-riverside.json"
]

#for file in files:
#    bible_db.insert_new_text(load_data(file))

pprint(bible_db.get_text_list())

pprint(bible_db.get_verse(40, 3, 4, 3))

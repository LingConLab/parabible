from pprint import pprint
from pathlib import Path
from psycopg2.errors import OperationalError
import argparse
import logging

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

corpus_dir = Path("corpus-txt")

arg_parser = argparse.ArgumentParser(
    description = 'Fills the DB with bible texts.',
)
arg_parser.add_argument(
    '-m', '--mode',
    choices=["debug", "full"],
    help='What texts to download and insert. "debug" does 5 texts. "full" does all the texts'
)
arg_parser.add_argument(
    '-d', '--delete',
    action='store_true',
    help='Delete .zip and extracted files in the end (doesnt work for now)'
)
arg_parser.add_argument(
    '-i', '--index_only',
    action='store_true',
    help='Do not populate db. Create index only'
)
args = arg_parser.parse_args()
urls = {
    'debug': "http://91.200.84.6/parabible-data/debug_pb_corpus.zip",
    'full': "http://91.200.84.6/parabible-data/full_pb_corpus.zip"
}


def get_zip():
    """Downloads zip file from the server."""
    from wget import download as wget_download
    if not args.mode:
        logger.error(f"mode argument is required")
        return
    file = Path(urls[args.mode].split('/')[-1])
    if Path.exists(file):
        logger.info(f"'{file}' already exists. Downloading skipped")
        return file
    else:
        logger.info(f"Downloading {urls[args.mode]}...")

    return wget_download(urls[args.mode])

def unzip(file_name):
    """Extracts zip file."""
    if Path.exists(corpus_dir):
        logger.info(
            f"'{corpus_dir}' directory already exists. " + \
            "Unzipping skipped. " + \
            f"Remove '{corpus_dir}' dir if you want to clean unzip '{file_name}'"
        )
        return
    from zipfile import ZipFile
    from tqdm import tqdm
    print() 
    logger.info(f"Unzipping '{file_name}' into '{corpus_dir}'...")
    with ZipFile(file_name, 'r') as zObj:
        for member in tqdm(zObj.infolist(), desc='Extracting '):
            zObj.extract(member, path=corpus_dir)

def parse():
    """Connects to the DB and parses extracted content there."""
    from web.app.dbmanager import BibleDB
    from web.app.dbmanager.parser import parser as db_parser

    logger.info(f"Parsing .txt files into DB...")

    try:
        local_bible_db = BibleDB()
    except OperationalError as e:
        logger.error(e)
        logger.error("Cant connect to the database. Is postgres DB up?")
        logger.info("Make sure that the database is up")
        return
    auto_commit_threshold = 100
    iter = 1
    for text_data, file_name in db_parser.parsed_texts(corpus_dir):
        iter += 1
        if iter % auto_commit_threshold == 0:
            logger.debug(f"Commiting DB changes")
            local_bible_db.conn.commit()
        logger.debug(f"Processing {file_name}")

        local_bible_db.insert_new_text(text_data)

def update_book_structure_dict():
    from tqdm import tqdm
    from json import dump
    from web.app.dbmanager import BibleDB
    from web.app.src import get_book_ids, book_struct_file
    logger.info(f"Creating books structure index dicts...")
    try:
        local_bible_db = BibleDB()
    except OperationalError as e:
        logger.error(e)
        logger.error("Cant connect to the database. Is postgres DB up?")
        logger.info("Make sure that the database is up")
        return
    
    result_dict = {}
    for b_id in tqdm(get_book_ids(), desc="Books"):
        result_dict[b_id] = {}
        for ch_id in local_bible_db.get_chapters(b_id):
            result_dict[b_id][ch_id] = local_bible_db.get_verse_ids(b_id, ch_id)
    with open(book_struct_file, 'w', encoding='utf-8') as f:
        dump(result_dict, f, indent=4)

if __name__ == "__main__":
    if not args.index_only:
        file_name = get_zip()
        unzip(file_name)
        parse()
    update_book_structure_dict()

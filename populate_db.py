from pprint import pprint
from pathlib import Path
from psycopg2.errors import OperationalError
import argparse
import logging

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

current_dir: Path = Path(__file__).parent
corpus_dir = current_dir.joinpath(Path("corpus-txt"))
env_file = current_dir.joinpath(Path('web/conf.env'))

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
    '-p', '--db_port',
    default=None,
    help='Specify database port'
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
    from dotenv import load_dotenv, find_dotenv
    from os import getenv, system
    from web.app.src.dbmanager import BibleDB
    from web.app.src.dbmanager.parser import parser as db_parser

    logger.info(f"Parsing .txt files into DB...")

    load_dotenv(env_file)
    db_port = getenv('PARABIBLE_DEBUG_DB_PORT') if not args.db_port else args.db_port

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
    
    local_bible_db.conn.commit()
    logger.info(f"Done! All data was copied to the database. You may now delete the *_pb_corpus.zip file and {corpus_dir} folder if its still present.")
    logger.info(f"Removing {corpus_dir}...")
    if system(f"rm -r {corpus_dir}") == 0:
        logger.info(f"Temporary corpus dir was removed.")
    else:
        logger.error(f"Failed to remove temporary {corpus_dir}. Feel free to remove it")

if __name__ == "__main__":
    file_name = get_zip()
    unzip(file_name)
    parse()

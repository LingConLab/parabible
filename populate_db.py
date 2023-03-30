from pprint import pprint
from pathlib import Path
import argparse
import logging

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

arg_parser = argparse.ArgumentParser(
    description = 'Fills the DB with bible texts.',
)
arg_parser.add_argument(
    '-m', '--mode',
    choices=["debug", "full"],
    help='What texts to download and insert. "debug" does 5 texts. "full" does all the texts',
    required=True
)
arg_parser.add_argument(
    '-d', '--delete',
    action='store_true',
    help='Delete .zip file after extraction.'
)
args = arg_parser.parse_args()
urls = {
    'debug': "http://91.200.84.6/parabible-data/debug_pb_corpus.zip",
    'full': "http://91.200.84.6/parabible-data/full_pb_corpus.zip"
}
corpus_dir = Path("corpus-txt")

def get_zip():
    from wget import download as wget_download
    file = Path(urls[args.mode].split('/')[-1])
    if Path.exists(file):
        logger.info(f"'{file}' already exists. Downloading skipped")
        return file
    else:
        logger.info(f"Downloading {urls[args.mode]}...")

    return wget_download(urls[args.mode])

def unzip(file_name):
    if Path.exists(corpus_dir):
        logger.info(
            f"'{corpus_dir}' directory already exists. " + \
            "Unzipping skipped.\n" + \
            f"Remove '{corpus_dir}' dir if you want to clean unzip '{file_name}'"
        )
    else:
        from zipfile import ZipFile
        from tqdm import tqdm
        print() 
        logger.info(f"Unzipping '{file_name}' into '{corpus_dir}'...")
        with ZipFile(file_name, 'r') as zObj:
            for member in tqdm(zObj.infolist(), desc='Extracting '):
                zObj.extract(member, path=corpus_dir)

def parse():
    from web.dbmanager import BibleDB
    from web.dbmanager.parser import parser as db_parser

    logger.info(f"Parsing .txt files into DB...")

    local_bible_db = BibleDB()
    auto_commit_threshold = 100
    iter = 1
    for text_data, file_name in db_parser.parsed_texts(corpus_dir):
        iter += 1
        if iter % auto_commit_threshold == 0:
            logger.debug(f"Commiting DB changes")
            local_bible_db.conn.commit()
        logger.debug(f"Processing {file_name}")

        local_bible_db.insert_new_text(text_data)

if __name__ == "__main__":
    file_name = get_zip()
    unzip(file_name)
    parse()

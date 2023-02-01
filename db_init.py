from pprint import pprint
from pathlib import Path
import logging

from web.dbmanager import bible_db
from web.dbmanager.parser import parser

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

texts_dir = f"paralleltext-master/bibles"

def main():
    auto_commit_threshold = 100
    iter = 1
    for text_data, file_name in parser.parsed_texts(texts_dir):
        iter += 1
        if iter % auto_commit_threshold == 0:
            logger.debug(f"Commiting DB changes")
            bible_db.conn.commit()
        #logger.info(f"Processing {file_name}")

        bible_db.insert_new_text(text_data)

if __name__ == "__main__":
    main()

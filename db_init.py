from pprint import pprint
from pathlib import Path
import logging

from web.dbmanager import bible_db
from parser.src.parser import parsed_texts, logger as parser_logger

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

texts_dir = f"parser/paralleltext-master/bibles/corpus"

def main():
    auto_commit_threshold = 50
    iter = 1
    for text_data, file_name in parsed_texts(texts_dir):
        iter += 1
        if iter % auto_commit_threshold == 0:
            logger.info(f"Commiting DB changes")
            bible_db.conn.commit()
        logger.info(f"Processing {file_name}")

        bible_db.insert_new_text(text_data)

if __name__ == "__main__":
    main()

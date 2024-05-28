from pathlib import Path
from typing import List
from tqdm import tqdm
import logging
import csv

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from web.app.src.dbmanager import BibleDB
from web.app.src.file_handling import file_data

def get_book_abbrivs() -> dict:
    return file_data.get_book_abbrivs()

def get_chapters(db: BibleDB, translation_id: int, book_id: int) -> List[int]:
    return db.get_chapters(translation_id, book_id)

def get_verses(db: BibleDB, translation_id: int, book_id: int, chapter: int) -> List[int]:
    return db.get_verse_ids(translation_id, book_id, chapter)

def get_verse_text(db: BibleDB, translation_id: int, book_id: int, chapter: int, verse: int) -> str:
    return db.get_verse((book_id, chapter, verse), translation_id)

def form_verse_tag(abbrivs: dict, book_id: int, chapter: int, verse: int) -> str:
    return f"{abbrivs[book_id]} {chapter}:{verse}"

def main():
    db = BibleDB()
    csv_result = Path(__file__).parent.joinpath('misc_scripts/script_data/export.csv')

    BOOK_IDS = range(40, 67) # 40 - 66
    TRANS_ID = 627
    abbrivs = {int(k): v for k, v in get_book_abbrivs().items()}

    with open(csv_result, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(("Verse", "Text"))
        for book_id in BOOK_IDS:
            logger.info(f"Processing {abbrivs[book_id]}")
            chapters = get_chapters(db, TRANS_ID, book_id)
            logger.info(f"{len(chapters)} chapters")
            for ch in chapters:
                logger.info(f"Chapter {ch}")
                verses = get_verses(db, TRANS_ID, book_id, ch)
                logger.info(f"{len(verses)} verses")
                for v in tqdm(verses):
                    verse_text = get_verse_text(db, TRANS_ID, book_id, ch, v)
                    verse_tag = form_verse_tag(abbrivs, book_id, ch, v)
                    writer.writerow((verse_tag, verse_text))

if __name__ == "__main__":
    main()

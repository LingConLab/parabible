from pathlib import Path
from time import sleep
from tqdm import tqdm
import requests
import logging
import json
import csv

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

API = "http://lingconlab.ru/parabible/api"

def call_api(url: str) -> dict:
    logger.debug(f"Getting {url}")
    resp = requests.get(url)
    if not resp.ok:
        logger.error(f"Error! {resp.text}")
        raise Exception(f"Error! {resp.text}")
    return json.loads(resp.text)

def get_book_abbrivs() -> dict:
    url = "http://lingconlab.ru/parabible/api/get/book_title_abbrs"
    return call_api(url)

def get_chapters(translation_id: int, book_id: int) -> list[int]:
    url = f"{API}/get/chapter_ids?mode=all"
    url += f"&translation_id={translation_id}"
    url += f"&book_id={book_id}"
    return call_api(url)['chapters']

def get_verses(translation_id: int, book_id: int, chapter: int) -> list[int]:
    url = f"{API}/get/verse_ids?mode=all"
    url += f"&translation_id={translation_id}"
    url += f"&book_id={book_id}&chapter_id={chapter}"
    return call_api(url)['verses']

def get_verse_text(translation_id: int, book_id: int, chapter: int, verse: int) -> str:
    url = f"{API}/get/verse?"
    url += f"translation_id={translation_id}"
    url += f"&book_id={book_id}&chapter={chapter}&verse={verse}"
    return call_api(url)['verse']

def form_verse_tag(abbrivs: dict, book_id: int, chapter: int, verse: int) -> str:
    return f"{abbrivs[book_id]} {chapter}:{verse}"

def main():
    csv_result = Path(__file__).parent.joinpath('misc_scripts/script_data/export.csv')

    BOOK_IDS = range(40, 67) # 40 - 66
    TRANS_ID = 627
    abbrivs = {int(k): v for k, v in get_book_abbrivs().items()}

    with open(csv_result, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(("Verse", "Text"))
        for book_id in BOOK_IDS:
            logger.info(f"Processing {abbrivs[book_id]}")
            chapters = get_chapters(TRANS_ID, book_id)
            logger.info(f"{len(chapters)} chapters")
            for ch in chapters:
                logger.info(f"Chapter {ch}")
                verses = get_verses(TRANS_ID, book_id, ch)
                logger.info(f"{len(verses)} verses")
                for v in tqdm(verses):
                    verse_text = get_verse_text(TRANS_ID, book_id, ch, v)
                    verse_tag = form_verse_tag(abbrivs, book_id, ch, v)
                    writer.writerow((verse_tag, verse_text))
                    sleep(0.2)

if __name__ == "__main__":
    main()

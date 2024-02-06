from psycopg2.errors import OperationalError
from pathlib import Path
import csv
import logging

logging.basicConfig(format='[%(levelname)s]:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from web.app.src.dbmanager import BibleDB

csv_input = Path('./script_data/Шаблон.csv')
new_lang_name = 'Armenian'
translation_id = 1343
csv_output = Path(f'./script_data/{new_lang_name}_{translation_id}.csv')
book_ids = {
    'Мф': 40,   # Matthew
    'Мк': 41,   # Mark
    'Лк': 42,   # Luke
    'Ин': 43,   # John
    'Деян': 44, # Acts
    'Откр': 66  # Revelation
}

def main():
    try:
        db = BibleDB()
    except OperationalError as e:
        logger.error(e)
        logger.error("Cant connect to the database. Is postgres DB up?")
        logger.info("Make sure that the database is up")
        return

    def get_verse(book, chapter, verse):
        return db.get_verse(
            (book_ids[book], chapter, verse),
            translation_id
        )

    with open(csv_input, 'r', newline='') as f_in:
        reader = csv.reader(f_in)

        col_names = next(reader)
        new_col_id = col_names.index('Ярлык1')
        col_names.insert(new_col_id, new_lang_name)

        with open(csv_output, 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(col_names)

            for row in reader:
                new_row = [ x for x in row ]
                new_row.insert(new_col_id, get_verse(row[0], row[1], row[2]))
                writer.writerow(new_row)

if __name__ == '__main__':
    main()

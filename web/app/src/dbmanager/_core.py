import psycopg2
from typing import List, Dict, Tuple
from psycopg2.extras import RealDictCursor, DictCursor
from psycopg2.extensions import AsIs
from typing import Literal
from collections import defaultdict
import logging

from ._const import NONE_LABEL

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def check_conn(func):
    def wrapped(self, *args, **kwargs):
        if self.conn:
            logger.debug(f"Connection is present. {self.conn}")
            return func(self, *args, **kwargs)
        else:
            logger.fatal(f"Attempted to access database with no connection to the database.{args}")
            logger.info(f"Trying to reconnect")
            try:
                self.conn = self.connect(self.DB_HOST)
            except psycopg2.OperationalError as e:
                logger.critical(f"Failed to reconnect to the database {e}")
                self.conn = None
            
    return wrapped

class BibleDB():
    def __init__(self, host_options: list = None) -> None:
        """Initializates connection and creates tables if dont exist"""

        if not host_options:
            host_options = []

        host_options.append('0.0.0.0')
        host_options.append('localhost')
        host_options.append('db')

        self.DB_NAME = "parabible"
        self.DB_USER = "dev"
        self.DB_PASS = "dev"
        self.DB_PORT = "5432"

        for host in host_options:
            try:
                self.conn = self.connect(host)
                logger.info(f"Connected to host {host}")
                break
            except psycopg2.OperationalError as e:
                logger.info(f"Failed to connect to the host option {host}\n{e}")
        else:
            # raise OperationalError exeption
            self.connect(host_options[0])

    def connect(self, host):
        return psycopg2.connect(
            database    =   self.DB_NAME,
            user        =   self.DB_USER,
            password    =   self.DB_PASS,
            host        =   host,
            port        =   self.DB_PORT
        )
    
    @check_conn
    def get_text_list(self, lang_format: str, lang: str, collumns: List[str] = None) -> List[dict]:
        """Return ids and other collumns of all the texts

        Args:
            collumns (List[str], optional): If None, returns defualt set of db collumns.
            You can override it

            Default: [
                "closest_iso_639_3",
                "vernacular_title",
                "year_short"
            ]

        Returns:
            List[dict]: list of entries dicts. Col name: value
        """
        if not lang_format in ["closest_iso_639_3", "iso_15924"]:
            return []
        if not collumns:
            collumns = [
                "closest_iso_639_3",
                "vernacular_title",
                "year_short"
            ]
        collumns.insert(0, "id")

        cur = self.conn.cursor()

        cur.execute("""
            SELECT
                %s
            FROM translations
            WHERE
                %s = %s
        """,
        (AsIs(''.join([f"{c}," for c in collumns]).removesuffix(',')),
        AsIs(lang_format), lang))
        result = cur.fetchall()
        logger.debug(result)
        return result

    @check_conn
    def get_verse(self, verse_id: Tuple[int], translation_id: int) -> str:
        """Get verse text in specific translation

        Args:
            verse_id (Tuple[int]) : (
                book_id (int): id of the book
                chapter_id (int): id of the chapter
                verse_id (int): id of the verse
            )
            translation_id (int): id of the translation

        Returns:
            str: text of the verse
        """
    
        logger.debug(f"SELECT verse with id {verse_id} translation {translation_id}")
        cur = self.conn.cursor()

        cur.execute(
            """
                SELECT line FROM verses
                WHERE 
                    book_id = %s AND
                    chapter_id = %s AND
                    verse_id = %s AND
                    translation_id = %s
            """, (verse_id[0], verse_id[1], verse_id[2], translation_id))

        result = cur.fetchone()
        return result[0] if result else result

    @check_conn
    def get_text_meta(self, id: int) -> Dict[str, any]:
        """Get meta of the text by its id

        Args:
            id (int): Id of the text

        Returns:
            Dict[str, any]: Meta of the text

            possible dict keys:
                closest_iso_639_3
                copyright_long
                copyright_short
                english_title
                id
                iso_15924
                notes
                url
                vernacular_title
                year_long
                year_short
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """ SELECT * FROM translations WHERE id = %s; """,
            (id,)
        )

        # Extract the column names
        #col_names = tuple(elt[0] for elt in cur.description)

        return dict(cur.fetchone())

    @check_conn
    def get_chapters(self, book_id: int):
        cur = self.conn.cursor()
        cur.execute(
            """ SELECT chapter_id FROM verses
                WHERE book_id = %s
                GROUP BY chapter_id; """, 
            (book_id,)
        )
        result = cur.fetchall()
        return result if not result else sorted( i[0] for i in result )
    
    @check_conn
    def get_verse_ids(self, book_id: int, chapter_id: int):
        cur = self.conn.cursor()
        cur.execute(
            """ SELECT verse_id FROM verses
                WHERE
                    book_id = %s AND
                    chapter_id = %s
                GROUP BY verse_id; """, 
            (book_id, chapter_id)
        )
        result = cur.fetchall()
        return result if not result else sorted( i[0] for i in result )

    @check_conn
    def insert_new_text(self, data: dict) -> None:
        """Loads new text into db

        Args:
            data (dict): text data

        Text data format example:
            {
                "meta": {
                    "language_name": "English",
                    "year_long": "1923; 2009",
                    "meta_tag": "meta_val",
                },
                "data": {
                    "lines": [  
                        {
                            "book_id": 40,
                            "chapter_id": 1,
                            "verse_id": 1,
                            "line": "THE ancestral line of Jesus Christ , son of David , son of Abraham :"
                        },
                        {
                            "book_id": 40,
                            "chapter_id": 1,
                            "verse_id": 2,
                            "line": "Abraham was the father of Isaac ; Isaac was the father of Jacob ; Jacob was the father of Judah and his brothers ;"
                        }
                    ]
                }
            }
        """

        if self.__is_dublicate(data["meta"]):
            logger.debug(f'\033[FText from {data["meta"]["url"]} is already present. It is skipped')
            return

        verse_cursor = self.conn.cursor()            
        translation_id = self.__insert_translation_meta(data["meta"])
        
        logger.debug(f"inserting verses of text with id = {translation_id} ({data['meta']['vernacular_title']})")

        """ for verse in data["data"]["lines"]:
            self.__insert_verse(verse, translation_id, verse_cursor) """
        bulk_size = 100
        verse_amount = len(data["data"]["lines"])

        logger.debug(f"{verse_amount} verses, {bulk_size} bulk size")

        for i in range(0, verse_amount - bulk_size, bulk_size):
            self.__insert_verse_bulk(
                data["data"]["lines"],
                i,
                min(i + bulk_size, verse_amount),
                translation_id,
                verse_cursor
            )

        self.conn.commit()
        #logger.info(f"{len(data['data']['lines'])} verses done!")

    @check_conn
    def get_langs_list(self, format: Literal["iso_15924", "closest_iso_639_3"]) -> list:
        cur = self.conn.cursor()
        sql_str = cur.mogrify(
            """ SELECT DISTINCT %s FROM translations; """, 
            (AsIs(format),)
        )
        cur.execute(sql_str)
        result = cur.fetchall()
        if not result:
            return result 
        result = map(lambda x: x[0], result)
        # result = map(lambda x: x if x else NONE_LABEL, result)
        result = filter(lambda x: bool(x), result) # removing None value
        result = sorted(result)
        logger.debug(result)
        return result

    @check_conn
    def __form_verse_values_string(self, data: dict, translation_id: int, cur) -> str:
        return cur.mogrify(
            "(%s, %s, %s, %s, %s)",
            (
                data["book_id"], data["chapter_id"],
                data["verse_id"], translation_id,
                data["line"]
            )
        )

    @check_conn
    def __insert_verse(self, data: dict, translation_id: int, cur):
        values_string = self.__form_verse_values_string(data, translation_id, cur)
        cur.execute(b"""
                INSERT INTO verses
                (book_id, chapter_id, verse_id, translation_id, line)
                VALUES
                """ + values_string
        )

    @check_conn
    def __insert_verse_bulk(self, data_list: List[dict], begin: int, end: int, translation_id: int, cur):
        """`begin`, `end` are indexes of current window.
        In order to not use additional memory.
        We dont slice or copy subarray, we pass it and tell the borders"""

        logger.debug(f"[{begin}, {end})")

        values_string = b','.join(
            self.__form_verse_values_string(
                data_list[i], translation_id, cur
            )
            for i in range(begin, end)
        )
        cur.execute(b"""
                INSERT INTO verses
                (book_id, chapter_id, verse_id, translation_id, line)
                VALUES
                """ + values_string + b" ON CONFLICT DO NOTHING"
        )

    @check_conn
    def __insert_translation_meta(self, meta: Dict[str, str]) -> int:
        """
        Args:
            meta (Dict[str]): meta data dict. It will replace missing key values with None.

        Raises:
            Exception: if db returns anything but integer

        Returns:
            int: id of the inserted record
        """        """"""
        auto_meta = defaultdict(lambda: None)
        auto_meta.update(meta)
        cursor = self.conn.cursor()
        cursor.execute("""
                INSERT INTO translations
                (
                    closest_iso_639_3, iso_15924,
                    year_short, year_long,
                    vernacular_title, english_title, url,
                    copyright_short, copyright_long, notes
                ) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
            (
                auto_meta["closest iso 639-3"], auto_meta["iso_15924"],
                auto_meta["year_short"], auto_meta["year_long"],
                auto_meta["vernacular_title"], auto_meta["english_title"], auto_meta["url"],
                auto_meta["copyright_short"], auto_meta["copyright_long"], auto_meta["notes"]
            )
        )
        self.conn.commit()
        returned_id = cursor.fetchone()[0]
        if isinstance(returned_id, int):
            return returned_id
        else:
            raise Exception(f"returned_id expected to be int. Got {returned_id} ({type(returned_id)})")

    @check_conn
    def __is_dublicate(self, meta: dict) -> bool:
        return False
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id
            FROM translations
            WHERE
                url                 = %s AND
                vernacular_title    = %s AND
                english_title       = %s
        """, (meta['url'], meta['vernacular_title'], meta['english_title']))
        result = cursor.fetchall()
        return bool(len(result))

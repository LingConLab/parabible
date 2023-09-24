import psycopg2
from typing import List, Dict, Tuple, Union
from psycopg2.extras import RealDictCursor, DictCursor
from psycopg2.extensions import AsIs
from typing import Literal
from collections import defaultdict
import logging

from ._const import NONE_LABEL

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
    def __init__(self, host_options: list = None, db_port: str = "5432") -> None:
        """Initializates connection and creates tables if dont exist"""

        if not host_options:
            host_options = []

        host_options.append('0.0.0.0')
        host_options.append('localhost')
        host_options.append('db')
        
        self.DB_NAME = "parabible"
        self.DB_USER = "dev"
        self.DB_PASS = "dev"
        self.DB_PORT = db_port

        for host in host_options:
            try:
                self.conn = self.connect(host)
                logger.info(f"Connected to host {host}")
                break
            except psycopg2.OperationalError as e:
                logger.debug(f"Failed to connect to the host option {host}\n{e}")
        else:
            logger.critical(f"""Failed to connect to the database.
            Tried to connect to following hosts: {host_options}
            Port: {self.DB_PORT}
            Without the connection to the database nothing but static html content will work!""")

    def connect(self, host):
        logger.info(f"Connection to {host}:{self.DB_PORT}")
        return psycopg2.connect(
            database        =   self.DB_NAME,
            user            =   self.DB_USER,
            password        =   self.DB_PASS,
            host            =   host,
            port            =   self.DB_PORT,
            connect_timeout =   5
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
    def get_translation_meta(self, id: int) -> Dict[str, any]:
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
    def get_books(self, translation_ids: Union[int, List[int]], mode: Literal["any", "all"] = "all") -> List[int]:
        """Get ids of books that have at least one translated verse in ALL or AT LEAST ONE given translation(s).

        Args:
            translation_ids (int | List[int]): id(s) of translation(s)
            mode (str): if "all" option is passed, return ids of books that contain translated verses in ALL translations
                        if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

        Returns:
            List[int]: list of book ids
        """        
        if isinstance(translation_ids, int): translation_ids = [translation_ids]
        cur = self.conn.cursor()
        if mode == "all":
            cur.execute(
                """ SELECT book_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s
                        GROUP BY book_id
                        HAVING COUNT(DISTINCT translation_id) = %(translation_count)s
                        ORDER BY book_id; """, 
                {'translation_ids': tuple(translation_ids),
                 'translation_count': len(translation_ids)}
            )
        elif mode == "any":
            cur.execute(
                """ SELECT book_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s
                        GROUP BY book_id
                        ORDER BY book_id; """, 
                {'translation_ids': tuple(translation_ids)}
            )
        else:
            raise ValueError(f"'mode' argument may be only 'any' or 'all'. Got '{mode}'")
        
        result = cur.fetchall()
        return result if not result else [i[0] for i in result]

    @check_conn
    def get_chapters(self, translation_ids: Union[int, List[int]], book_id: int, mode: Literal["any", "all"] = "all") -> List[int]:
        """Get ids of chapters in a given book that have at least one translated verse in ALL or AT LEAST ONE given translation(s).

        Args:
            translation_ids (int | List[int]): id(s) of translation(s)
            book_id (int): id of a book
            mode (str): if "all" option is passed, return ids of books that contain translated verses in ALL translations
                        if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

        Returns:
            List[int]: list of chapter numbers (ids)
        """
        if isinstance(translation_ids, int): translation_ids = [translation_ids]
        cur = self.conn.cursor()
        if mode == "all":
            cur.execute(
                """ SELECT chapter_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s AND
                            book_id = %(book_id)s
                        GROUP BY chapter_id
                        HAVING COUNT(DISTINCT translation_id) = %(translation_count)s
                        ORDER BY chapter_id; """, 
                {'translation_ids': tuple(translation_ids),
                 'book_id': book_id,
                 'translation_count': len(translation_ids)}
            )
        elif mode == "any":
            cur.execute(
                """ SELECT chapter_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s AND
                            book_id = %(book_id)s
                        GROUP BY chapter_id
                        ORDER BY chapter_id; """, 
                {'translation_ids': tuple(translation_ids),
                 'book_id': book_id}
            )
        else:
            raise ValueError(f"'mode' argument may be only 'any' or 'all'. Got '{mode}'")
        
        result = cur.fetchall()
        return result if not result else [i[0] for i in result]
    
    @check_conn
    def get_verse_ids(self, translation_ids: Union[int, List[int]], book_id: int, chapter_id: int, mode: Literal["any", "all"] = "all") -> List[int]:
        """Get ids of verses in a given book and chapter that are translated in ALL or AT LEAST ONE given translation(s).

        Args:
            translation_ids (int | List[int]): id(s) of translation(s)
            book_id (int): id of a book
            chapter_id (int): id of a chapter
            mode (str): if "all" option is passed, return ids of books that contain translated verses in ALL translations
                        if "any" option is passed, return ids of books that contain translated verses in AT LEAST ONE translation

        Returns:
            List[int]: list of verse numbers (ids)
        """
        if isinstance(translation_ids, int): translation_ids = [translation_ids]
        cur = self.conn.cursor()
        if mode == "all":
            cur.execute(
                """ SELECT verse_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s   AND
                            book_id         = %(book_id)s           AND
                            chapter_id      = %(chapter_id)s
                        GROUP BY verse_id
                        HAVING COUNT(DISTINCT translation_id) = %(translation_count)s
                        ORDER BY verse_id; """, 
                {'translation_ids': tuple(translation_ids),
                 'book_id': book_id,
                 'chapter_id': chapter_id,
                 'translation_count': len(translation_ids)}
            )
        elif mode == "any":
            cur.execute(
                """ SELECT verse_id FROM verses 
                        WHERE
                            translation_id in %(translation_ids)s   AND
                            book_id         = %(book_id)s           AND
                            chapter_id      = %(chapter_id)s
                        GROUP BY verse_id
                        ORDER BY verse_id; """, 
                {'translation_ids': tuple(translation_ids),
                 'book_id': book_id,
                 'chapter_id': chapter_id}
            )
        else:
            raise ValueError(f"'mode' argument may be only 'any' or 'all'. Got '{mode}'")
        
        result = cur.fetchall()
        return result if not result else [i[0] for i in result]

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

        # 'straight forward' way to do this. This inserts verses one by one which is slow
        """ for verse in data["data"]["lines"]:
            self.__insert_verse(verse, translation_id, verse_cursor) """
        # here we insert verses in bulk 100 verses at a time. This drastically improves speed of inserting new translation
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
        """Helper func for verse insertion. 
        Converts safely data["book_id"], data["chapter_id"], data["verse_id"], translation_id, data["line"]
        to sql string
        (40, 1, 1, 12, "verse line goes here ...")

        Args:
            data (dict)
            translation_id (int)
            cur (_type_)

        Returns:
            str: sql formatted string
        """        
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
    def get_index_size(self, table_name: str, index_name: str) -> str:
        cur = self.conn.cursor()
        cur.execute(
            """ SELECT pg_size_pretty(pg_total_relation_size('%s')) AS index_size
                FROM pg_indexes
                WHERE tablename = '%s' AND indexname = '%s'; """, 
            (index_name, table_name, index_name)
        )
        result = cur.fetchall()
        return result if not result else [i[0] for i in result]

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

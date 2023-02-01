import psycopg2
import logging

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ._schemas import table_schemas

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
            except psycopg2.OperationalError:
                try:
                    self.conn = self.connect(self.ALT_DB_HOST)
                except psycopg2.OperationalError as e:
                    logger.critical(f"Failed to cennect to the datbase{e}")
                    self.conn = None
            
    return wrapped

class BibleDB():
    DB_NAME = "parabible"
    DB_USER = "dev"
    DB_PASS = "dev"
    DB_HOST = "parabible-postgresql"; ALT_DB_HOST = "0.0.0.0"
    DB_PORT = "5432"

    def __init__(self) -> None:
        """Initializates connection and creates tables if dont exist
        """
        try:
            self.conn = self.connect(self.DB_HOST)
        except psycopg2.OperationalError:
            try:
                self.conn = self.connect(self.ALT_DB_HOST)
            except psycopg2.OperationalError as e:
                logger.critical(f"Failed to cennect to the datbase{e}")
                self.conn = None
        self.create_tables()

    def connect(self, host):
        return psycopg2.connect(
            database    =   self.DB_NAME,
            user        =   self.DB_USER,
            password    =   self.DB_PASS,
            host        =   host,
            port        =   self.DB_PORT
        )

    @check_conn
    def create_tables(self) -> None:  
        cur = self.conn.cursor()
        
        for table in table_schemas:
            collumns = ''.join([f"{k} {v}," for k, v in table["collumns"].items()])
            other = ''.join([f"{val}," for val in table["other"]])

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS "{name}"({collumns})
                """.format(
                    name = table["name"],
                    collumns = str(collumns + other).removesuffix(',')
                )
            )

        self.conn.commit()
    
    @check_conn
    def get_text_list(self, collumns: list[str] = None) -> list[dict]:
        """Return ids and other collumns of all the texts

        Args:
            collumns (list[str], optional): If None, returns defualt set of db collumns.
            You can override it

            Default: [
                "closest_iso_639_3",
                "vernacular_title",
                "year_short"
            ]

        Returns:
            list[dict]: list of entries dicts. Col name: value
        """

        if not collumns:
            collumns = [
                "closest_iso_639_3",
                "vernacular_title",
                "year_short"
            ]
        collumns.insert(0, "id")

        cur = self.conn.cursor()

        cur.execute(f"""
            SELECT
                {''.join([f"{c}," for c in collumns]).removesuffix(',')}
            FROM translations
        """)

        result = cur.fetchall()
        dict_formatted = [{collumns[i]: tup[i] for i in range(len(tup))} for tup in result]
        return dict_formatted

    @check_conn
    def get_verse(self, book_id: int, chapter_id: int, verse_id: int, translation_id: int) -> str:
        """Get verse text in specific translation

        Args:
            book_id (int): id of the book
            chapter_id (int): id of the chapter
            verse_id (int): id of the verse
            translation_id (int): id of the translation

        Returns:
            str: text of the verse
        """
        cur = self.conn.cursor()

        cur.execute("""
            SELECT line from verses
            WHERE 
                book_id = %s AND
                chapter_id = %s AND
                verse_id = %s AND
                translation_id = %s
        """, (book_id, chapter_id, verse_id, translation_id))

        return cur.fetchone()[0]

    @check_conn
    def get_lang_id(self, lang_name: str) -> int:
        """Dummy. Dont use it. It does nothing

        Args:
            lang_name (str): _description_

        Returns:
            int: _description_
        """
        return -1
        existing = self.get_lang_id_only_if_exists(lang_name=lang_name)
        if existing >= 0: return existing

        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO langs
            (name)
            VALUES
            (%s)
            RETURNING id
        """, (lang_name,))
        self.conn.commit()
        return cur.fetchone()

    @check_conn
    def get_lang_id_only_if_exists(self, lang_name: str) -> int:
        """Dummy. Dont use it. It does nothing

        Args:
            lang_name (str): _description_

        Returns:
            int: _description_
        """
        return -1
        
        lang_name = lang_name.strip().lower()
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id
            FROM langs
            WHERE name = %s
        """,
        (lang_name,))
        
        res = cur.fetchall()
        if len(res) == 1: return res[0]
        
        return -1

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
    def __insert_verse_bulk(self, data_list: list[dict], begin: int, end: int, translation_id: int, cur):
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
    def __insert_translation_meta(self, meta):
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
                meta["closest iso 639-3"], meta["iso_15924"],
                meta["year_short"], meta["year_long"],
                meta["vernacular_title"], meta["english_title"], meta["url"],
                meta["copyright_short"], meta["copyright_long"], meta["notes"]
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

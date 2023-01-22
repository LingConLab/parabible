from pprint import pprint
import logging
import psycopg2

logging.basicConfig(format='  [%(levelname)s]:\t%(message)s', level=logging.DEBUG)

TABLES = {
    "translations":
        """
        id                  SERIAL PRIMARY KEY,
        lang_id             INT,
        closest_iso_639_3   TEXT,
        iso_15924           TEXT,
        year_short          TEXT,
        year_long           TEXT,
        vernacular_title    TEXT,
        english_title       TEXT,
        url                 TEXT,
        copyright_short     TEXT,
        copyright_long      TEXT,
        notes               TEXT
        """,
    "langs":
        """
        id                  SERIAL PRIMARY KEY,
        name                TEXT
        """,
    "translated_segments":
        """
        segment_id          INT,
        translation_id      INT,
        data                TEXT,
        PRIMARY KEY(segment_id, translation_id)
        """,
    "hashed_wordforms":
        """
        wordform_hash       SERIAL PRIMARY KEY,
        segment_id          INT,
        translation_id      INT
        """,
}
DB_NAME = "parabible"
HOST_ADDR = "0.0.0.0"
PORT = "5432"

conn = psycopg2.connect(
        database = DB_NAME,
        user = "dev",
        password = "dev",
        host = HOST_ADDR,
        port = PORT
    )

def write_translation(translation: dict[dict, str]):
    pass

def init_db():
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    tables = cursor.fetchall()
    tables = tables[0] if tables else []
    logging.info(f"Tables present: {tables}")
    flag = False
    for t, v in TABLES.items():
        if t not in tables:
            cursor.execute(f"""
                CREATE TABLE {t} (
                    {v}
                )
            """)
            logging.info(f"{t} was missing so it was created.")
    conn.commit()
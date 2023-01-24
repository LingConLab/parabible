from pprint import pprint
import logging
import psycopg2 as db

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
}

DB_NAME = "parabible"
HOST_ADDR = "0.0.0.0"
PORT = "5432"

conn = db.connect(
        database = DB_NAME,
        user = "dev",
        password = "dev",
        host = HOST_ADDR,
        port = PORT
    )

def write_text_meta(meta: dict):
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO translations
            (
                lang_id, closest_iso_639_3, iso_15924,
                year_short, year_long,
                vernacular_title, english_title, url,
                copyright_short, copyright_long, notes
            ) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """,
        (
            2, meta["closest iso 639-3"], meta["iso_15924"],
            meta["year_short"], meta["year_long"],
            meta["vernacular_title"], meta["english_title"], meta["url"],
            meta["copyright_short"], meta["copyright_long"], meta["notes"]
        )
    )
    conn.commit()
    returned_id = cursor.fetchone()
    logging.debug(f"Inserted id: {returned_id}")

def write_text_data(data: list[dict]):
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
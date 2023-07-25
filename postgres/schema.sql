CREATE TABLE IF NOT EXISTS translations (
    id                  SERIAL PRIMARY KEY,
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
);

CREATE TABLE IF NOT EXISTS verses (
    book_id             INT NOT NULL,
    chapter_id          INT NOT NULL,
    verse_id            INT NOT NULL,
    translation_id      INT NOT NULL,
    PRIMARY KEY(book_id, chapter_id, verse_id, translation_id),

    line                TEXT
);

CREATE INDEX IF NOT EXISTS idx_translation_id ON verses (translation_id);
CREATE INDEX IF NOT EXISTS idx_book_id ON verses (book_id);
CREATE INDEX IF NOT EXISTS idx_chapter_id ON verses (chapter_id);

from json import load
from logging import getLogger
from pprint import pprint
from psycopg2.extensions import connection

from ._const import schema_file

logger = getLogger(__name__)

def execute_from_schema(conn: connection) -> None:
    """Reads schema sql file and executes it using `conn` connection"""
    cur = conn.cursor()
    with open(schema_file, 'r') as f:
        cur.execute(f.read())
    conn.commit()

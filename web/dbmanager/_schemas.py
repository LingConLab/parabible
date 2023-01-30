from json import load
from logging import getLogger

logger = getLogger(__name__)

from pathlib import Path
__data_dir_name = "data"
data_dir = Path(__file__).parent.joinpath(Path(__data_dir_name))

if not Path.exists(data_dir) or not Path.is_dir(data_dir):
    logger.critical(f"{data_dir} is invalid or missing")

file_name = "schemas.json"
file_path = data_dir.joinpath(file_name)
if not file_path.exists():
    logger.critical(f"{file_path} is missing")

table_schemas = None
with open(file_path, 'r', encoding="utf-8") as f:
    table_schemas = load(f)

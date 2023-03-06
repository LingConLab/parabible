from pathlib import Path
from json import load
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

# Section to edit
__data_dir_name = "data"
__iso_index_file_name = "iso_639-3_index.json"

# Funcs
def check_dir(dir_path):
    if not Path.exists(dir_path) or not Path.is_dir(dir_path):
        logger.critical(f"{dir_path} dir is invalid or missing")
        
def check_file(file_path, is_critical: bool, do_create_on_missing: bool) -> bool:
    """If `is_critical` then critical error. Else info and create file"""
    if not Path.exists(file_path) or not Path.is_file(file_path):
        if is_critical:
            logger.critical(f"{file_path} file is invalid or missing.")
            return False
        elif do_create_on_missing:
            with open(file_path, 'w'): pass
            if not Path.exists(file_path) or not Path.is_file(file_path):
                logger.warn(f"{file_path} file is invalid or missing. Creation attempt failed.")
                return False
            else:
                logger.info(f"{file_path} was created.")
                return True
        else:
            logger.warn(f"{file_path} file is invalid or missing.")
            return False
    else:
        return True

# Processing section
## Parent dir
parent_dir = Path(__file__).parent
data_dir = parent_dir.joinpath(Path(__data_dir_name))
check_dir(data_dir)
## Iso index file
__iso_index_file = data_dir.joinpath(__iso_index_file_name)
__iso_index_present = check_file(__iso_index_file, is_critical=False, do_create_on_missing=False)
if __iso_index_present:
    with open(__iso_index_file, 'r', encoding='utf-8') as f:
        __raw = load(f)
        __index_dict = defaultdict(lambda: "Unknown ISO 639-3 code")
        __index_dict.update(__raw)

def get_iso_lang_name(iso_code: str) -> str:
    if __iso_index_present:
        return __index_dict[iso_code]
    else:
        return iso_code
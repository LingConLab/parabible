from pathlib import Path
from typing import List, Union
from json import load
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Section to edit
__data_dir_name = "data"
__book_struct_file_name = "books_structure.json"
__iso_index_file_name = "iso_639-3_index.json"
__book_names_file_name = "book_names.json"

# Funcs
def check_dir(dir_path, create_if_missing=False, is_critical=False):
    if not Path.exists(dir_path) or not Path.is_dir(dir_path):
        if is_critical:
            logger.critical(f"{dir_path} dir is invalid or missing")
            raise FileNotFoundError(f"{dir_path} dir is invalid or missing")
        if create_if_missing:
            Path.mkdir(dir_path)
            logger.info(f"Created directory {dir_path}")
    else:
        logger.debug(f"Directory present {dir_path}")
        
def check_file(file_path, is_critical: bool, do_create_on_missing: bool) -> bool:
    """If `is_critical` then critical error. Else info and create file"""
    if not Path.exists(file_path) or not Path.is_file(file_path):
        if is_critical:
            logger.critical(f"{file_path} file is invalid or missing.")
            raise FileNotFoundError(f"{file_path} file is invalid or missing.")
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
        logger.debug("File present '{}'\nis_critical : {}\ncreate_on_missing : {}\npath : {}".format(
            file_path.name,
            is_critical,
            do_create_on_missing,
            file_path
        ))
        return True

# Processing section
## Directories
parent_dir = Path(__file__).parent
data_dir = parent_dir.joinpath(Path(__data_dir_name))
check_dir(data_dir, is_critical=True)

def load_dict_from_file(file_path, parent_dir=data_dir, is_critical=False, do_create_on_missing=False, convert_keys_to_int=False, default="Unknown") -> dict:
    file = parent_dir.joinpath(file_path)
    file_present = check_file(file, is_critical, do_create_on_missing)
    if file_present:
        with open(file, 'r', encoding='utf-8') as f:
            unprocessed = load(f)
            result_dict = defaultdict(lambda: default)
            result_dict.update(unprocessed)
            if convert_keys_to_int:
                result_dict = { int(k): v for k, v in result_dict.items() }
            return result_dict
    else:
        return None

## Iso names
__iso_index_dict = load_dict_from_file(__iso_index_file_name)

def get_iso_lang_name(iso_code: str) -> str:
    if __iso_index_dict:
        return __iso_index_dict[iso_code]
    else:
        return iso_code
    
## Book names
__book_names_dict = load_dict_from_file(__book_names_file_name, convert_keys_to_int=True)

def get_book_title(book_id: int) -> str:
    if __book_names_dict:
        return __book_names_dict[book_id]["title"]
    else:
        return book_id
    
def get_book_short_title(book_id: int) -> str:
    if __book_names_dict:
        return __book_names_dict[book_id]["abbreviation"]
    else:
        return book_id

def get_book_ids() -> List[int]:
    if __book_names_dict:
        return list(__book_names_dict.keys())
    else:
        return []

def get_book_abbrivs() -> dict:
    if __book_names_dict:
        return { k: v["abbreviation"] for k, v in __book_names_dict.items() }
    else:
        return None

## Books structure
book_struct_file = data_dir.joinpath(__book_struct_file_name)
__book_struct_dict = load_dict_from_file(__book_struct_file_name)

def get_chapters_ids(book_id: Union[str, int]) -> list:
    if __book_struct_dict:
        return list(__book_struct_dict[str(book_id)].keys())
    
def get_verses_ids(book_id: Union[str, int], chapter_id: Union[str, int]) -> list:
    if __book_struct_dict:
        return __book_struct_dict[str(book_id)][str(chapter_id)]

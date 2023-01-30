from os import listdir as os_listdir
from pathlib import Path
from re import match as regex_match, search as regex_search
from pprint import pprint
import logging

from .line_blacklist import blacklist

logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def __get_files(str_path) -> list[Path]:
    """Get all file names from inputed path

    Args:
        `rel_path` (str|Path): directory path

    Returns:
        list[Path]: list of all file paths in the directory
    """

    path = Path(str_path)
    file_names = os_listdir(path)
    return [path.joinpath(f) for f in file_names]

def __get_file_meta(file_name: str) -> str:
    """ Generator that cleans, fixes and yields meta line by line

    Args:
        `file_name` (str): file name

    Returns:
        Iterator[str]

    Yields:
        str: a meta data line
    """

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            final_line = line
            # meta string format check
            if not regex_match(r'# .*:', line):
                break
            # Problem №1 solving
            if regex_match(r'#\d{8}', line):
                final_line = line.removeprefix('#')
            yield final_line

def __get_file_lines(file_name: str) -> str:
    """ Generator that yields content lines one by one

    Args:
        `file_name` (str): file name

    Returns:
        Iterator[str]

    Yields:
        str: a content line
    """

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            yield line

def parse_file(file_name: Path, empty_value = None) -> dict[str, dict]:
    """ Get a dict of parsed data

    Args:
        `file_name` (Path): file name
        `empty_value` (Any, optional): The value to what empty values will be set. Defaults to None.

    Raises:
        AttributeError: If content line doesn't pass regex

    Returns:
        dict[str, dict]:    {
            'meta': dict,
            'data': dict,
        }
        
    Return short example:
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
    
    meta = {}
    data = {
        "lines": []
    }
    line_no = 0
    
    def check_blacklist(l):
        if l.strip() in blacklist:
            logger.debug(f"\nMet balcklisted line in {file_name} line: {line_no}\n{l}\n")
            return False
        return True
    
    for l in __get_file_meta(file_name=file_name):
        if not check_blacklist(l): continue
        line_no += 1
        try:
            key, val = l.replace('# ', '').split(':', maxsplit=1)
        except ValueError:
            logger.debug(f"Meta line cant be splitted. File: {file_name} Line:{l}")
            key = l.replace('# ', '').replace(':', '')
            val = ''
        # Problem №2 solving
        key = key.strip().lower(); val = val.strip()
        if val == '': val = empty_value
        meta[key] = val
        
    for l in __get_file_lines(file_name=file_name):
        if not check_blacklist(l): continue
        line_no += 1
        try:
            b_id, ch_id, vrs_id, line = regex_search(r'^(\d{2})(\d{3})(\d{3})\t(.*)$', l).groups()
        except AttributeError:
            try:
                b_id, ch_id, vrs_id = regex_search(r'^(\d{2})(\d{3})(\d{3})', l).groups()
            except AttributeError:
                raise AttributeError(f'Regex failed at line: {l.strip()}\nFile: {file_name}\nLine: {line_no}')
            finally:
                line = empty_value
        try:
            data["lines"].append({
                "book_id": int(b_id),
                "chapter_id": int(ch_id),
                "verse_id": int(vrs_id),
                "line": line
            })
        except ValueError:
            logger.debug(f"""Id is not int. Values are\n
                b_id:{b_id} ({type(b_id)})
                ch_id:{ch_id} ({type(ch_id)})
                vrs_id:{vrs_id} ({type(vrs_id)})
            """)
            
    return {
        'meta': meta,
        'data': data
    }

def parsed_texts(rel_path):
    """ Yields parsed data of the files in `rel_path` relative path

    Args:
        `rel_path` (str | Path): relative path to the file

    Yields:
        dict: see `parse_file()`
    """
    files = __get_files(rel_path)
    for f in files:
        yield parse_file(f), f.name

def main():
    unique = set()
    for f in __get_files():
        parse_file(f, unique)
    pprint(unique)

if __name__ == "__main__":
    main()

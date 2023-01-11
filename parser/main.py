from os import listdir as os_listdir
from pathlib import Path
from re import match as regex_match

from pprint import pprint

def get_files() -> list[Path]:
    """ Get all file names from curpus folder """

    relative_dir = "paralleltext-master/bibles/corpus/"
    current_dir = Path(__file__).parent.resolve()
    abs_dir = current_dir.joinpath(relative_dir)
    file_names = os_listdir(abs_dir)
    return [abs_dir.joinpath(f) for f in file_names]

def get_file_meta(file_name: str) -> str:
    """ Generator that cleans, fixes and yields meta line by line """

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

def get_file_lines(file_name: str) -> str:
    """ TODO """

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            yield line

def parse_file(file_name: str, unique: set):
    """ TODO """
    meta = {}
    for l in get_file_meta(file_name):
        try:
            key, val = l.replace('# ', '').split(':', maxsplit=1)
        except ValueError:
            print(f"Meta line cant be splitted. File: {file_name} Line:{l}")
            key = l.replace('# ', '').replace(':', '')
            val = ''
        # Problem №2 solving
        key = key.strip().lower(); val = val.strip()
        meta[key] = val
        unique.add(key)
    #pprint(meta)

def main():
    unique = set()
    for f in get_files():
        parse_file(f, unique)
    pprint(unique)

if __name__ == "__main__":
    main()

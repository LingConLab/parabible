from pprint import pprint
from time import time
from tqdm import tqdm

from src.parser import parsed_translations
from src.db_handler import init_db, write_text_meta

def temp_json_filler(np_dict: dict, f_name: str):
    from json import dump
    with open("bible_json/" + f_name.replace(".txt", ".json"), 'w', encoding='utf-8') as f:
        dump(np_dict, f, indent=2, ensure_ascii=False)

def main():
    pb = tqdm(unit=" lines", colour="pink", unit_scale=True)
    file_count = 0
    for p, f_name in parsed_translations('paralleltext-master/bibles/corpus/'):
        temp_json_filler(p, f_name)
        file_count += 1
        pb.update(len(p["data"]["lines"]))
        if file_count % 25 == 0: pb.set_postfix({'Files': file_count})
    init_db()
    
if __name__ == '__main__':
    main()
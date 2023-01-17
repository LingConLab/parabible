from pprint import pprint
from time import time
from tqdm import tqdm

from src.parser import parsed_translations
from src.db_handler import write_translation

def temp_json_filler(np_dict: dict):
    from json import dump
    with open("bible_json/" + np_dict["file_name"].replace(".txt", ".json"), 'w', encoding='utf-8') as f:
        dump(np_dict, f, indent=2)

def main():
    pb = tqdm(unit=" lines", colour="pink", unit_scale=True)
    file_count = 0
    for p in parsed_translations('paralleltext-master/bibles/corpus/'):
        if file_count > 2: break
        temp_json_filler(p)
        file_count += 1
        pb.update(len(p["data"]["lines"]))
        if file_count % 25 == 0: pb.set_postfix({'Files': file_count})
    
if __name__ == '__main__':
    main()
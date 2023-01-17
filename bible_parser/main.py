from src.parser import parsed
from pprint import pprint

def main():
    for p in parsed('paralleltext-master/bibles/corpus/'):
        pprint(p)
    
if __name__ == '__main__':
    main()
import os

def main():
    corp_dir = "paralleltext-master/bibles/corpus/"
    files = os.listdir(corp_dir)
    print(f"{len(files)} files")
    vers = set()
    langs = set()
    for i in range(len(files)):
        l, v = files[i].split("-x-")
        v = v.replace(".txt", "")
        vers.add(v)
        langs.add(l)
        
    print(f"{len(vers)} unique bible versions")
    print(f"{len(langs)} unique langs")

if __name__ == "__main__":
    main()

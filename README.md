# Overview
Consists of a flask python app and a postresql database. They exist in two different docker containers. Flask app refers to the DB via local network.

For a quick start run these:
<pre>
docker-compose up
python3 db_init.py
</pre>

# Docker handling shell/python scripts

These scripts help handle operations with docker.

~~Before running `docker-compose up` make sure to run `init` script first. This will launch docker container and parse and insert all the data into database.~~ (This isnt working for now)

* `db_init.py`
    * Parses data from *parser/paralleltext-matser/bibles/corpus/* to the database. You dont need to run itevery time you launch docker. Only on first launch or if you have updated curpus (the mentioned derectories). **Database docker container must be accessable and running!**
* `stop` sh script
    * stops all parabible's running containers
* `vipe` sh scrips
    * stops all parabible's running containers, deletes containers, deletes images
    * better use `stop` bc after `vipe` it will rebuild images (it takes some time). But if you want to be sure that everything is up to date then use `vipe`

~~*(Id like it to run automatically on postgres initialisation but I wasnt able to find python init scripts support)*~~

# Surface documentstion
## parser
Parses bible texts from [Michel Cysouw's repo](https://github.com/cysouw/multialignment-of-paralleltext) data into python dictionary that can be inserted into the DB. Now it saves parsed data as json files.

**TODO** handy script that inserts data into DB

## postgres
Contains docker files

## web
Flask web app, its docker files,

`dbmanager` module that provides access to the DB

***For the details see readme files in other dirs***


```
parabible
├─ .gitignore
├─ README.md
├─ compose.yml
├─ db_init.py
├─ init
├─ paralleltext-master
│  ├─ .gitignore
│  ├─ README.md
│  ├─ bibleParse.py
│  └─ bibles
│     ├─ bul-x-bible-newworld.txt
│     ├─ deu-x-bible-neue.txt
│     ├─ eng-x-bible-worldwide.txt
│     ├─ jpn-x-bible-newworld.txt
│     └─ pol-x-bible-newworld.txt
├─ postgres
│  ├─ Dockerfile
│  ├─ README.md
│  └─ env_file
├─ stop
├─ vipe
└─ web
   ├─ Dockerfile
   ├─ README.md
   ├─ app
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  ├─ static
   │  │  ├─ EBGaramond-Regular.ttf
   │  │  └─ style.css
   │  ├─ templates
   │  │  ├─ corpus.html
   │  │  ├─ home.html
   │  │  ├─ index.html
   │  │  └─ library.html
   │  └─ views.py
   ├─ dbmanager
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  ├─ _core.py
   │  ├─ _schemas.py
   │  ├─ data
   │  │  └─ schemas.json
   │  └─ parser
   │     ├─ README.md
   │     ├─ __init__.py
   │     ├─ __pycache__
   │     ├─ faced_problems.md
   │     ├─ line_blacklist.py
   │     └─ parser.py
   ├─ env_file
   ├─ requirements.txt
   └─ run.py

```
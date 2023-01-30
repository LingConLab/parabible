# Overview
Consists of a flask python app and a postresql database. They exist in two different docker containers. Flask app refers to the DB via local network.

For a quick start run these:
<code><br>
python3 db_init.py<br>
docker-compose up
</code>

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

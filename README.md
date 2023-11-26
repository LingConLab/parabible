# Quick start
Consists of a flask python app and a postresql database. They exist in two different docker containers. Flask app refers to the DB via local network.

For a quick start run these:
<pre>
docker compose up db

// here wait till you see "database system is ready to accept connections" for the second time. This means db is set up. (It says it one time, then runs init scripts, then restarts and tells it for the second time)
// then stop the container, press (Ctrl + C) one time

docker compose up -d
pip3 install -r requirements.txt

// Now we run population script. This will download the corpus and put it to the database. `full` mode puts all ~1800 translations (takes >1h). `debug` mode puts just 10 translations (takes <1min)

python3 populate_db.py -m full
</pre>

# Overview

Parabible is a project developed at HSE Moscow University that provides a user-friendly tool for working with a massive parallel bible translations corpus. It features a Flask web GUI and data storage in a PostgreSQL database, enabling users to easily access specific verses from specific translations and compare them side by side.

It consists of 1846 translations which are taken from [cysouw](https://github.com/cysouw). 

The latest version is hosted here : http://lingconlab.ru/parabible/

This project is present as 2 (3) connected docker containers.

 - python flask container
 - postgresql container
 - pgAdmin container (optional)

## postgres
*postgres/* Contains docker files and sql schema file for the postgres container.

## web
*web/* contains the actual web python flask app and docker files for the python flask container.

## pgadmin
Optional container to access the database admin panel. It may be disabled/enabled in *compose.yml* file in the `pgAdmin` section:
<pre>
pgAdmin:

    ...
    
    # !!!
    # COMMENT THIS TO ENABLE
    profiles:
      - donotstart
    # !!!
</pre>

***For the details see readme files in other dirs***

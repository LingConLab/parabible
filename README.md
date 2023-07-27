# Quick start
Consists of a flask python app and a postresql database. They exist in two different docker containers. Flask app refers to the DB via local network.

For a quick start run these:
<pre>
pip3 install wget tqdm psycopg2
docker compose up db -d
python3 populate_db.py -m full -p [database_port_here*]
docker compose up -d
</pre>
 \*you can find db port in [docker-compose.yml](docker-compose.yml) in `db` service. You will see ports: - port1:port2. You need port1, the first one.

# Overview

Parabible is a project developed at HSE Moscow University that provides a user-friendly tool for working with a massive parallel bible translations corpus. It features a Flask web GUI and data storage in a PostgreSQL database, enabling users to easily access specific verses from specific translations and compare them side by side.

It consists of 1846 translations which are taken from [cysouw](https://github.com/cysouw). 

The latest version is hosted here : http://lingconlab.ru/nginx_root/parabible/

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

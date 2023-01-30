## How to handle all this

~~Before running `docker-compose up` make sure to run `init` script first. This will launch docker container and parse and insert all the data into database.~~ (This isnt working for now)

* `docker-compose up`
    * starts python flask and postgresql containers
* `stop` sh script
    * stops all parabible's running containers
* `vipe` sh scrips
    * stops all parabible's running containers, deletes containers, deletes images
    * better use `stop` bc after `vipe` it will rebuild images (it takes some time). But if you want to be sure that everything is up to date then use `vipe`

~~*(Id like it to run automatically on postgres initialisation but I wasnt able to find python init scripts support)*~~

**:)**
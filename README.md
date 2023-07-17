# CRUK Data Engineer assignment
This is a ETL pipeline that fetch data from API loads it to a datalake, apply some transformations and load it to Postgres DB. Later some business analysis is performed on the DB to get business insights.


Below is the HLD of the ETL pipeline:

<img width="750" alt="hld" src="https://github.com/manojsairam008/Taxi-Rides-ETL/assets/139365266/8986b72c-8119-4c45-a10f-fe160fe8f039">


## Local SetUp

### Things you'll need to have installed for local setup

* Python 3.10 (possibly via [pyenv](https://github.com/pyenv/pyenv))
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* A container runtime such as [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* You may not need to install [docker-compose](https://github.com/docker/compose/releases) if you use Docker Desktop

Once your docker desktop is Up, run the below commands to execute the code
```
❯ docker build .
❯ docker-compose run --rm db
❯ docker-compose run --rm etl
```

## local setup tips

- You can create new tables by adding a `.sql` file inside `.initdb.d` folder and rebuilding the database
- You can rebuild the database by stopping and removing the container `docker-compose down -t0`

## General Instructions

> The entire pipeline is build in docker and uses docker resources
> The output of the sql query is saved in results.txt file having list of records [week_of_march, PULocationIds] 
> Data Analyst can customise the sql query (/src/resources/query.sql) and rerun the pipeline and can see their new results in same results.txt file

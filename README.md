# CRUK Data Engineer assignment
This is a ETL pipeline that fetch data from API loads it to a datalake, apply some transformations and load it to Postgres DB. Later some business analysis is performed on the DB to get business insights.
Below is the HLD of the ETL pipeline:
![plot](./Users/postmalone/Downloads/hld.png)



This is the technical exercise we use at CRUK to evaluate potential new candidate Data Engineers. It will allow 
you to demonstrate that you know how to: 

* Acquire and explore a dataset
* Ingest data
* Transform data
* Query data

Please read all the instructions below carefully and don’t hesitate to contact us if you have any queries.

As a Data Engineer, you shouldn't find this exercise to be particularly difficult. We're expecting a simple solution
that addresses only what is asked.

## Instructions

### Context
In this challenge, pretend that you are an Engineer working in a Data Engineering Team. You have been given the following user story to implement:

> As a data analyst
> 
> I want to query the [New York City Taxi cab Data Set](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
> 
> So that I can conveniently answer important business questions such as 
>
>    _"In each week for the month of March 2021, what are the top 5 Pick up locations (`PULocationID`) 
>    that result in trips which are slower than the average speed for a trip in the month 
>    (regardless of drop off and pick up locations)?"_

At CRUK, we mainly use Snowflake as our Data Warehouse, with technologies provided by AWS (e.g. Glue, S3 and Serverless databases like Aurora Postgres) for tasks such as orchestration and ingestion. We use infrastructure as code frameworks like AWS CDK (Cloud Development Kit) to create and maintain our AWS infrastructure. For this exercise we are ideally looking for an implementation that aligns with these technologies, but if you are more comfortable with other technologies on AWS, please feel free to use them. If you do not have access to AWS we have included a containerised version of PostgreSQL to allow you to perform the challenge on your local machine. This local setup includes:

* A working `docker-compose` file that has working sample Python code that connects to the postgres db and runs a piece of test SQL.
* A Python script to retrieve source data. We've used Python 3.10
* A `Pipenv` environment describing some dependencies 

We will not penalise your solution if you prefer to stick to the local setup, but please include notes in a README file explaining how you would move your workload into AWS, and some thoughts on how your implementation will scale. 

### Things you'll need to have installed for local setup

* Python 3.10 (possibly via [pyenv](https://github.com/pyenv/pyenv))
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* A container runtime such as [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* You may not need to install [docker-compose](https://github.com/docker/compose/releases) if you use Docker Desktop

### What we want you to do
If you are planning to use AWS, your Glue job should download the NYC Yellow taxi data set for March 2021
  (from [https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet) ). *Note that we only want the "Yellow" set, and for March 2021.*
* **INGEST AND TRANSFORM** Ingest the data set into an Aurora PostgreSQL instance, with the following considerations:
  * You should only ingest the columns needed to answer the question below (i.e. for the SQL query you will need to write)
  * You need to correct a known data quality issue where Location ID 161 and Location 237 have been accidentally swapped in the source system. *You need to renumber them correctly during the ingestion*.
* **QUERY** When the database is up and running and all the steps above have been executed, it should be possible to run a  
  SQL query (you can use the RDS query editor in the AWS console) against the ingested data set. Write a SQL query to answer the question above. i.e.

     > In each week for the month of March 2021, what are the top 5 Pick up locations (PULocationID) 
     that result in trips which are slower than the average trip speed in the whole month 
     (regardless of drop off and pick up locations)?
  
     Make a note of the result of the query in a file called `results.txt` in the root of the repository.

     Note that, in answering this question, you will need to calculate the average speed of a trip from the existing columns. *You should
     discard any invalid rows which would make the calculation invalid.*

If you are using the local setup, change the docker-compose file and provide (new and modified existing) Python scripts so that,
on running the container (via a `docker-compose run <yourservicenamehere>` command) PostgreSQL should start up in the container and you will then need to download and ingest the data as described above


## What we're looking for
Things we value in your solution are:
* _Self-explanatory code_ – the solution must speak for itself. Multiple paragraphs explaining the solution are a sign that it isn’t straightforward enough to understand purely by reading the code. Also, you should ensure your code is correctly formatted and lints cleanly.
* _Tests_ – the solution must be well tested (possibly using a test-first approach).
* _Simplicity_ – We value simplicity as an architectural virtue and a development practice. Solutions should reflect the difficulty of the assigned task, and should NOT be overly complex. Layers of abstraction, patterns, or architectural features that aren’t called for should NOT be included.

Your solution needs to include:

1. Instructions about your strategy and important decisions you made. Provide these as a markdown file.
2. The document in (1) should also answer the following questions:
* How did you meet the needs of the data analyst described in the user story?
* How did you ensure data quality?
* What would need to change for the solution scale to work with a 1TiB dataset with new data arriving each day?
3. Your submission should be a zip file containing your solution and the requested documentation, or a link to your Github respository.
4. Your submission needs to contain everything we need to run the code (scripts etc.)
5. If you are using AWS, please include your infrastructure as code (either AWS CDK code or cloudformation template)

## What happens after this?
We hope you'll succeed in this phase! If you do, you proceed to the next phase, in which we'll arrange an interview
where we are expecting you to run us through your solution, demonstrating it from your device. You'll show it running, and walk us 
through your solution while we discuss any choices that you made and provide feedback.

Apart from the exercise, we'll have a conversation about your experience, and you'll 
let us know in detail your past challenges and your future expectations.

*Good Luck!*

## local setup

Basic setup with bootstrapping PostgreSQL with a sample table and querying it.

```
❯ docker build .
❯ docker-compose run --rm db
❯ docker-compose run --rm etl
```

## local setup tips

- You can create new tables by adding a `.sql` file inside `.initdb.d` folder and rebuilding the database
- You can rebuild the database by stopping and removing the container `docker-compose down -t0`


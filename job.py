from enum import Enum

import requests
from tqdm import tqdm
import pandas as pd
import io
import pyarrow.parquet as pq
import os
import logging
import psycopg
from retry.api import retry_call
import src.ingest.extract as extract
import src.transform.transform as transform
import src.resources.conf as config
import src.utils.pythonUtilis as pyutils
import src.utils.postgresUtils as dbutils


def ingestion():
    year = 2021
    month = 3
    taxi_color = "yellow"
    output_path = config.api_output_path
    logging.info("Fetching Api Results")

    # Fetch data from API and write to output path as parquet
    extract.fetch_api_data(year, month, taxi_color, output_path)


def transformation_analysis():
    output_path = config.api_output_path
    query_path = config.sql_query_path
    write_sql_path = config.analysis_results_path
    db_args = config.db_args_list
    table_name = config.postgres_table

    # Create postgres connection
    db_connnection = dbutils.create_connection(db_args)
    cur = db_connnection.cursor()

    print("Transformation started..")
    # Read the api data, transform it and returns a transformed list
    transformed_list = transform.transformation(output_path)

    print("Loading to postgres started..")
    # Load the transformed data to postgres table
    transform.load_to_postgres(cur, transformed_list, table_name)

    # Execute SQL query for data analysis
    print("Data Analysis in Postgres..")
    sql_query = pyutils.read_file(query_path)
    transform.load_query_results(cur, sql_query, write_sql_path)

    logging.info("Loading successful")


if __name__ == "__main__":
    # Extract the data and load it to datalake
    print("Starting Ingestion...")
    ingestion()

    # Transform the data from datalake and load it to postgres
    print("Starting Transformation...")
    transformation_analysis()

    logging.info("ETL FINISHED...")

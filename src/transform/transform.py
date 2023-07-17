import pandas as pd
import requests
from tqdm import tqdm
import pandas as pd
import io
import pyarrow.parquet as pq
import os
import logging
import psycopg
from retry.api import retry_call
import src.utils.pythonUtilis as pyutils
import src.resources.conf as config


def transformation(output_filename):
    '''
    Read data from datalake (docker container), apply required transformation
    :param output_filename: path of output data from ingestion
    :return: list of transformed data
    '''
    logging.info("Creating pandas df of parquet dataset....")
    trip_df = pd.read_parquet(output_filename, engine='fastparquet')

    df_col_list = config.trip_table_col_list
    trip_df = trip_df[df_col_list]
    trip_df["tpep_pickup_datetime"] = trip_df["tpep_pickup_datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    trip_df["tpep_dropoff_datetime"] = trip_df["tpep_dropoff_datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    transformed_trip_list = trip_df.values.tolist()
    return transformed_trip_list


def load_to_postgres(cur, list_data, table_name):
    '''
    Laod data to postgres
    :param db_connnection: postgres db connection
    :param list_data: data to be loaded to postgres
    :param table_name: name of postgres table
    :return:
    '''
    logging.info("Creating cursor...")
    logging.info("Inserting data to postgres table...")
    data_to_load = [tuple(l) for l in list_data]

    # Single Inserts
    '''
    for record in list_data:
        record_value = pyutils.convert_list_to_string(record)
        sql_query = "INSERT INTO {} VALUES ({})".format(table_name, record_value)
        cur.execute(sql_query)     
    '''
    # Bulk Inserts
    sql_query_bulk_inserts = "INSERT INTO {} (VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, trip_distance, PULocationID) VALUES (%s, %s, %s, %s, %s)".format(table_name)
    cur.executemany(sql_query_bulk_inserts, data_to_load)



def load_query_results(cur, sql_query, write_sql_path):
    '''
    Run sql query for data analysis and insert results to result.txt file
    :param db_connnection: postgres db connection
    :param sql_query: sql query for data analysis
    :param write_sql_path: path where output data is written
    '''
    query_result_lst = []
    cur.execute(sql_query)
    for row in cur:
        query_result_lst.append(row)

    # Writing Query results to result.txt
    pyutils.write_file(str(query_result_lst), write_sql_path)




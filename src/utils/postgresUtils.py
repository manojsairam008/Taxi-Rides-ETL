import requests
from tqdm import tqdm
import pandas as pd
import io
import pyarrow.parquet as pq
import os
import logging
import psycopg
from retry.api import retry_call


def create_connection(db_args):
    '''
    Creating db connection
    :param db_args:
    :return: connection
    '''
    try:
        conn = retry_call(
            psycopg.connect,
            fargs=db_args,
            tries=10,
            delay=1,
        )
        return conn
    except Exception as e:
        print(e)
        return None

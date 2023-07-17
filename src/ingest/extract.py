from enum import Enum

import requests
from tqdm import tqdm
import pandas as pd
import io
import pyarrow.parquet as pq
import os
import logging
import psycopg
import src.utils.pythonUtilis as pyutils


def fetch_api_data(year: int, month: int, taxi_type: str, output_filename: str):
    '''
    Fetching data from API and saving results to output path
    '''
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{pyutils._filename_for_date(year, month, taxi_type)}"
    logging.info(f"Fetching dataset at {url}")
    response = requests.get(url)
    logging.info(f"API response code: {response}")
    if response.status_code == 200:
        # Save the data to a file.
        with open(output_filename, "wb") as f:
            data = response.content
            logging.info("Writing data to {}".format(output_filename))
            f.write(data)
            logging.info("Writing data finised")
    else:
        print("Error getting data: " + response.status_code)



# DB details
postgres_table = "trip"

# Path
api_output_path = '/home/etl/yellow_tripdata_2021-03.parquet'
sql_query_path = '/mnt/scripts/src/resources/query.sql'
analysis_results_path = '/mnt/scripts/results.txt'


trip_table_col_list = ['VendorID','tpep_pickup_datetime','tpep_dropoff_datetime','trip_distance','PULocationID']
db_args_list = ["host=db port=5432 dbname=postgres user=postgres password=postgres"]
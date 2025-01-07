#!/usr/bin/env python
# coding: utf-8

import os 
import argparse 
from sqlalchemy import create_engine
import pandas as pd

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_name = 'output.parquet'

    # download the parquet
    os.system(f"wget {url} -O {parquet_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    data = pd.read_parquet(parquet_name, engine="fastparquet")

    data.tpep_pickup_datetime = pd.to_datetime(data.tpep_pickup_datetime)
    data.tpep_dropoff_datetime = pd.to_datetime(data.tpep_dropoff_datetime)

    
    data.to_sql(name='table_name', con=engine, if_exists='replace')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest parquet data to postgres')

    parser.add_argument('--user', help="username for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="table name where we will write the results to")
    parser.add_argument('--url', help="url of the parquet")

    args = parser.parse_args()
    main(args)

# !wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

# !pip install fastparquet
# !pip install pyarrow

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
    table_name2 = params.table_name2
    url = params.url
    url2 = params.url2

    csv_name = 'output.csv'
    parquet_name = 'output.parquet'

    # download the csv
    os.system(f"wget {url} -O {csv_name}")
    os.system(f"wget {url2} -O {parquet_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    data = pd.read_csv(csv_name)
    data2 = pd.read_parquet(parquet_name, engine="fastparquet")

    data2.tpep_pickup_datetime = pd.to_datetime(data2.tpep_pickup_datetime)
    data2.tpep_dropoff_datetime = pd.to_datetime(data2.tpep_dropoff_datetime)

    
    data.to_sql(name=table_name, con=engine, if_exists='replace')
    data2.to_sql(name=table_name2, con=engine, if_exists='replace')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data to postgres')

    parser.add_argument('--user', help="username for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="table name where we will write the results to")
    parser.add_argument('--table_name2', help="table name two where we will write the results to")
    parser.add_argument('--url', help="url of the csv")
    parser.add_argument('--url2', help="url of the parquet")

    args = parser.parse_args()
    main(args)


# !wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
# !wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
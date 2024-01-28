import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    tablename = params.tablename
    url = params.url

    file_name = 'output.csv'

    os.system(f'wget {url} -O {file_name}')
 
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    taxi_data_iter = pd.read_csv(file_name,compression='gzip',iterator=True,chunksize=100000)

    taxi_data = next(taxi_data_iter)

    taxi_data['tpep_pickup_datetime'] = pd.to_datetime(taxi_data['tpep_pickup_datetime'])
    taxi_data['tpep_dropoff_datetime'] = pd.to_datetime(taxi_data['tpep_dropoff_datetime'])

    taxi_data.columns = [column.upper() for column in taxi_data.columns]

    taxi_data.head(n=0).to_sql(name=tablename,con=engine,if_exists='replace')

    taxi_data.to_sql(name=tablename, con=engine, if_exists='append')

    while True:
        try:
            start_time = time()

            taxi_data = next(taxi_data_iter)

            taxi_data['tpep_pickup_datetime'] = pd.to_datetime(taxi_data['tpep_pickup_datetime'])
            taxi_data['tpep_dropoff_datetime'] = pd.to_datetime(taxi_data['tpep_dropoff_datetime'])

            taxi_data.columns = [column.upper() for column in taxi_data.columns]

            taxi_data.to_sql(name=tablename,con=engine,if_exists='append')

            end_time = time()

            print(f"Time Taken to Process each Chunk: {end_time - start_time}")
        
        except StopIteration as e:
            print('Data Load Has been Completed Successfully')
            exit('Program Completed Successfully')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV Data to Postgres')

    parser.add_argument('--user',help='User Name of the Postgres Server')
    parser.add_argument('--password',help='Password of the Postgres Server')
    parser.add_argument('--host',help='Host of the Postgres Server')
    parser.add_argument('--port',help='Port of the Postgres Server')
    parser.add_argument('--database',help='Data Base of the Postgres Server')
    parser.add_argument('--tablename',help='Name of the Table where you will write the resuts to')
    parser.add_argument('--url',help='URL of the CSV File')

    args = parser.parse_args()
    main(args)
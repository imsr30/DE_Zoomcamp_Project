import pandas as pd
from sqlalchemy import create_engine
from time import time

taxi_data_iter = pd.read_csv('Week_1/2_Docker_SQL/yellow_tripdata_2021-01.csv',iterator=True,chunksize=100000)

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# taxi_data = next(taxi_data_iter)

# taxi_data['tpep_pickup_datetime'] = pd.to_datetime(taxi_data['tpep_pickup_datetime'])
# taxi_data['tpep_dropoff_datetime'] = pd.to_datetime(taxi_data['tpep_dropoff_datetime'])

# taxi_data.columns = [column.upper() for column in taxi_data.columns]

# taxi_data.head(n=0).to_sql(name='YELLOW_TAXI_DATA',con=engine,if_exists='replace')

while True:
    start_time = time()

    taxi_data = next(taxi_data_iter)

    taxi_data['tpep_pickup_datetime'] = pd.to_datetime(taxi_data['tpep_pickup_datetime'])
    taxi_data['tpep_dropoff_datetime'] = pd.to_datetime(taxi_data['tpep_dropoff_datetime'])

    taxi_data.columns = [column.upper() for column in taxi_data.columns]

    taxi_data.to_sql(name='YELLOW_TAXI_DATA',con=engine,if_exists='append')

    end_time = time()

    print(f"Time Taken to Process each Chunk: {end_time - start_time}")
import datetime

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def push_postgres(df):
    # set today's date for the create_date column timestamp
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # pre-ingestion renaming and type refactoring
    df['create_date'] = today
    df.rename({'ip': 'masked_ip', 'device_id': 'masked_device_id'}, axis=1, inplace=True)
    df['create_date'] = pd.to_datetime(df['create_date'], infer_datetime_format=True)


    table_name = 'user_logins'
    # run the DDL in case the table doesn't exist
    ddl_statement = '''CREATE TABLE IF NOT EXISTS user_logins(
                        user_id varchar(128),
                        device_type varchar(32),
                        masked_ip varchar(256),
                        masked_device_id varchar(256),
                        locale varchar(32),
                        app_version varchar(5),
                        create_date date);'''

    # setup credentials for connection
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='booty'
    )

    cursor = conn.cursor()
    # execute the ddl statement to generate the table if it doesn't exist
    cursor.execute(ddl_statement)

    conn.commit()

    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

    # ingest the dataframe of masked SQS messages into the database
    df.to_sql(table_name, engine, if_exists='append', index=False)

    conn.close()

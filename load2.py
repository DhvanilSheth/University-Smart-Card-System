import mysql.connector
from sqlalchemy import create_engine

def load(df, host, user, password, database="UniDB", table_name="integrated_data"):
    # Create a connection to the database
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()

    # Drop existing tables in UniDB (Be cautious with this step)
    cursor.execute("DROP DATABASE IF EXISTS UniDB")
    cursor.execute("CREATE DATABASE UniDB")
    cursor.execute("USE UniDB")

    connection.commit()

    # SQLAlchemy engine for Pandas
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}', echo=False)

    # Load data into the new table
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    cursor.close()
    connection.close()
    print("Data Loaded into UniDB Warehouse")
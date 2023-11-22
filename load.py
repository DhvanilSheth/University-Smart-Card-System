import mysql.connector
from sqlalchemy import create_engine

def load(dfs, host, user, password, database="UniDB"):
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
    # table_names = {0:"integrated_data"}
    table_names = {0:"sports_data", 1:"hostel_data", 2:"mess_data", 3:"admin_data", 4:"access_data", 
                   5:"sports_data1", 6:"hostel_data1", 7:"mess_data1", 8:"admin_data1", 9:"access_data1",
                   10:"sports_data2", 11:"hostel_data2", 12:"mess_data2", 13:"admin_data2", 14:"access_data2"}
    for df in range(len(dfs)):
        dfs[df].to_sql(name=table_names[df], con=engine, if_exists='replace', index=False)

    cursor.close()
    connection.close()
    print("Data Loaded into UniDB Warehouse")
import mysql.connector
import pandas as pd
import json

def insert_data_from_csv(table_name, csv_path, connection):
    df = pd.read_csv(csv_path)
    df.columns = [col.replace(" ", "_") for col in df.columns]
    data_columns_escaped = ", ".join([f"`{col}`" for col in df.columns])
    values = [tuple(row) for row in df.values]
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO `{table_name}` ({data_columns_escaped}) VALUES ({placeholders})"
    cursor = connection.cursor()
    try:
        cursor.executemany(insert_query, values)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data into {table_name}: {err}")
        connection.rollback()
    finally:
        cursor.close()

def create_db_and_tables(db_name, tables, host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

<<<<<<< HEAD
# Connect to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)
cursor = connection.cursor()

# For each database and its tables defined in the config file
for db_name, table_infos in config_data.items():
=======
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
>>>>>>> 959a77ceced6c531e035c2ca0537d90c39cf4ec7
    cursor.execute(f"USE {db_name}")

    for table_info in tables:
        columns = ", ".join([f"{header['Name']} {header['Type']}" for header in table_info["headers"]])
        primary_keys = ", ".join(table_info["primary_key"])
        create_command = f"""
        CREATE TABLE IF NOT EXISTS {table_info['table']} (
            {columns},
            PRIMARY KEY ({primary_keys})
        )
        """
        cursor.execute(create_command)

        if table_info["insert"]:
            insert_data_from_csv(table_info["table"], table_info["path"], connection)

    cursor.close()
    connection.close()

def run_from_config(host, user, password):
    with open("data_sources_config.json", "r") as f:
        configs = json.load(f)
        for config in configs:
            create_db_and_tables(config["db_name"], config["tables"], host, user, password)

run_from_config('localhost', 'root', 'akis@123')


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

def drop_table_if_exists(table_name, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    except mysql.connector.Error as err:
        print(f"Error dropping table {table_name}: {err}")
    finally:
        cursor.close()

def create_db_and_tables(db_name, tables, host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    
    for table_config in tables:
        table_name = table_config["table"]
        headers = table_config["headers"]
        primary_key = table_config["primary_key"]
        
        if table_config["insert"]:
            columns = ", ".join([f"{header['Name']} {header['Type']}" for header in headers])
            primary_key_str = ", ".join(primary_key)
            create_command = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns},
                PRIMARY KEY ({primary_key_str})
            )
            """
            cursor.execute(create_command)
            insert_data_from_csv(table_name, table_config["path"], connection)
        else:
            drop_table_if_exists(table_name, connection)

    cursor.close()
    connection.close()

def run_from_config(host, user, password):
    with open("data_sources_config.json", 'r') as file:
        configs = json.load(file)
    
    for config in configs:
        create_db_and_tables(config["db_name"], config["tables"], host, user, password)

run_from_config('localhost', 'root', 'akis@123')

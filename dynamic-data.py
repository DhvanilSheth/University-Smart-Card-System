import mysql.connector
import pandas as pd
import json

# Read the configuration file
with open('data_sources_config.json', 'r') as config_file:
    tables_data = json.load(config_file)

# Connect to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="akis@123",
)

cursor = connection.cursor()

# Create the databases dynamically from the configuration file
for table_info in tables_data:
    table_name = table_info['table']
    csv_path = table_info['path']
    db_name = table_info['db_name']
    headers = table_info['headers']
    
    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    # Create table if it doesn't exist
    columns_definitions = ', '.join([f"{header['Name'].replace(' ', '_')} {header['Type']}" for header in headers])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {db_name}.{table_name} ({columns_definitions})"
    cursor.execute(create_table_query)

    # Read CSV and insert data
    df = pd.read_csv(csv_path)
    columns = df.columns.tolist()
    values = df.values.tolist()

    for value_set in values:
        insert_query = f"INSERT IGNORE INTO {db_name}.{table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
        cursor.execute(insert_query, tuple(value_set))
    
    connection.commit()

cursor.close()
connection.close()

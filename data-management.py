import mysql.connector
import pandas as pd
import json
import os

config_file_path = 'data_sources_config.json'

with open(config_file_path, 'r') as file:
    config_data = json.load(file)

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)
cursor = connection.cursor()

def synchronize_table(db_name, table_name, csv_path, headers, primary_keys):
    cursor.execute(f"USE {db_name}")
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print(f"Table {db_name}.{table_name} does not exist. Skipping...")
        return
    
    csv_data = pd.read_csv(csv_path)
    columns = ', '.join([header['Name'] for header in headers])
    cursor.execute(f"SELECT {columns} FROM {table_name}")
    db_data = pd.DataFrame(cursor.fetchall(), columns=[header['Name'] for header in headers])
    merged_data = pd.merge(csv_data, db_data, on=primary_keys, how='outer', indicator=True)
    to_insert = merged_data[merged_data['_merge'] == 'left_only'].drop(columns='_merge')
    to_update = merged_data[(merged_data['_merge'] == 'both') & (merged_data.filter(like='_x').ne(merged_data.filter(like='_y')).any(axis=1))]
    to_delete = merged_data[merged_data['_merge'] == 'right_only'].drop(columns='_merge')
    
    if not to_insert.empty:
        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.executemany(insert_query, to_insert.to_numpy().tolist())
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows into {db_name}.{table_name}")
    
    for index, row in to_update.iterrows():
        set_clause = ', '.join([f"{header['Name']} = %s" for header in headers])
        where_clause = ' AND '.join([f"{key} = '{row[key]}'" for key in primary_keys])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(update_query, row.filter(like='_x').tolist())
        connection.commit()
        print(f"Updated 1 row in {db_name}.{table_name}")
    
    for index, row in to_delete.iterrows():
        where_clause = ' AND '.join([f"{key} = '{row[key]}'" for key in primary_keys])
        delete_query = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(delete_query)
        connection.commit()
        print(f"Deleted 1 row from {db_name}.{table_name}")

for db in config_data:
    db_name = db['db_name']
    for table in db['tables']:
        if table['insert']:
            synchronize_table(db_name, table['table'], table['path'], table['headers'], table['primary_key'])

cursor.close()
connection.close()

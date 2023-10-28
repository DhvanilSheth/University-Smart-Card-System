import mysql.connector
import pandas as pd
import json

def clean_df_columns(df):
    """Sanitize DataFrame column names by replacing spaces with underscores."""
    df.columns = [col.replace(" ", "_") for col in df.columns]
    return df

# Read the configuration file
with open('data_sources_config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Connect to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="akis@123",
)
cursor = connection.cursor()

# For each database and its tables defined in the config file
for db_name, table_infos in config_data.items():
    cursor.execute(f"USE {db_name}")

    for table_info in table_infos:
        # Extract table details from the configuration
        table_name = table_info['table']
        csv_path = table_info['path']
        headers = table_info['headers']

        # Construct the CREATE TABLE query
        columns_definitions = ', '.join([f"{header['Name'].replace(' ', '_')} {header['Type']}" for header in headers])
        primary_keys = ', '.join([pk.replace(' ', '_') for pk in table_info['primary_key']])
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_definitions},
                PRIMARY KEY ({primary_keys})
            )
        """
        cursor.execute(create_table_query)

        # Read CSV and insert data
        df = pd.read_csv(csv_path)
        df = clean_df_columns(df)
        columns = df.columns.tolist()
        values = df.values.tolist()

        for value_set in values:
            insert_query = f"INSERT IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            cursor.execute(insert_query, tuple(value_set))

        connection.commit()

cursor.close()
connection.close()

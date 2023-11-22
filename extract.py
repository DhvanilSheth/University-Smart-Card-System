import mysql.connector
import json
import pandas as pd

with open('data_sources_config.json', 'r') as file:
    data_config = json.load(file)

def query_db(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def extract_table_data(connection, table_name, headers):
    columns = ", ".join([header["Name"] for header in headers])
    query = f"SELECT {columns} FROM {table_name}"
    data = query_db(connection, query)
    return pd.DataFrame(data, columns=[header["Name"] for header in headers])

def extract_db_data(host, user, password, db_name, tables):
    connection = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    dfs = {}
    for table in tables:
        dfs[table["table"]] = extract_table_data(connection, table["table"], table["headers"])
    connection.close()
    return dfs

def extract(localhost, username, password):
    sports_dfs = extract_db_data(localhost, username, password, "SportsDB", data_config[0]["tables"])
    mess_dfs = extract_db_data(localhost, username, password, "MessDB", data_config[1]["tables"])
    hostel_dfs = extract_db_data(localhost, username, password, "HostelDB", data_config[2]["tables"])
    admin_dfs = extract_db_data(localhost, username, password, "AdminDB", data_config[3]["tables"])
    access_dfs = extract_db_data(localhost, username, password, "AccessDB", data_config[4]["tables"])
    
    print("Data Extraction Complete")
    return sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs
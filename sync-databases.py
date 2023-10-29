import mysql.connector
import pandas as pd
import json

def synchronize_databases(host, user, password):
    with open("databases.json", 'r') as file:
        expected_databases = json.load(file)

    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("USE UniDB")
    cursor.execute("SELECT Name FROM localDBs")
    current_databases_in_UniDB = {record[0] for record in cursor.fetchall()}

    for db, db_type in expected_databases.items():
        if db not in current_databases_in_UniDB:
            print(f"Adding {db} to UniDB.")
            cursor.execute("SELECT IFNULL(MAX(Sr_No), 0) + 1 FROM localDBs")
            next_sr_no = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO localDBs (Sr_No, Name, Type) VALUES (%s, %s, %s)", (next_sr_no, db, db_type))

    for db in current_databases_in_UniDB:
        if db not in expected_databases:
            print(f"Removing {db} from UniDB.")
            cursor.execute(f"DELETE FROM localDBs WHERE Name = %s", (db,))

    cursor.execute("SHOW DATABASES")
    all_databases = {record[0] for record in cursor.fetchall()}
    for db in expected_databases:
        if db not in all_databases:
            print(f"Creating database {db} in MySQL.")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")

    for db in all_databases:
        if db not in expected_databases and db not in {'mysql', 'information_schema', 'performance_schema', 'sys', 'UniDB'}:
            print(f"Dropping database {db} from MySQL.")
            cursor.execute(f"DROP DATABASE IF EXISTS {db}")

    connection.commit()
    cursor.close()
    connection.close()

synchronize_databases('localhost', 'root', 'hanoon2002')

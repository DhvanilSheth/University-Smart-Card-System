import os
import pandas as pd
import mysql.connector
import json

UNIQUE_KEY_CONFIGURATION = {
    'pool': ['Roll No', 'Sr No'],
    'pool_non_membership': ['Roll No', 'In_Time', 'Date'],
    'medicine_sports': ['Contact No', 'Time', 'Date'],
    'gym': ['Roll No', 'In_Time', 'Date'],
    'equipment_requests': ['Roll No', 'In_Time', 'Date'],
    'equipment_loss': ['Roll No', 'Time', 'Date'],
    'mess_1_data': ['Roll No', 'Sr No'],
    'mess_2_data': ['Roll NO', 'Sale ID'],
    'home_leave_data': ['Roll No', 'Out Time', 'Date'],
    'hostel_data': ['Roll No', 'Sr No'],
    'medicine_data': ['Contact', 'Time', 'Date'],
    'package_collection_data': ['Pick Up Student Number', 'Driver Contact', 'Sr No']
}

csv_dir = './Data/'

def create_uniDB(host, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS UniDB")
        cursor.execute("USE UniDB")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS localDBs (
                Sr_No INT,
                Name VARCHAR(255),
                Type VARCHAR(255)
            )
        """)
        insert_data = [
            (1, 'SportsDB', 'Sports'),
            (2, 'HostelDB', 'Hostel'),
            (3, 'MessDB', 'Mess')
        ]
        cursor.executemany("INSERT INTO localDBs (Sr_No, Name, Type) VALUES (%s, %s, %s)", insert_data)
        connection.commit()
        print("UniDB set up complete")
        
        data_dict = {
            'HostelDB': 'Hostel',
            'SportsDB': 'Sports',
            'MessDB': 'Mess'
        }
        with open('databases.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print("Data written to 'databases.json'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            

def clean_dbs(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    databases = ["SportsDB", "HostelDB", "MessDB", "UniDB"]
    for db in databases:
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {db}")
        except mysql.connector.Error as err:
            print(f"Error dropping {db}: {err}")
    cursor.close()
    connection.close()
    print("Databases cleaned.")

def process_csv(db, csv_file):
    df = pd.read_csv(csv_file)
    unique_key = UNIQUE_KEY_CONFIGURATION.get(db)
    df['Unique_Key'] = df.apply(lambda row: '_'.join([str(row[col]) for col in unique_key]), axis=1)
    df['Key_Combination'] = ':'.join([col.replace(" ", "_") for col in UNIQUE_KEY_CONFIGURATION.get(db)])
    df['LookUp_Count'] = 0
    df['Update_Count'] = 0
    df.to_csv(csv_file, index=False)

def delete_duplicates(csv_file):
    df = pd.read_csv(csv_file)
    df.drop_duplicates(subset=['Unique_Key'], keep='first', inplace=True)
    df.to_csv(csv_file, index=False)

def clean_data(csv_file):
    df = pd.read_csv(csv_file)
    df.dropna(subset=[col for col in df.columns if not df[col].dtype == 'O'], inplace=True)
    df.dropna(subset=[col for col in df.columns if df[col].dtype == 'O'], how='any', inplace=True)
    df.to_csv(csv_file, index=False)
    

clean_dbs('localhost', 'root', 'akis@123')
create_uniDB('localhost', 'root', 'akis@123')

allowed_csv_names = set(UNIQUE_KEY_CONFIGURATION.keys())

for root, dirs, files in os.walk(csv_dir):
    for file in files:
        db_name = file[:-4]  
        if db_name in allowed_csv_names:
            csv_file = os.path.join(root, file)
            process_csv(db_name, csv_file)
            delete_duplicates(csv_file)
            clean_data(csv_file)

print("Data Transformation Complete")
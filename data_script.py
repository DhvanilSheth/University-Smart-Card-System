# pip install pandas mysql-connector-python
# import pandas as pd
# import mysql.connector

# def makeSportsDB(host, user, password):
#     # Connect to the MySQL server
#     connection = mysql.connector.connect(host=host, user=user, password=password)
#     cursor = connection.cursor()
    
#     # Create the "SportsDB" database
#     cursor.execute("CREATE DATABASE IF NOT EXISTS SportsDB")
#     cursor.execute("USE SportsDB")
    
#     # Define the create table commands

    
#     # Create tables
#     for command in create_commands.values():
#         cursor.execute(command)
    
#     # Insert data from CSV files into tables
#     csv_files = [
#         "./Data/pool_non_membership.csv",
#         "./Data/pool.csv",
#         "./Data/gym.csv",
#         "./Data/equipment_requests.csv",
#         "./Data/equipment_loss.csv",
#         "./Data/medicine_sport.csv"
#     ]
    
#     for csv_file in csv_files:
#         table_name = csv_file.split("/")[-1].replace(".csv", "")
        
#         data = pd.read_csv(csv_file)
#         data_columns = ", ".join([col.replace(" ", "_") for col in data.columns])
        
#         for index, row in data.iterrows():
#             values = tuple(row)
#             insert_query = f"INSERT INTO {table_name} ({data_columns}) VALUES {values}"
#             cursor.execute(insert_query)
    
#     connection.commit()
#     cursor.close()
#     connection.close()
    
#     return "SportsDB and tables created successfully and data inserted!"

# makeSportsDB(host='localhost', user='root', password='root')


import mysql.connector
import pandas as pd

def insert_data_from_csv(table_name, csv_path, connection):
    df = pd.read_csv(csv_path)
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

def makeSportsDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS SportsDB")
    cursor.execute("USE SportsDB")
    
    create_commands = {
        "pool_non_membership": """
        CREATE TABLE IF NOT EXISTS pool_non_membership (
            Date DATE,
            Name VARCHAR(255),
            Tax_ID INT,
            Payment INT,
            Roll_No INT,
            In_Time TIME,
            Sign VARCHAR(255)
        )
        """,
        "pool": """
        CREATE TABLE IF NOT EXISTS pool (
            Sr_No INT,
            Card_Number INT,
            Membership_Expiry DATE,
            Name VARCHAR(255),
            Roll_No INT,
            Sex VARCHAR(10),
            Department VARCHAR(50),
            Presence BOOLEAN
        )
        """,
        "gym": """
        CREATE TABLE IF NOT EXISTS gym (
            Date DATE,
            Name VARCHAR(255),
            Roll_No INT,
            Room_No VARCHAR(10),
            Contact BIGINT,
            In_Time TIME,
            Out_Time TIME,
            Signature VARCHAR(255)
        )
        """,
        "equipment_requests": """
        CREATE TABLE IF NOT EXISTS equipment_requests (
            Date DATE,
            Name VARCHAR(255),
            Roll_No INT,
            Room_No VARCHAR(10),
            Contact BIGINT,
            Equipment_Issued VARCHAR(255),
            Quantity INT,
            In_Time TIME,
            Out_Time TIME,
            Signature VARCHAR(255),
            Remarks TEXT
        )
        """,
        "equipment_loss": """
        CREATE TABLE IF NOT EXISTS equipment_loss (
            Date DATE,
            Name VARCHAR(255),
            Roll_No INT,
            Room_No VARCHAR(10),
            Contact BIGINT,
            Equipment VARCHAR(255),
            Time TIME,
            Remarks TEXT
        )
        """,
        "medicine_sport": """
        CREATE TABLE IF NOT EXISTS medicine_sport (
            Date DATE,
            Time TIME,
            Name VARCHAR(255),
            Contact_No INT,
            Quantity INT,
            Medicine_Name VARCHAR(255),
            Student_Sign VARCHAR(255),
            Security_Sign VARCHAR(255)
        )
        """
    }
    
    for command in create_commands.values():
        cursor.execute(command)
    
    csv_files = {
        "pool_non_membership": "./Data/pool_non_membership.csv",
        "pool": "./Data/pool.csv",
        "gym": "./Data/gym.csv",
        "equipment_requests": "./Data/equipment_requests.csv",
        "equipment_loss": "./Data/equipment_loss.csv",
        "medicine_sport": "./Data/medicine_sport.csv"
    }
    
    try:
        for table_name, csv_file in csv_files.items():
            insert_data_from_csv(table_name, csv_file, connection)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        connection.close()

    return "SportsDB and tables created successfully and data inserted!"

# Example usage
makeSportsDB(host='localhost', user='root', password='root')

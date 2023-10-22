import mysql.connector
import pandas as pd

def insert_data_from_csv(table_name, csv_path, connection):
    df = pd.read_csv(csv_path)
    df.columns = [col.replace(" ", "_") for col in df.columns]
    data_columns_escaped = ", ".join([f"`{col}`" for col in df.columns])
    values = [tuple(row) for row in df.values]
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO `{table_name}` ({data_columns_escaped}) VALUES ({placeholders})"
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    for value in values:
        try:
            cursor.execute(insert_query, value)
            connection.commit()
        except mysql.connector.IntegrityError:
            print(f"Duplicate entry {value} for table {table_name}. Skipping.")
            continue
    # cursor.executemany(insert_query, values)
    connection.commit()
    cursor.close()

def set_primary_key(cursor, table_name, primary_key_column):
    cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key_column});")

def makeSportsDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS SportsDB")
    cursor.execute("USE SportsDB")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pool_non_membership (
            Date DATE,
            Name VARCHAR(255),
            Tax_ID INT,
            Payment INT,
            Roll_No INT,
            In_Time TIME,
            Sign VARCHAR(255)
        )
    """)
    cursor.execute("""
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
    """)
    cursor.execute("""
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
    """)
    cursor.execute("""
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
    """)
    cursor.execute("""
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
    """)
    cursor.execute("""
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
    """)
    csv_files = {
        "pool_non_membership": "./Data/pool_non_membership.csv",
        "pool": "./Data/pool.csv",
        "gym": "./Data/gym.csv",
        "equipment_requests": "./Data/equipment_requests.csv",
        "equipment_loss": "./Data/equipment_loss.csv",
        "medicine_sport": "./Data/medicine_sport.csv"
    }
    for table_name, csv_file in csv_files.items():
        insert_data_from_csv(table_name, csv_file, connection)
    set_primary_key(cursor, "pool", "Roll_No")
    set_primary_key(cursor, "gym", "Roll_No")
    set_primary_key(cursor, "equipment_requests", "Roll_No")
    set_primary_key(cursor, "equipment_loss", "Roll_No")
    cursor.close()
    connection.close()

def makeHostelDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS HostelDB")
    cursor.execute("USE HostelDB")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS home_leave_data (
            Date DATE,
            Name VARCHAR(255),
            Contact BIGINT,
            Out_Time TIME,
            Roll_No INT,
            Room_No VARCHAR(10),
            To_Address VARCHAR(255),
            Return_Time TIME,
            Return_Date DATE,
            Signature VARCHAR(255),
            Security_Signature VARCHAR(255)
        ) 
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostel_data (
            Sr_No INT,
            Room_Type VARCHAR(50),
            Floor VARCHAR(50),
            Room_No VARCHAR(10),
            Student_Name VARCHAR(255),
            Roll_No INT,
            Course_Type VARCHAR(50),
            Year VARCHAR(50),
            Email_ID VARCHAR(255),
            Fees INT,
            Security_Amt INT,
            Bank_ID INT,
            Contact BIGINT,
            Remarks TEXT,
            From_Date DATE,
            To_Date DATE,
            Name_Share VARCHAR(255),
            Roll_No_Share INT,
            Course_Share VARCHAR(50),
            Year_Share VARCHAR(50),
            Email_ID_Share VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicine_data (
            Date DATE,
            Name VARCHAR(255),
            Contact BIGINT,
            Medicine_Name VARCHAR(255),
            Quantity INT,
            Room_No VARCHAR(10),
            Time TIME,
            Roll_No INT,
            Signature VARCHAR(255),
            Purpose VARCHAR(255),
            Security_Signature VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS package_collection_data (
            Date DATE,
            Name VARCHAR(255),
            Room VARCHAR(50),
            Delivery_Driver_Name VARCHAR(255),
            Driver_Contact BIGINT,
            Company VARCHAR(255),
            Quantity INT,
            Student_Who_Picks_It VARCHAR(255),
            Above_Person_Number BIGINT,
            Signature VARCHAR(255),
            Security_Signature VARCHAR(255)
        )
    """)
    csv_files = {
        "home_leave_data": "./Data/home_leave_data.csv",
        "hostel_data": "./Data/hostel_data.csv",
        "medicine_data": "./Data/medicine_data.csv",
        "package_collection_data": "./Data/package_collection_data.csv"
    }
    for table_name, csv_file in csv_files.items():
        insert_data_from_csv(table_name, csv_file, connection)
    set_primary_key(cursor, "home_leave_data", "Roll_No")
    set_primary_key(cursor, "hostel_data", "Roll_No")
    set_primary_key(cursor, "medicine_data", "Roll_No")
    cursor.close()
    connection.close()

def makeMessDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS MessDB")
    cursor.execute("USE MessDB")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mess_1_data (
            Sr_No INT,
            Name VARCHAR(255),
            Phone_Number BIGINT,
            Roll_No INT,
            Cash DECIMAL(10, 2),
            PayTM DECIMAL(10, 2),
            Total DECIMAL(10, 2),
            Date_of_Purchase DATE,
            Breakfast DECIMAL(10, 2),
            Lunch DECIMAL(10, 2),
            Snack DECIMAL(10, 2),
            Dinner DECIMAL(10, 2)
        ) 
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mess_2_data (
            Sale_ID INT,
            Sale_Date DATE,
            Coupon_Type VARCHAR(255),
            Name VARCHAR(255),
            Phone_Number BIGINT,
            Roll_NO INT,
            Paytm DECIMAL(10, 2),
            Cash DECIMAL(10, 2),
            Total_Amount DECIMAL(10, 2)
        )
    """)
    csv_files = {
        "mess_1_data": "./Data/mess_1_data.csv",
        "mess_2_data": "./Data/mess_2_data.csv"
    }
    for table_name, csv_file in csv_files.items():
        insert_data_from_csv(table_name, csv_file, connection)
    set_primary_key(cursor, "mess_1_data", "Roll_No")
    set_primary_key(cursor, "mess_2_data", "Roll_No")
    cursor.close()
    connection.close()

def run(localhost, username, password):
    makeSportsDB(localhost, username, password)
    makeHostelDB(localhost, username, password)
    makeMessDB(localhost, username, password)

def alter_primary_keys(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

    # List of commands to alter primary keys
    commands = [
        # SportsDB
        ("USE SportsDB;",),
        ("ALTER TABLE pool DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE pool_non_membership DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE medicine_sport DROP PRIMARY KEY, ADD PRIMARY KEY(Contact_No, Time, Date);",),
        ("ALTER TABLE gym DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_requests DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_loss DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Time, Date);",),

        # MessDB
        ("USE MessDB;",),
        ("ALTER TABLE mess1 DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE mess2 DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sale_ID);",),

        # HostelDB
        ("USE HostelDB;",),
        ("ALTER TABLE home_leave_data DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Out_Time, Date);",),
        ("ALTER TABLE hostel_data DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE medicine_data DROP PRIMARY KEY, ADD PRIMARY KEY(Contact, Time, Date);",),
        ("ALTER TABLE package_collection DROP PRIMARY KEY, ADD PRIMARY KEY(Student_Contact, Driver_Contact, Sr_No);",)
    ]

    for command in commands:
        try:
            cursor.execute(*command)
        except mysql.connector.Error as err:
            print(f"Error executing {command}: {err}")

    cursor.close()
    connection.close()

run('localhost', 'root', 'root')

alter_primary_keys('localhost', 'root', 'root')
# pip install pandas mysql-connector-python

import mysql.connector

def makeSportsDB(host, user, password):
    # Connect to the MySQL server
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    
    # Create the "SportsDB" database
    cursor.execute("CREATE DATABASE IF NOT EXISTS SportsDB")
    cursor.execute("USE SportsDB")
    
    # Define the create table commands
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
    
    # Create tables
    for command in create_commands.values():
        cursor.execute(command)
    
    # Insert data from CSV files into tables
    csv_files = [
        "./data/pool_non_membership.csv",
        "./data/pool.csv",
        "./data/gym.csv",
        "./data/equipment_requests.csv",
        "./data/equipment_loss.csv",
        "./data/medicine_sport.csv"
    ]
    
    for csv_file in csv_files:
        table_name = csv_file.split("/")[-1].replace(".csv", "")
        
        data = pd.read_csv(csv_file)
        data_columns = ", ".join([col.replace(" ", "_") for col in data.columns])
        
        for index, row in data.iterrows():
            values = tuple(row)
            insert_query = f"INSERT INTO {table_name} ({data_columns}) VALUES {values}"
            cursor.execute(insert_query)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return "SportsDB and tables created successfully and data inserted!"

makeSportsDB(host='192.168.32.187', user='sa', password='wasd456fgA')
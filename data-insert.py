import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
IP = os.getenv("IP")
USER = os.getenv("USERNAME")
PASS = os.getenv("PASSWORD")

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

def execute_create_commands(cursor, create_commands):
    for create_command in create_commands.values():
        cursor.execute(create_command)

def makeSportsDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS SportsDB")
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
        "medicine_sports": """
        CREATE TABLE IF NOT EXISTS medicine_sports (
            Date DATE,
            Time TIME,
            Name VARCHAR(255),
            Contact_No BIGINT,
            Quantity INT,
            Medicine_Name VARCHAR(255),
            Student_Sign VARCHAR(255),
            Security_Sign VARCHAR(255)
        )
        """
    }

    execute_create_commands(cursor, create_commands)

    csv_files = {
        "pool_non_membership": "./Data/pool_non_membership.csv",
        "pool": "./Data/pool.csv",
        "gym": "./Data/gym.csv",
        "equipment_requests": "./Data/equipment_requests.csv",
        "equipment_loss": "./Data/equipment_loss.csv",
        "medicine_sports": "./Data/medicine_sports.csv"
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

def makeHostelDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS HostelDB")
    cursor.execute("CREATE DATABASE IF NOT EXISTS HostelDB")
    cursor.execute("USE HostelDB")

    create_commands = {
        "home_leave_data": """
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
        """,
        "hostel_data": """
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
        """,
        "medicine_data": """
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
        """,
        "package_collection_data": """
        CREATE TABLE IF NOT EXISTS package_collection_data (
            Sr_No INT,
            Date DATE,
            Name VARCHAR(255),
            Room VARCHAR(50),
            Delivery_Driver_Name VARCHAR(255),
            Driver_Contact BIGINT,
            Company VARCHAR(255),
            Quantity INT,
            Pick_Up_Student VARCHAR(255),
            Pick_Up_Student_Number BIGINT,
            Signature VARCHAR(255),
            Security_Signature VARCHAR(255)
        )
        """
    }

    execute_create_commands(cursor, create_commands)

    csv_files = {
        "home_leave_data": "./Data/home_leave_data.csv",
        "hostel_data": "./Data/hostel_data.csv",
        "medicine_data": "./Data/medicine_data.csv",
        "package_collection_data": "./Data/package_collection_data.csv"
    }

    try:
        for table_name, csv_file in csv_files.items():
            insert_data_from_csv(table_name, csv_file, connection)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        connection.close()

    return "HostelDB and tables created successfully and data inserted!"

def makeMessDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS MessDB")
    cursor.execute("CREATE DATABASE IF NOT EXISTS MessDB")
    cursor.execute("USE MessDB")

    create_commands = {
        "mess_1_data": """
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
        """,
        "mess_2_data": """
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
        """
    }

    execute_create_commands(cursor, create_commands)

    csv_files = {
        "mess_1_data": "./Data/mess_1_data.csv",
        "mess_2_data": "./Data/mess_2_data.csv"
    }

    try:
        for table_name, csv_file in csv_files.items():
            insert_data_from_csv(table_name, csv_file, connection)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        connection.close()

    return "MessDB and tables created successfully and data inserted!"

def makeAdminDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS AdminDB")
    cursor.execute("CREATE DATABASE IF NOT EXISTS AdminDB")
    cursor.execute("USE AdminDB")

    create_student_information_table = """
    CREATE TABLE IF NOT EXISTS Student_Information (
        Name VARCHAR(255),
        Roll_No VARCHAR(255) PRIMARY KEY,
        Contact_No VARCHAR(255),
        Email_ID VARCHAR(255),
        Course VARCHAR(255),
        Gender VARCHAR(50)
    )
    """

    cursor.execute(create_student_information_table)

    try:
        insert_data_from_csv("Student_Information", "./Data/student_information.csv", connection)
    except Exception as e:
        print(f"An error occurred while inserting data into Student_Information: {str(e)}")
    finally:
        cursor.close()
        connection.close()

    return "AdminDB and Student_Information table created successfully and data inserted!"

def makeAccessDB(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS AccessDB")
    cursor.execute("CREATE DATABASE IF NOT EXISTS AccessDB")
    cursor.execute("USE AccessDB")

    create_access_logs_table = """
    CREATE TABLE IF NOT EXISTS Access_Logs (
        Sr_No INT,
        Roll_No VARCHAR(255),
        Name VARCHAR(255),
        Building VARCHAR(255),
        Room VARCHAR(255),
        In_Time TIME,
        Out_Time TIME,
        In_Date DATE,
        Out_Date DATE
    )
    """

    cursor.execute(create_access_logs_table)

    try:
        insert_data_from_csv("Access_Logs", "./Data/access_logs.csv", connection)
    except Exception as e:
        print(f"An error occurred while inserting data into Access_Logs: {str(e)}")
    finally:
        cursor.close()
        connection.close()

    return "AccessDB and Access_Logs table created successfully and data inserted!"

def data_insertion(localhost, username, password):
    makeSportsDB(localhost, username, password)
    makeHostelDB(localhost, username, password)
    makeMessDB(localhost, username, password)
    makeAdminDB(localhost, username, password)
    makeAccessDB(localhost, username, password)
    print("Data insertion into all databases and tables completed!")
    
data_insertion(IP, USER, PASS)
# pip install pandas mysql-connector-python

import pandas as pd
import mysql.connector

# MySQL connection parameters
db_params = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root' ,
    'password': 'root'
}

# A dictionary mapping databases to their respective tables and CSV files
db_table_files = {
    'Sports': [
        ('equipment_loss', 'Data/equipment_loss.csv'),
        ('equipment_requests', 'Data/equipment_requests.csv'),
        ('gym', 'Data/gym.csv'),
        ('pool', 'Data/pool.csv'),
        ('pool_non_membership', 'Data/pool_non_membership.csv'),
        ('medicine_sport', 'Data/medicine_sport.csv')
    ],
    'Mess': [
        ('mess_1', 'Data/mess_1.csv'),
        ('mess_2', 'Data/mess_2.csv')
    ],
    'Hostel': [
        ('home_leave_data', 'Data/home_leave_data.csv'),
        ('hostel_data', 'Data/hostel_data.csv'),
        ('medicine_data', 'Data/medicine_data.csv'),
        ('package_collection_data', 'Data/package_collection_data.csv')
    ]
}

# # Connect to MySQL
# conn = mysql.connector.connect(**db_params)

# # Create a cursor object
# cursor = conn.cursor()

# # Loop through each database, table, and file
# for db, tables_files in db_table_files.items():

#     # If the database doesn't exist, create it
#     cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db};')
#     # Use the appropriate database
#     cursor.execute(f'USE {db};')
#     cursor.execute(f'CREATE TABLE IF NOT EXISTS equipment_loss(Date      DATE  NOT NULL PRIMARY KEY,Name      VARCHAR(255) NOT NUL,Roll_No   INTEGER  NOT NULL,Room_No   VARCHAR(5) NOT NULL,Contact   VARCHAR(10) NOT NULL,Equipment VARCHAR(255) NOT NULL,Time      VARCHAR(5) NOT NULL,Remarks   VARCHAR(255) NOT NULL);')
#     cursor.execute(f'CREATE TABLE IF NOT EXISTS equipment_requests(Date             DATE  NOT NULL PRIMARY KEY,Name             VARCHAR(255) NOT NULL,Roll_No          INTEGER  NOT NULL,Room_No          VARCHAR(5) NOT NULL,Contact          VARCHAR(10) NOT NULL,Equipment_Issued VARCHAR(12) NOT NULL,Quantity         INTEGER  NOT NULL,In               VARCHAR(5) NOT NULL,Out              VARCHAR(5) NOT NULL,Signature        VARCHAR(25) NOT NULL,Remarks          VARCHAR(255) NOT NULL);')
#     # cursor.execute(f'')
#     # Loop through each table and file
#     for table, file in tables_files:
#         # Read the CSV file into a DataFrame, skipping the first row
#         df = pd.read_csv(file, skiprows=1)
        
#         # Convert DataFrame columns to a format suitable for MySQL insertion
#         columns_str = ', '.join(df.columns)
#         values_str = ', '.join(['%s'] * len(df.columns))
        
#         # Form the insertion query
#         insert_query = f'INSERT INTO {table} ({columns_str}) VALUES ({values_str});'
        
#         # Loop through DataFrame rows and insert them into the MySQL table
#         for _, row in df.iterrows():
#             cursor.execute(insert_query, tuple(row))
        
#         # Commit the transaction
#         conn.commit()

# # Close the cursor and connection
# cursor.close()
# conn.close()

def create_database_and_tables(db_table_files):
    for db_name, tables in db_table_files.items():
        # Create a SQLite database
        conn = sqlite3.connect(f'{db_name}.db')
        cursor = conn.cursor()

        for table_name, csv_filename in tables:
            # Read the CSV file to determine the table schema
            with open(csv_filename, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)

            # Create the table with dynamic schema
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{header} TEXT' for header in headers])})"
            cursor.execute(create_table_query)

            # Insert data from CSV into the table
            with open(csv_filename, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    placeholders = ', '.join(['?'] * len(row))
                    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    cursor.execute(insert_query, row)

        # Commit and close the database connection
        conn.commit()
        conn.close()

create_database_and_tables(db_table_files)
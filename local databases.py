# pip install pandas mysql-connector-python

import pandas as pd
import mysql.connector

# MySQL connection parameters
db_params = {
    'host': 'Saggitarius',
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

# Connect to MySQL
conn = mysql.connector.connect(**db_params)

# Create a cursor object
cursor = conn.cursor()

# Loop through each database, table, and file
for db, tables_files in db_table_files.items():
    # Use the appropriate database
    cursor.execute(f'USE {db};')
    
    # Loop through each table and file
    for table, file in tables_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        
        # Convert DataFrame columns to a format suitable for MySQL insertion
        columns_str = ', '.join(df.columns)
        values_str = ', '.join(['%s'] * len(df.columns))
        
        # Form the insertion query
        insert_query = f'INSERT INTO {table} ({columns_str}) VALUES ({values_str});'
        
        # Loop through DataFrame rows and insert them into the MySQL table
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
        
        # Commit the transaction
        conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

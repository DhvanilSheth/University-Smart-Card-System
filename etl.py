import mysql.connector

def alter_primary_keys(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

    dbs_tables_keys = {
        'SportsDB': {
            'pool': ['Roll_No', 'Sr_No'],
            'pool_non_membership': ['Roll_No', 'In_Time', 'Date'],
            'medicine_sports': ['Contact_No', 'Time', 'Date'],
            'gym': ['Roll_No', 'In_Time', 'Date'],
            'equipment_requests': ['Roll_No', 'In_Time', 'Date'],
            'equipment_loss': ['Roll_No', 'Time', 'Date']
        },
        'MessDB': {
            'mess_1_data': ['Roll_No', 'Sr_No'],
            'mess_2_data': ['Roll_No', 'Sale_ID']
        },
        'HostelDB': {
            'home_leave_data': ['Roll_No', 'Out_Time', 'Date'],
            'hostel_data': ['Roll_No', 'Sr_No'],
            'medicine_data': ['Contact', 'Time', 'Date'],
            'package_collection_data': ['Pick_Up_Student_Number', 'Driver_Contact', 'Sr_No']
        }
    }

    for db, tables in dbs_tables_keys.items():
        cursor.execute(f"USE {db};")
        for table, keys in tables.items():
            combined_keys = ", ".join(keys)
            try:
                cursor.execute(f"ALTER TABLE {table} ADD PRIMARY KEY ({combined_keys});")
            except mysql.connector.Error as err:
                print(f"Error executing command on table {table}: {err}")

    cursor.close()
    connection.close()

alter_primary_keys('localhost', 'root', 'akis@123')
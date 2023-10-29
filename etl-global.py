import mysql.connector
import json

def create_uniDB(host, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS UniDB")
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

create_uniDB("localhost", "root", "hanoon2002")
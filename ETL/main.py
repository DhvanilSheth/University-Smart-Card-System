import subprocess
import mysql.connector


def CleanDBs(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    databases = ["SportsDB", "HostelDB", "MessDB"]
    for db in databases:
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {db}")
        except mysql.connector.Error as err:
            print(f"Error dropping {db}: {err}")
    cursor.close()
    connection.close()
    print("Databases cleaned.")


CleanDBs('localhost', 'root', 'root')
subprocess.run(['python', 'extract.py'])
subprocess.run(['python', 'transform.py'])
subprocess.run(['python', 'load.py'])
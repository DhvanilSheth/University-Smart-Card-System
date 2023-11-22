import time
import sys
import shutil
import subprocess
import os
import csv
import json
from tabulate import tabulate
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
IP = os.getenv("DB_IP")
USER = os.getenv("DB_USERNAME")
PASS = os.getenv("DB_PASSWORD")

DYNAMIC_DATA = 'dynamic-data.py'
ETL_EXTRACT = 'extract.py'
ETL_LOAD = 'load.py'
ETL_TRANSFORM = 'transform.py'
ETL_GLOBAL = 'etl-global.py'
SYNC_DB = 'sync-databases.py'
DATA_GEN = 'data-gen.py'
DATA_INSERT = 'data-insert.py'

DATABASES = {
    1: "SportsDB",
    2: "MessDB",
    3: "HostelDB"
}
PRIMARY_KEY_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]
HEADER_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]
SOURCES = [["Source1", "Database1"], ["Source2", "Database2"], ["Source3", "Database3"]]  
RED = "\033[91m"
GREEN = "\033[92m"
NORMAL = "\033[0m"
BLUE = "\033[94m"

def deleteRow(table_name, serial_number):
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'UniDB'
    }

    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor()
        query = f"DELETE FROM {table_name} WHERE Sr_No = {serial_number}"
        cursor.execute(query)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def getRows(table_name):
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'UniDB'
    }

    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()
        
def getRollNo():
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'AdminDB'
    }
    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor()
        query = "SELECT Roll_No FROM Student_Information"
        cursor.execute(query)
        roll_numbers = [result[0] for result in cursor.fetchall()]
        return roll_numbers
    finally:
        cursor.close()
        connection.close()
        
def getTableData(table_name):
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'UniDB'
    }

    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {table_name}")
        table_data = cursor.fetchall()
        headers = [row['Field'] for row in table_data]
        types = [row['Type'] for row in table_data]

        return headers, types

    finally:
        cursor.close()
        connection.close()
        
def insertData(table_name, data):
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'UniDB'
    }
    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT MAX(Sr_No) FROM {table_name}")
        max_sr_no = cursor.fetchone()[0]
        next_sr_no = max_sr_no + 1 if max_sr_no is not None else 1
        columns = ", ".join(data.keys())
        values = ", ".join("'"+str(value)+"'" for value in data.values())
        query = f"INSERT INTO {table_name} (Sr_No, {columns}) VALUES ({next_sr_no}, {values})"
        print(query)
        cursor.execute(query)
        connection.commit()
        print(f"Data inserted successfully with Sr_No: {next_sr_no}")

    finally:
        cursor.close()
        connection.close()
        
def getStudentInfo(roll_no):
    db_config = {
        'host': IP,
        'user': USER,
        'password': PASS,
        'database': 'AdminDB'
    }
    connection = mysql.connector.connect(**db_config)
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM Student_Information WHERE Roll_No = {roll_no}"
        cursor.execute(query)
        student_info = cursor.fetchone()
        return student_info
    finally:
        cursor.close()
        connection.close()


def format(item, char1='*'):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width - 4
    item_with_margin = f"{char1} {item.ljust(box_width)} {char1}"
    return item_with_margin

def print_progress_bar(segments, completed):
    terminal_width, _ = shutil.get_terminal_size()
    bar_length = terminal_width - len("Progression: ") - 2
    completed_blocks = int(bar_length * (completed / segments))
    remaining_blocks = bar_length - completed_blocks
    progress_bar = f"[{GREEN}{'#' * completed_blocks}{RED}{'-' * remaining_blocks}{NORMAL}]"
    indentation = ' ' * len("Progression: ")
    print(f"{'.' * terminal_width}")
    sys.stdout.write(f"\rProgression: {progress_bar}\n")
    sys.stdout.flush()
    print(f"{'.' * terminal_width}")
    print()
    return segments == completed

def display_error_card(error_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    error_text = f"{RED}ERROR: {error_message}\n"
    top_border = f"{RED}{'*' * box_width}"
    bottom_border = f"{RED}{'*' * box_width}"
    print(top_border)  
    line = f"{RED}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border)  
    print(NORMAL) 

def display_success_card(success_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    error_text = f"{GREEN}SUCCESS: {success_message}\n"
    top_border = f"{GREEN}{'*' * box_width}"
    bottom_border = f"{GREEN}{'*' * box_width}"
    print(top_border)  
    line = f"{GREEN}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border) 
    print(NORMAL)  
    
def display_title_card(title_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    error_text = f"{BLUE}{title_message}\n"
    top_border = f"{BLUE}{'*' * box_width}"
    bottom_border = f"{BLUE}{'*' * box_width}"
    print(top_border) 
    line = f"{BLUE}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border) 
    print(NORMAL)  

def display_boxed_text(text, char1='*', char2='*', char3='*', margin=1):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin
    text_lines = text.split("\n")
    top_border = f"{char1 * box_width}"
    bottom_border = f"{char1 * box_width}"
    print(top_border)  
    for line in text_lines:
        if line.startswith("*"):
            line = f"{char1}{' ' * (box_width - 2 * left_margin - len(line) + 3)}{line.strip().lstrip('*').rstrip('*').strip()} {char1}"
        else:
            line = f"{char1}{line.strip().center(box_width - 2 * left_margin)}{char1}"
        print(line)
    print(bottom_border) 

def display_menu(char1='*', margin=5):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin

    menu = [
        "* 1. Application",
        "* 2. Settings",
        "* 3. Exit"
    ]

    for item in menu:
        item_with_margin = f"{item.ljust(box_width - 2 * left_margin - 4)} *"
        print(item_with_margin) 
    print() 

def display_settings_menu(char1='*', margin=5):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin

    menu = [
        "* 1. Insert New Entry to Table",
        "* 2. Delete Entry from Table",
        "* 3. Insert Table to Database",
        "* 4. Delete Table from Database",
        "* 5. Insert New Database",
        "* 6. Delete New Database",
        "* 7. Run Data-Gen and Data-Insert",
        "* 10. Exit",
    ]

    for item in menu:
        item_with_margin = f"{item.ljust(box_width - 2 * left_margin - 4)} *"
        print(item_with_margin) 
    print() 
    
def display_application_menu(char1='*', margin=5):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin

    menu = [
        "* 1. Student Performance and Wellness Analysis",
        "* 2. Financial Management and Billing",
        "* 3. Student Identity Profile",
        "* 4. Mess Meal Tracking",
        "* 5. Student Sports Inventory Management",
        "* 6. Hostel Facilities Usage",
        "* 7. Sports Facility Usage",
        "* 8. Student Access Tracking",
        "* 9. Exit"
    ]

    for item in menu:
        item_with_margin = f"{item.ljust(box_width - 2 * left_margin - 4)} *"
        print(item_with_margin) 
    print() 
    
def insert_new_data(json_data, json_file_path):
    completed = 0
    segments = 5
    text = "Insert New Data\n\n"
    print_progress_bar(segments, completed)

    db_index = int(input("Select Database:\n1. SportsDB\n2. MessDB\n3. HostelDB\nEnter the index: ")) - 1
    if db_index < 0 or db_index > 2:
        print("Invalid database. Try again.")
        return

    db_name = DATABASES[db_index + 1]
    completed += 1
    print_progress_bar(segments, completed)

    print(format(f"{db_name} Chosen"))
    table_name = input("Give a name for the new source: ")
    table_name = "_".join(table_name.split())
    completed += 1
    print_progress_bar(segments, completed)

    headers = []
    primary_key = []

    header_index = 0
    while True:
        insert_header = input("Do you want to Insert New Header [Y/N]? ")
        if insert_header.lower() != "y":
            if not headers:
                display_error_card("Enter at least one HEADER")
                return
            else:
                break

        header_name = input("Header Name: ")
        header_name = "_".join(header_name.split())

        header_type = None
        while header_type is None:
            print("Header Types:")
            for idx, header_type_option in enumerate(HEADER_TYPES):
                print(f"{idx}. {header_type_option}")

            header_type_choice = input("Select a header type by index: ")
            if header_type_choice.isdigit():
                header_type_choice = int(header_type_choice)
                if 0 <= header_type_choice < len(HEADER_TYPES):
                    header_type = HEADER_TYPES[header_type_choice]
                    print(f"Header {header_index}: {header_name} ({header_type})")
                    headers.append({"Name": header_name, "Type": header_type})
                    header_index += 1
                else:
                    print("Invalid index. Try again.")
            else:
                print("Invalid input. Enter the index to choose a header type.")

    completed += 1
    print_progress_bar(segments, completed)

    while not primary_key:
        print("Select primary key columns from the following headers by their index:")
        for idx, header in enumerate(headers):
            print(f"{idx}: {header['Name']} ({header['Type']})")

        primary_key_input = input("Enter the indices of the primary key columns (e.g., '0 2'). Enter 'Done' when finished: ")

        if primary_key_input.lower() == "done":
            if primary_key:
                break
            else:
                print("Please select at least one column as the primary key.")
                continue

        primary_key_indices = [int(idx) for idx in primary_key_input.split() if idx.isdigit()]

        for idx in primary_key_indices:
            if 0 <= idx < len(headers):
                primary_key.append(headers[idx])

    completed += 1
    print_progress_bar(segments, completed)
    
    data_to_insert = "Data to insert:\n"
    data_to_insert += f"Database: {db_name}\n"
    data_to_insert += f"Table: {table_name}\n"
    data_to_insert += "Headers:\n"
    for header in headers:
        data_to_insert += f"- {header['Name']} ({header['Type']})\n"
    data_to_insert += "Primary Key:\n"
    for key in primary_key:
        data_to_insert += f"- {key['Name']} ({key['Type']})\n"

    print(data_to_insert)
    
    insert_confirm = input("Proceed with insertion [Y/N]? ")
    if insert_confirm.lower() == "y":
        new_data_source = {
            'table': table_name,
            'insert': False, 
            'path': f"./Data/{table_name}.csv",
            'headers': headers,
            'primary_key': [key['Name'] for key in primary_key]
        }
        json_data[db_index]['tables'].append(new_data_source)
        with open(json_file_path, 'w') as f:
            json.dump(json_data, f, indent=2)

        csv_file_path = f"./Data/{table_name}.csv"
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[header['Name'] for header in headers])
                writer.writeheader()
        
        display_boxed_text("Data inserted successfully")
        completed += 1
        print_progress_bar(segments, completed)

    else:
        display_boxed_text("Data insertion canceled")
        completed += 1
        print_progress_bar(segments, completed)
        
def get_sources(insert_value=True):
    with open("data_sources_config.json", "r") as f:
        configs = json.load(f)

    return [(table["table"], db["db_name"]) for db in configs for table in db["tables"] if table["insert"] == insert_value]

def toggle_source_insert(source, db_name, insert_value):
    with open("data_sources_config.json", "r") as f:
        configs = json.load(f)

    for config in configs:
        if config["db_name"] == db_name:
            for table in config["tables"]:
                if table["table"] == source:
                    table["insert"] = insert_value
                    break

    with open("data_sources_config.json", "w") as f:
        json.dump(configs, f, indent=4)

def add_source():
    sources_to_add = get_sources(insert_value=False)
    
    if not sources_to_add:
        print("There exists no table to insert.")
        return

    print("Select Source:")
    for i, source in enumerate(sources_to_add, start=1):
        print(f"{i}. {source[0]} - {source[1]}")

    while True:
        option = input("Enter the index of the source to add or 'Exit' to exit: ")
        if option.lower() == 'exit':
            return
        try:
            option = int(option)
            if 1 <= option <= len(sources_to_add):
                selected_source = sources_to_add[option - 1]
                print(f"Selected Source: {selected_source[0]} - {selected_source[1]}")
                toggle_source_insert(selected_source[0], selected_source[1], insert_value=True)
                return
            else:
                print("Invalid option. Try again.")
        except ValueError:
            print("Invalid option. Try again.")

def remove_source():
    sources_to_remove = get_sources(insert_value=True)
    print("Select Source:")
    for i, source in enumerate(sources_to_remove, start=1):
        print(f"{i}. {source[0]} - {source[1]}")

    while True:
        option = input("Enter the index of the source to remove or 'Exit' to exit: ")
        if option.lower() == 'exit':
            return
        try:
            option = int(option)
            if 1 <= option <= len(sources_to_remove):
                selected_source = sources_to_remove[option - 1]
                print(f"Selected Source: {selected_source[0]} - {selected_source[1]}")
                toggle_source_insert(selected_source[0], selected_source[1], insert_value=False)
                return
            else:
                print("Invalid option. Try again.")
        except ValueError:
            print("Invalid option. Try again.")
            
def addDB():
    try:
        with open('databases.json', 'r') as json_file:
            data_dict = json.load(json_file)
    except FileNotFoundError:
        data_dict = {}  
    print("Select the type of Database:")
    print("1. Hostel")
    print("2. Mess")
    print("3. Sports")
    
    type_index = int(input("Enter the index: "))
    if type_index not in [1, 2, 3]:
        print("Invalid input. Please select a valid index.")
        return
    database_type = {1: "Hostel", 2: "Mess", 3: "Sports"}[type_index]
    database_name = input("Enter the name of the DB: ")
    data_dict[database_name] = database_type
    with open('databases.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    display_success_card(f"Added '{database_name}' to databases.json with type '{database_type}'.")

def deleteDB():
    try:
        with open('databases.json', 'r') as json_file:
            data_dict = json.load(json_file)
    except FileNotFoundError:
        print("No data found in databases.json.")
        return

    print("Current entries in databases.json:")
    for idx, (name, db_type) in enumerate(data_dict.items(), start=1):
        print(f"{idx}. {name} ({db_type})")

    if data_dict:
        try:
            delete_index = int(input("Enter the index of the entry to delete: "))
            if delete_index in range(1, len(data_dict) + 1):
                entry_to_delete = list(data_dict.keys())[delete_index - 1]
                del data_dict[entry_to_delete]

                with open('databases.json', 'w') as json_file:
                    json.dump(data_dict, json_file, indent=4)

                display_success_card(f"Deleted '{entry_to_delete}' from databases.json.")
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
    else:
        print("No entries to delete.")
        
def insertEntry():
    try:
        db_roll_no = getRollNo()
        with open('data_sources_config.json', 'r') as config_file:
            config_data = json.load(config_file)

        table_mapping = {db_config["db_name"]: [table["table"] for table in db_config["tables"]] for db_config in config_data}
        print("Select a Database:")
        for i, db_name in enumerate(table_mapping.keys()):
            print(f"{i + 1}. {db_name}")

        selected_db_index = int(input("Enter the index of the Database you want to edit: ")) - 1
        selected_db = list(table_mapping.keys())[selected_db_index]
        print(f"\nTables in {selected_db}:")
        for i, table_name in enumerate(table_mapping[selected_db]):
            print(f"{i + 1}. {table_name}")

        selected_table_index = int(input("Enter the index of the Table you want to edit: ")) - 1
        selected_table = table_mapping[selected_db][selected_table_index]

        headers, types = getTableData(selected_table)

        data = {}

        while True:
            try:
                roll_no = input(f"Enter value for Roll_No: ")
                if roll_no in db_roll_no:
                    data["Roll_No"] = roll_no
                    student_info = getStudentInfo(data["Roll_No"])
                    student_data = [(key, student_info[key]) for key in student_info]
                    print("Student Information:")
                    print(tabulate(student_data, headers=["Attribute", "Value"], tablefmt="pretty"))
                    break
                else:
                    print("Roll_No does not exist. You need to create a user for the Roll Number.")
            except ValueError:
                print("Roll_No must be an integer. Please enter a valid integer.")

        for header, data_type in zip(headers, types):
            if header != "Roll_No" and header != "Sr_No":  # Exclude "Sr_No"
                value = input(
                    f"Enter value for {header} ({data_type}) (press Enter to keep it NULL): "
                )

                if header in student_info and str(value) != str(student_info[header]):
                    print(f"Error: {header} value does not match the existing data.")
                    return
                data[header] = value if value != "" else None

        print("\nThe Final Information to be added will be:")
        print(f"Database: {selected_db}")
        print(f"Table: {selected_table}")
        print("Row to be added:")
        headers_names = [header for header in headers if header != "Sr_No"]
        data_values = [
            str(data[header]) if data[header] is not None else "NULL"
            for header in headers if header != "Sr_No"
        ]
        table_data = [headers_names, data_values]
        table = tabulate(table_data, headers="firstrow", tablefmt="pretty")
        print(table)
        insertData(selected_table, data)
        print("\nData Inserted Successfully") 
    
    except:
        display_error_card("Error in Inserting Data")   

def deleteEntry():
    try:
        with open('data_sources_config.json', 'r') as config_file:
            config_data = json.load(config_file)

        databases = [db_config["db_name"] for db_config in config_data if db_config["db_name"] != "AccessDB"]
        
        # Select a Database
        print("Select a Database:")
        for i, db_name in enumerate(databases):
            print(f"{i + 1}. {db_name}")

        selected_db_index = int(input("Enter the index of the Database you want to edit: ")) - 1
        selected_db = databases[selected_db_index]
        
        # Get tables for the selected database
        table_mapping = {db_config["db_name"]: [table["table"] for table in db_config["tables"]] for db_config in config_data}
        tables = table_mapping[selected_db]
        
        # Select a Table
        print(f"\nTables in {selected_db}:")
        for i, table_name in enumerate(tables):
            print(f"{i + 1}. {table_name}")

        selected_table_index = int(input("Enter the index of the Table you want to edit: ")) - 1
        selected_table = tables[selected_table_index]

        # Get headers and types using getTableData
        headers, types = getTableData(selected_table)

        # Display data in the table using getRows
        rows = getRows(selected_table)
        print("\nExisting Data in the Table:")
        print(tabulate(rows, headers=headers, tablefmt="pretty"))

        # Ask the user for the serial number of the row to delete
        try:
            serial_to_delete = int(input("Enter the serial number of the row you want to delete: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return
        # Delete the selected row
        deleteRow(selected_table, serial_to_delete)
        print("\nRow Deleted Successfully")

    except Exception as e:
        display_error_card("Error in Deleting Data")

def runDGDI():
    print_progress_bar(2,0)
    subprocess.run(['python', DATA_GEN])
    print_progress_bar(2,1)
    subprocess.run(['python', DATA_INSERT])
    print_progress_bar(2,2)
    display_success_card("Data Generated and Inserted Successfully")
    return
    
def setting():
    display_settings_menu(margin=-1)
    json_file_path = "data_sources_config.json"

    with open(json_file_path, "r") as f: 
        json_data = json.load(f)
    
    choice = input("Enter your choice: ")
    if choice == "1":
        display_title_card("Insert Entry option selected")
        insertEntry()
    elif choice == "2":
        display_title_card("Delete Row option selected")
        deleteEntry()
    elif choice == "3":
        display_title_card("Insert Table option selected")
    elif choice == "4":
        display_title_card("Delete Table option selected")
    elif choice == "5":
        display_title_card("Insert Database options selected")
        addDB()
    elif choice == "6":
        display_title_card("Delete Database options selected")
        deleteDB()
    elif choice == "7":
        display_title_card("Running Data-Gen and Data-Insert")
        runDGDI()
    elif choice == "8":
        display_title_card("")
    elif choice == "9":
        display_title_card("")
    elif choice == "10":
        display_title_card("Exiting the application")
        exit(0)
    else:
        display_title_card("Invalid choice. Try again")
        
def spwa():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")

def fmb():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return

def sip():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return

def mmt():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return

def sim():
    start = input("Enter the start time of the query: ")
    end = input("Enter the end time of the query: ")
    return

def hfu():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return

def sfu():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return

def sat():
    roll_no = input("Enter the roll number of the student: ")
    name = input("Enter the name of the student: ")
    return
    
def application():
    display_application_menu(margin=-1)
    choice = input("Enter your choice: ")
    if choice == "1":
        display_title_card("Student Performance and Wellness Analysis selected")
        spwa()
    elif choice == "2":
        display_title_card("Financial Management and Billin selected")
        fmb()
    elif choice == "3":
        display_title_card("Student Identity Profile selected")
        sip()
    elif choice == "4":
        display_title_card("Mess Meal Tracking selected")
        mmt()
    elif choice == "5":
        display_title_card("Sports Inventory Management selected")
        sim()
    elif choice == "6":
        display_title_card("Hostel Facilties Usage selected")
        hfu()
    elif choice == "7":
        display_title_card("Sports Facility Usage selected")
        sfu()
    elif choice == "8":
        display_title_card("Student Access Tracking selected")
        sat()
    elif choice == "9":
        display_title_card("Exiting the application")
        return
          
def dynamic():
    print_progress_bar(2,0)
    subprocess.run(['python', DYNAMIC_DATA])
    print_progress_bar(2,1)
    subprocess.run(['python', SYNC_DB])
    print_progress_bar(2,2)
    display_success_card("Data Updation Completed")
    
def etl():
    print_progress_bar(4,0)
    subprocess.run(['python', ETL_EXTRACT])
    print_progress_bar(4,1)
    subprocess.run(['python', ETL_TRANSFORM])
    print_progress_bar(4,2)
    subprocess.run(['python', ETL_LOAD])
    print_progress_bar(4,3)
    subprocess.run(['python', ETL_GLOBAL])
    print_progress_bar(4,4)
    display_success_card("ETL Process Completed")
       
while True:
    display_title_card("Welcome to University Smart Card System")

    display_menu(margin=-1)

    choice = input("Enter your choice: ")

    if choice == "1":
        display_title_card("Application selected")
        application()
    elif choice == "2":
        display_title_card("Setting selected")
        setting()
    elif choice == "3":
        display_title_card("Exiting the application")
        break
    else:
        display_error_card("Invalid choice. Try again")
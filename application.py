import time
import sys
import shutil
import subprocess
import os
import csv
import json

DYNAMIC_DATA = 'dynamic-data.py'
ETL_EXTRACT = 'extract.py'
ETL_LOAD = 'load.py'
ETL_TRANSFORM = 'transform.py'
ETL_GLOBAL = 'etl-global.py'
SYNC_DB = 'sync-databases.py'

# Constants for database and table names
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
    print(top_border)  # Top border
    line = f"{RED}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border)  # Bottom border
    print(NORMAL)  # Reset color

def display_success_card(success_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    error_text = f"{GREEN}SUCCESS: {success_message}\n"
    top_border = f"{GREEN}{'*' * box_width}"
    bottom_border = f"{GREEN}{'*' * box_width}"
    print(top_border)  # Top border
    line = f"{GREEN}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border)  # Bottom border
    print(NORMAL)  # Reset color
    
def display_title_card(title_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    error_text = f"{BLUE}{title_message}\n"
    top_border = f"{BLUE}{'*' * box_width}"
    bottom_border = f"{BLUE}{'*' * box_width}"
    print(top_border)  # Top border
    line = f"{BLUE}{error_text.strip().center(box_width)}{NORMAL}"
    print(line)
    print(bottom_border)  # Bottom border
    print(NORMAL)  # Reset color

def display_boxed_text(text, char1='*', char2='*', char3='*', margin=1):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin
    text_lines = text.split("\n")
    top_border = f"{char1 * box_width}"
    bottom_border = f"{char1 * box_width}"
    print(top_border)  # Top border
    for line in text_lines:
        if line.startswith("*"):
            # Text lines starting with '*' are considered menu items and have a different margin
            line = f"{char1}{' ' * (box_width - 2 * left_margin - len(line) + 3)}{line.strip().lstrip('*').rstrip('*').strip()} {char1}"
        else:
            # Other lines have the default margin
            line = f"{char1}{line.strip().center(box_width - 2 * left_margin)}{char1}"
        print(line)
    print(bottom_border)  # Bottom border

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
        "* 1. Insert New Source",
        "* 2. Delete Source",
        "* 3. Add Source",
        "* 4. Remove Source",
        "* 5. Modify Existing Source",
        "* 6. Update Data",
        "* 7. Run ETL",
        "* 8. Add Database",
        "* 9. Remove Database",
        "* 10. Exit",
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

    # Select Database
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
    
    # Display the entire data
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
        # Update JSON configuration
        new_data_source = {
            'table': table_name,
            'insert': False,  # Set to False by default
            'path': f"./Data/{table_name}.csv",
            'headers': headers,
            'primary_key': [key['Name'] for key in primary_key]
        }
        json_data[db_index]['tables'].append(new_data_source)
        with open(json_file_path, 'w') as f:
            json.dump(json_data, f, indent=2)

        # Create CSV file if it doesn't exist
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

    # Ask the user for the index of the entry to delete
    if data_dict:
        try:
            delete_index = int(input("Enter the index of the entry to delete: "))
            if delete_index in range(1, len(data_dict) + 1):
                entry_to_delete = list(data_dict.keys())[delete_index - 1]
                del data_dict[entry_to_delete]

                # Write the updated data_dict back to databases.json
                with open('databases.json', 'w') as json_file:
                    json.dump(data_dict, json_file, indent=4)

                display_success_card(f"Deleted '{entry_to_delete}' from databases.json.")
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
    else:
        print("No entries to delete.")

def setting():
    display_settings_menu(margin=-1)
    json_file_path = "data_sources_config.json"

    with open(json_file_path, "r") as f: 
        json_data = json.load(f)
    
    choice = input("Enter your choice: ")
    if choice == "1":
        display_title_card("Insert Source option selected")
        insert_new_data(json_data, json_file_path)
    elif choice == "2":
        display_title_card("Delete Source option selected")
    elif choice == "3":
        display_title_card("Add Source option selected")
        add_source()
    elif choice == "4":
        display_title_card("Remove Source option selected")
        remove_source()
    elif choice == "5":
        display_title_card("Modify Existing Source option selected")
    elif choice == "6":
        display_title_card("Updating Data initiated")
        dynamic()
    elif choice == "7":
        display_title_card("Initiating ETL Process")
        etl()
    elif choice == "8":
        display_title_card("Adding database options selected")
        addDB()
    elif choice == "9":
        display_title_card("Deleting database options selected")
        deleteDB()
    elif choice == "10":
        display_title_card("Exiting the application")
        exit(0)
    else:
        display_title_card("Invalid choice. Try again")

def application():
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
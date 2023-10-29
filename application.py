import time
import sys
import shutil
import subprocess

DYNAMIC_DATA = 'dynamic-data.py'
ETL_EXTRACT = 'extract.py'
ETL_LOAD = 'load.py'
ETL_TRANSFORM = 'transform.py'

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
    
# Function to display text in a designed template with borders and left/right margins
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
        "* 6. Run Dynamic Data Updation",
        "* 7. Run ETL",
        "* 8. Exit",
    ]

    for item in menu:
        item_with_margin = f"{item.ljust(box_width - 2 * left_margin - 4)} *"
        print(item_with_margin) 
    print() 

def insert_new_data():
    completed = 0
    segments = 4
    text = "Insert New Data\n\n"
    print_progress_bar(segments, completed)

    db_name = int(input("Select Database:\n1. SportsDB\n2. MessDB\n3. HostelDB\nEnter the index: "))
    if db_name < 1 or db_name > 3:
        print("Invalid database. Try again.")
        return

    db_name = DATABASES[db_name]
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
        display_boxed_text("Data inserted successfully")
    else:
        display_boxed_text("Data insertion canceled")
        

def remove_data():
    text = "Remove Data\n\n"

    print("Select Source:")
    for i, source in enumerate(SOURCES, start=1):
        print(f"{i}. {source[0]} - {source[1]}")

    while True:
        option = input("Enter the index of the source to remove or 'Exit' to exit: ")
        if option.lower() == 'exit':
            return
        try:
            option = int(option)
            if 1 <= option <= len(SOURCES):
                selected_source = SOURCES[option - 1]
                print(f"Selected Source: {selected_source[0]} - {selected_source[1]}")
                return
            else:
                print("Invalid option. Try again.")
        except ValueError:
            print("Invalid option. Try again.")

def dynamic():
    subprocess.run(['python', DYNAMIC_DATA])
    display_success_card("Config Data Updated")
    
def etl():
    subprocess.run(['python', ETL_EXTRACT])
    subprocess.run(['python', ETL_TRANSFORM])
    subprocess.run(['python', ETL_LOAD])
    display_success_card("ETL Process Completed")

def setting():
    display_settings_menu(margin=-1)
    
    choice = input("Enter your choice: ")
    if choice == "1":
        display_title_card("Insert Source option selected")
        insert_new_data()
    elif choice == "2":
        display_title_card("Delete Source option selected")
    elif choice == "3":
        display_title_card("Add Source option selected")
    elif choice == "4":
        display_title_card("Remove Source option selected")
        remove_data()
    elif choice == "5":
        display_title_card("Modify Existing Source option selected")
    elif choice == "6":
        display_title_card("Pulling Data from config")
        dynamic()
    elif choice == "7":
        display_title_card("Initiating ETL Process")
        etl()
    elif choice == "8":
        display_title_card("Exiting the application")
    else:
        display_title_card("Invalid choice. Try again")
        

def application():
    return

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
    
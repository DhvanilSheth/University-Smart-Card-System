import time
import sys
import shutil
import subprocess
import json

DYNAMIC_DATA = 'dynamic-data.py'
ETL_EXTRACT = 'extract.py'
ETL_LOAD = 'load.py'
ETL_TRANSFORM = 'transform.py'

DATABASES = {
    1: "SportsDB",
    2: "MessDB",
    3: "HostelDB"
}
PRIMARY_KEY_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]
HEADER_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]

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
            line = f"{char1}{' ' * (box_width - 2 * left_margin - len(line) + 3)}{line.strip().lstrip('*').rstrip('*').strip()} {char1}"
        else:
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

def remove_data():
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

def add_source():
    sources_to_add = get_sources(insert_value=False)
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
        add_source()
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
    

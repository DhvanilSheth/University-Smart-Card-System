import time
import sys
import shutil

# Constants for database and table names
DATABASES = {
    1: "SportsDB",
    2: "MessDB",
    3: "HostelDB"
}
PRIMARY_KEY_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]
HEADER_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]
SOURCES = [["Source1", "Database1"], ["Source2", "Database2"], ["Source3", "Database3"]]  # Replace with your SOURCES list

# Function to display a progress bar
def print_progress_bar(segments, completed):
    # Get the terminal width
    terminal_width, _ = shutil.get_terminal_size()

    # Calculate the bar length based on the terminal width
    bar_length = terminal_width - len("Progression: ") - 2

    # Calculate the number of completed and remaining blocks
    completed_blocks = int(bar_length * (completed / segments))
    remaining_blocks = bar_length - completed_blocks

    # ANSI escape codes for color
    red_color = "\033[91m"  # Red
    green_color = "\033[92m"  # Green
    reset_color = "\033[0m"  # Reset color

    # Build the progress bar with colors
    progress_bar = f"[{green_color}{'#' * completed_blocks}{red_color}{'-' * remaining_blocks}{reset_color}]"

    # Calculate the number of spaces for indentation
    indentation = ' ' * len("Progression: ")

    print(f"{'.' * terminal_width}")
    
    # Print the "Progression:" text and progress bar
    sys.stdout.write(f"\rProgression: {progress_bar}\n")
    sys.stdout.flush()
    
    print(f"{'.' * terminal_width}")
    print()

    # Check if segments equals completed
    return segments == completed

def display_error_card(error_message):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width

    # ANSI escape codes for color
    red_color = "\033[91m"  # Red
    reset_color = "\033[0m"

    error_text = f"{red_color}ERROR: {error_message}\n"
    top_border = f"{red_color}{'*' * box_width}"
    bottom_border = f"{red_color}{'*' * box_width}"
    print(top_border)  # Top border
    line = f"{red_color}{error_text.strip().center(box_width)}{reset_color}"
    print(line)
    print(bottom_border)  # Bottom border
    print(reset_color)  # Reset color

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

# Function to display the menu with left and right margins and vertically aligned items
def display_menu(char1='*', margin=5):
    terminal_width, _ = shutil.get_terminal_size()
    box_width = terminal_width
    left_margin = margin

    menu = [
        "* 1. Application",
        "* 2. Settings",
        "* 3. Exit"
    ]

    print()  # Empty line for top margin
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
        "* 2. Remove Source",
        "* 3. Modify Existing Source",
        "* 4. Exit",
    ]

    print()  # Empty line for top margin
    for item in menu:
        item_with_margin = f"{item.ljust(box_width - 2 * left_margin - 4)} *"
        print(item_with_margin) 
    print() 

def insert_new_data():
    completed = 0
    segments = 4
    text = "Insert New Data\n\n"
    print_progress_bar(segments, completed)
    
    db_name = int(input("Select Database:\n1.SportsDB\n2.MessDB\n3.HostelDB\nEnter the index: "))
    if db_name < 1 or db_name >3:
        print("Invalid database. Try again.")
        return
    
    db_name = DATABASES[db_name]
    completed += 1
    print_progress_bar(segments, completed)
    
    print(f"{db_name} Chosen")
    table_name = input("Give a name for the new source: ")
    table_name = "_".join(table_name.split())
    completed += 1
    print_progress_bar(segments, completed)

    headers = []
    primary_key = []

    while True:
        insert_header = input("Do you want to Insert New Header [Y/N]? ")
        if insert_header.lower() != "y":
            if not headers:
                display_error_card("New table cannot be created")
                return
            else:
                break

        header_name = input("Header Name: ")
        header_name = "_".join(header_name.split())

        header_type = input("Header Type " + str(HEADER_TYPES) + ": ")
        if header_type not in HEADER_TYPES:
            print("Invalid header type. Try again.")
            continue

        headers.append({"Name": header_name, "Type": header_type})

    completed += 1
    print_progress_bar(segments, completed)

    while not primary_key:
        primary_key_input = input("Which columns should be the primary key (e.g., '0 2' for columns 0 and 2): ")
        primary_key_indices = [int(idx) for idx in primary_key_input.split() if idx.isdigit()]

        for idx in primary_key_indices:
            if 0 <= idx < len(headers):
                primary_key.append(headers[idx])

    text += "Data to insert:\n"
    text += f"Database: {db_name}\n"
    text += f"Table: {table_name}\n"
    text += "Headers:\n"
    for header in headers:
        text += f"- {header['Name']} ({header['Type']})\n"
    text += "Primary Key:\n"
    for key in primary_key:
        text += f"- {key['Name']} ({key['Type']})\n"

    insert_confirm = input("Proceed with insertion [Y/N]? ")
    if insert_confirm.lower() == "y":
        # Add code here to insert data into the database
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


def setting():
    display_settings_menu(margin=-1)
    
    choice = input("Enter your choice: ")
    if choice == "1":
        display_boxed_text("Insert Source option selected", margin=1)
        insert_new_data()
    elif choice == "2":
        display_boxed_text("Remove Source option selected", margin=1)
        remove_data()
    elif choice == "3":
        display_boxed_text("Modify Existing Source option selected", margin=1)
    elif choice == "4":
        display_boxed_text("Exiting the application", margin=1)
    else:
        display_boxed_text("Invalid choice. Try again", margin=1)
        

def application():
    return

while True:
    display_boxed_text("Welcome to University Smart Card System", margin=1)

    display_menu(margin=-1)

    choice = input("Enter your choice: ")

    if choice == "1":
        display_boxed_text("Application selected", margin=1)
        application()
    elif choice == "2":
        display_boxed_text("Setting selected", margin=1)
        setting()
    elif choice == "3":
        display_boxed_text("Exiting the application", margin=1)
        break
    else:
        display_boxed_text("Invalid choice. Try again", margin=1)
    

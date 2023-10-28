import time
import sys
import shutil

# Constants for database and table names
DATABASES = ["SportsDB", "MessDB", "HostelDB"]
PRIMARY_KEY_TYPES = ["INT", "TEXT"]
HEADER_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]

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
    progress_bar = f"{red_color}[{green_color}{'#' * completed_blocks}{red_color}{'-' * remaining_blocks}{reset_color}]"

    # Calculate the number of spaces for indentation
    indentation = ' ' * len("Progression: ")

    # Print the "Progression:" text and progress bar
    sys.stdout.write(f"\rProgression: {progress_bar}\n")
    sys.stdout.flush()

    # Check if segments equals completed
    return segments == completed

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
def display_menu_with_margins(char1='*', margin=5):
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
        print(item_with_margin)  # Left and right margins
    print()  # Empty line for bottom margin

def insert_new_data():
    completed = 0
    segments = 3
    text = "Insert New Data\n\n"
    display_boxed_text("Data Insertion")
    text = "\n"
    print_progress_bar(segments, completed)
    db_name = input("Which DB? Options [SportsDB, MessDB, HostelDB]: ")
    if db_name not in DATABASES:
        print("Invalid database name. Try again.")
        return
    completed += 1
    print_progress_bar(segments, completed)

    table_name = input("Give Table Name: ")
    table_name = "_".join(table_name.split())
    completed += 1
    print_progress_bar(segments, completed)

    headers = []
    primary_key = []

    while True:
        insert_header = input("Do you want to Insert New Header [Y/N]? ")
        if insert_header.lower() != "y":
            if not headers:
                display_boxed_text("New table cannot be created")
                return
            else:
                break

        header_name = input("Header Name: ")
        header_name = "_".join(header_name.split())

        header_type = input("Header Type [INT, TEXT]: ")
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


while True:
    display_boxed_text("Welcome to University Smart Card System", margin=1)

    display_menu_with_margins(margin=-1)

    choice = input("Enter your choice: ")

    if choice == "1":
        insert_new_data()
    elif choice == "2":
        # Add code for removing a source
        display_boxed_text("Remove Source option selected", margin=1)
    elif choice == "3":
        # Add code for modifying an existing source
        display_boxed_text("Modify Existing Source option selected", margin=1)
    elif choice == "4":
        display_boxed_text("Exiting the application", margin=1)
        break
    else:
        display_boxed_text("Invalid choice. Try again", margin=1)

import time
import sys
import shutil

# Constants for database and table names
DATABASES = ["SportsDB", "MessDB", "HostelDB"]
PRIMARY_KEY_TYPES = ["INT", "TEXT"]
HEADER_TYPES = ["INT", "TEXT", "DATE", "VARCHAR(255)", "BOOLEAN", "TIME", "BIGINT", "DECIMAL(10, 2)"]

# Function to display a progress bar
def print_progress_bar(progress):
    bar_length = 30
    block = int(round(bar_length * progress))
    progress_bar = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{progress_bar}] {int(progress * 100)}%")
    sys.stdout.flush()

# Function to display text in a designed template with borders and left/right margins
def display_boxed_text(text, char1='*', char2='*', char3='*', margin=5):
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
    text = "Insert New Data\n\n"
    db_name = input("Which DB? Options [SportsDB, MessDB, HostelDB]: ")
    if db_name not in DATABASES:
        print("Invalid database name. Try again.")
        return

    table_name = input("Give Table Name: ")
    table_name = "_".join(table_name.split())

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
        display_boxed_text("Remove Source option selected", margin=5)
    elif choice == "3":
        # Add code for modifying an existing source
        display_boxed_text("Modify Existing Source option selected", margin=5)
    elif choice == "4":
        display_boxed_text("Exiting the application", margin=5)
        break
    else:
        display_boxed_text("Invalid choice. Try again", margin=5)

import time
import sys

# Constants for database and table names
DATABASES = ["SportsDB", "MessDB", "HostelDB"]
PRIMARY_KEY_TYPES = ["INT", "TEXT"]
HEADER_TYPES = ["INT", "TEXT"]

# Function to display a progress bar
def print_progress_bar(progress):
    bar_length = 30
    block = int(round(bar_length * progress))
    progress_bar = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{progress_bar}] {int(progress * 100)}%")
    sys.stdout.flush()

# Function to display text in a designed template
def display_template(text, char1='#', char2='.', char3='-'):
    template = f"{char1*50}\n"
    template += f"{char2*50}\n"
    template += f"{text}\n"
    template += f"{char3*50}"
    print(template)

def insert_new_data():
    display_template("Insert New Data")
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
                display_template("New table cannot be created")
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

    display_template("Data to insert:")
    print("Database:", db_name)
    print("Table:", table_name)
    display_template("Headers:")
    for header in headers:
        print(f"- {header['Name']} ({header['Type']})")
    display_template("Primary Key:")
    for key in primary_key:
        print(f"- {key['Name']} ({key['Type']})")

    insert_confirm = input("Proceed with insertion [Y/N]? ")
    if insert_confirm.lower() == "y":
        # Add code here to insert data into the database
        display_template("Data inserted successfully")
    else:
        display_template("Data insertion canceled")

while True:
    display_template("Welcome to University Smart Card System")
    print("1. Insert New Source")
    print("2. Remove Source")
    print("3. Modify Existing Source")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        insert_new_data()
    elif choice == "2":
        # Add code for removing a source
        display_template("Remove Source option selected")
    elif choice == "3":
        # Add code for modifying an existing source
        display_template("Modify Existing Source option selected")
    elif choice == "4":
        display_template("Exiting the application")
        break
    else:
        display_template("Invalid choice. Try again")

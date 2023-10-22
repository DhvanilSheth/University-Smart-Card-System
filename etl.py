import mysql.connector

def alter_primary_keys(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

    # List of commands to alter primary keys
    commands = [
        # SportsDB
        ("USE SportsDB;",),
        ("ALTER TABLE pool ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE pool_non_membership ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE medicine_sports ADD PRIMARY KEY(Contact_No, Time, Date);",),
        ("ALTER TABLE gym ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_requests ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_loss ADD PRIMARY KEY(Roll_No, Time, Date);",),

        # MessDB
        ("USE MessDB;",),
        ("ALTER TABLE mess_1_data ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE mess_2_data ADD PRIMARY KEY(Roll_No, Sale_ID);",),

        # HostelDB
        ("USE HostelDB;",),
        ("ALTER TABLE home_leave_data ADD PRIMARY KEY(Roll_No, Out_Time, Date);",),
        ("ALTER TABLE hostel_data ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE medicine_data ADD PRIMARY KEY(Contact, Time, Date);",),
        ("ALTER TABLE package_collection_data ADD PRIMARY KEY(Pick_Up_Student_Number, Driver_Contact, Sr_No);",)
    ]

    for command in commands:
        try:
            cursor.execute(*command)
        except mysql.connector.Error as err:
            print(f"Error executing {command}: {err}")

    cursor.close()
    connection.close()

alter_primary_keys('localhost', 'root', 'root')
import mysql.connector

def alter_primary_keys(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

    # List of commands to alter primary keys
    commands = [
        # SportsDB
        ("USE SportsDB;",),
        ("ALTER TABLE pool DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE pool_non_membership DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE medicine_sport DROP PRIMARY KEY, ADD PRIMARY KEY(Contact_No, Time, Date);",),
        ("ALTER TABLE gym DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_requests DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, In_Time, Date);",),
        ("ALTER TABLE equipment_loss DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Time, Date);",),

        # MessDB
        ("USE MessDB;",),
        ("ALTER TABLE mess1 DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE mess2 DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sale_ID);",),

        # HostelDB
        ("USE HostelDB;",),
        ("ALTER TABLE home_leave_data DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Out_Time, Date);",),
        ("ALTER TABLE hostel_data DROP PRIMARY KEY, ADD PRIMARY KEY(Roll_No, Sr_No);",),
        ("ALTER TABLE medicine_data DROP PRIMARY KEY, ADD PRIMARY KEY(Contact, Time, Date);",),
        ("ALTER TABLE package_collection DROP PRIMARY KEY, ADD PRIMARY KEY(Student_Contact, Driver_Contact, Sr_No);",)
    ]

    for command in commands:
        try:
            cursor.execute(*command)
        except mysql.connector.Error as err:
            print(f"Error executing {command}: {err}")

    cursor.close()
    connection.close()

alter_primary_keys('localhost', 'root', 'root')
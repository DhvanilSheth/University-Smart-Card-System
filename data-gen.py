from faker import Faker
import csv
import random

fake = Faker()

def generate_roll_numbers():
    roll_numbers = []
    for roll in range(1, 100):
        year_of_admission = random.randint(2018, 2024)
        roll_number_part = f"{roll:03d}"
        roll_number = f"{year_of_admission}{roll_number_part}"
        roll_numbers.append(roll_number)
    return roll_numbers

def generate_names():
    names = []
    for name in range(1,100):
        newName = fake.name()
        names.append(newName)
    return names

def generate_mapping(roll_numbers, student_names):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        student_name = student_names[i]
        mappings[roll_number] = student_name
    return mappings

roll_numbers = generate_roll_numbers()
student_names = generate_names()
mess_price_ranges = { '15 Days' : '1500',  '20 Days': '2000', '25 Days': '2500' }
course_types = ['BTech', 'Mtech', 'PhD']
room_types = ['Single', 'Double', 'Married']
floors = ['Ground', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Nineth', 'Tenth']
roll_no_name_mapping = generate_mapping(roll_numbers, student_names)

def generate_hostel_data(num_records):
    with open('./Data/hostel_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr. No", 
                         "Room Type",
                         "Floor",
                         "Room No", 
                         "Student Name"
                         "Roll No",
                         "Course Type",
                         "Year",
                         "Email ID",
                         "Fees",
                         "Security Amt",
                         "Bank ID", 
                         "Contact", 
                         "Remarks", 
                         "From", 
                         "To", 
                         "Sharing",
                         "Name", 
                         "Roll No", 
                         "Course", 
                         "Year", 
                         "Email ID"])  
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            writer.writerow([i+1,
                             fake.random.choice(room_types),
                             fake.random.choice(floors),
                             f"A-{fake.random_number(digits=3)}",
                             name,
                             roll_number,
                             fake.random.choice(course_types),
                             fake.random_number(digits=1),
                             fake.email(),
                             fake.random_number(digits=5),
                             fake.random_number(digits=5),
                             fake.random_number(digits=5),
                             fake.phone_number(),
                             fake.text(),
                             fake.date(),
                             fake.date(),
                             fake.name(),
                             random.choice(roll_numbers),
                             fake.word(),
                             fake.random_number(digits=1),
                             fake.email()
                             ])

def generate_mess_1_data(num_records):
    with open('./Data/mess_1_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sale ID", "Sale Date", "Coupon Type", "Name", "Phone Number", "Roll NO", "Paytm", "Cash", "Total Amount"])
        for i in range(num_records):
            choice_of_payment = random.random()
            type = random.choice(list(mess_price_ranges.keys()))
            cost = mess_price_ranges[type]
            mobile_number = fake.random_number(digits=10)
            if choice_of_payment == 1:
                writer.writerow([i + 1, fake.date_time(), type, fake.name(), mobile_number, random.choice(roll_numbers), cost, 0, cost])
            else:
                writer.writerow([i + 1, fake.date_time(), type, fake.name(), mobile_number, random.choice(roll_numbers), 0, cost, cost])


def generate_bms_hk_visitor_data(num_records):
    with open('./Data/bms_hk_visitor_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Department", "Purpose", "Room and Floor No", "Time In", "Time Out", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.sentence(), f"{fake.word()}-{fake.random_number(digits=2)}", fake.time(), fake.time(), fake.name(), fake.name()])


def generate_package_collection_data(num_records):
    with open('./Data/package_collection_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Room", "Delivery driver name", "Driver Contact", "Company", "Quantity", "Student Who Picks it", "Above person number", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), f"A-{fake.random_number(digits=3)}", fake.name(), fake.phone_number(), fake.company(), fake.random_number(digits=2), fake.name(), fake.phone_number(), fake.name(), fake.name()])


def generate_home_leave_data(num_records):
    with open('./Data/home_leave_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Out Time", "Roll No", "Room No", "To Address", "Return Time", "Return Date", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.time(), random.choice(roll_numbers), f"A-{fake.random_number(digits=3)}", fake.address(), fake.time(), fake.date(), fake.name(), fake.name()])


def generate_medicine_data(num_records):
    with open('./Data/medicine_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Medicine Name", "Quantity", "Room No", "Time", "Roll No", "Signature", "Purpose", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.random_number(digits=2), f"A-{fake.random_number(digits=3)}", fake.time(), random.choice(roll_numbers), fake.name(), fake.sentence(), fake.name()])


def generate_sports_data(num_records):
    with open('./Data/sports_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Sport", "Equipment", "Room No", "Time", "Roll No", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.word(), f"A-{fake.random_number(digits=3)}", fake.time(), fake.random_number(digits=6), fake.name(), fake.name()])

generate_hostel_data(100)
generate_mess_1_data(100)
generate_bms_hk_visitor_data(100)
generate_package_collection_data(100)
generate_home_leave_data(100)
generate_medicine_data(100)
generate_sports_data(100)
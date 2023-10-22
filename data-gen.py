import os
import json
from faker import Faker
import csv
import random

fake = Faker()

# Read DATA_SOURCES configuration from JSON file
with open('data_sources_config.json', 'r') as file:
    DATA_SOURCES = json.load(file)

roll_numbers_generated = set()

def generate_roll_numbers():
    roll_numbers = set()
    generated_roll_numbers = []

    while len(generated_roll_numbers) < 99:
        year_of_admission = random.randint(2018, 2024)
        roll_number_part = f"{random.randint(1, 999):03d}"
        roll_number = f"{year_of_admission}{roll_number_part}"

        if roll_number not in roll_numbers:
            roll_numbers.add(roll_number)
            generated_roll_numbers.append(roll_number)

    return generated_roll_numbers

def generate_names():
    names = []
    for name in range(1,100):
        newName = fake.name()
        names.append(newName)
    return names

def generate_mobile_no():
    numbers = []
    for number in range(1,100):
        newNum = fake.random_number(digits=10)
        numbers.append(newNum)
    return numbers

def generate_mapping_roll_no_to_name(roll_numbers, student_names):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        student_name = student_names[i]
        mappings[roll_number] = student_name
    return mappings

def generate_mapping_roll_no_to_email(roll_numbers, student_names):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        student_name = student_names[i]
        first_name = student_name.split()[0]
        last_5_digits = str(roll_number)[-5:]
        email = f"{first_name.lower()}{last_5_digits}@iiitd.ac.in"
        mappings[roll_number] = email
    return mappings
    
def generate_mapping_roll_no_to_course(roll_numbers, course_types):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        course_type = course_types[i % len(course_types)]
        mappings[roll_number] = course_type
    return mappings

def generate_mapping_roll_no_to_mobile(roll_numbers, mobile_numbers):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        mobile_number = mobile_numbers[i]
        mappings[roll_number] = mobile_number
    return mappings

roll_numbers = generate_roll_numbers()
student_names = generate_names()
mobile_numbers = generate_mobile_no()
mess_price_ranges = { '15 Days' : '1500',  '20 Days': '2000', '25 Days': '2500' }
hostel_fee_ranges = { 'Single' : '40000', 'Double' : '30000', 'Married': '35000'}
course_types = ['BTech', 'Mtech', 'PhD']
room_types = ['Single', 'Double', 'Married']
floors = ['Ground', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
remarks = ['No Remarks', 'Late Fees', 'Property Damage', 'Health Issues']
roll_no_name_mapping = generate_mapping_roll_no_to_name(roll_numbers, student_names)
roll_no_email_mapping = generate_mapping_roll_no_to_email(roll_numbers, student_names)
roll_no_course_mapping = generate_mapping_roll_no_to_course(roll_numbers, course_types)
roll_no_mobile_mapping = generate_mapping_roll_no_to_mobile(roll_numbers, mobile_numbers)

def generate_hostel_data(num_records):
    with open('./Data/hostel_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr No", 
                         "Room Type",
                         "Floor",
                         "Room No", 
                         "Student Name",
                         "Roll No",
                         "Course Type",
                         "Year",
                         "Email ID",
                         "Fees",
                         "Security Amt",
                         "Bank ID", 
                         "Contact", 
                         "Remarks", 
                         "From_Date", 
                         "To_Date", 
                         "Name_Share", 
                         "Roll_No_Share", 
                         "Course_Share", 
                         "Year_Share", 
                         "Email_ID_Share"])  
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            email = roll_no_email_mapping[roll_number]
            year = roll_number[:4]
            course = roll_no_course_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            type = fake.random.choice(room_types)
            fees = hostel_fee_ranges[type]
            security = fees[:-1]
            roll_number_2 = random.choice(roll_numbers)
            name_2 = roll_no_name_mapping[roll_number_2]
            email_2 = roll_no_email_mapping[roll_number_2]
            year_2 = roll_number_2[:4]
            course_2 = roll_no_course_mapping[roll_number_2]
            writer.writerow([i+1,
                            fake.random.choice(room_types),
                            fake.random.choice(floors),
                            f"A-{fake.random_number(digits=3)}",
                            name,
                            roll_number,
                            course,
                            year,
                            email,
                            fees,
                            security,
                            fake.random_number(digits=5),
                            mobile,
                            fake.random.choice(remarks),
                            fake.date(),
                            fake.date(),
                            name_2,
                            roll_number_2,
                            course_2,
                            year_2,
                            email_2
                            ])

def generate_mess_1_data(num_records):
    with open('./Data/mess_1_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr No", "Name", "Phone Number", "Roll No", "Cash", "PayTM", "Total", "Date of Purchase", "Breakfast", "Lunch", "Snack", "Dinner"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            choice_of_payment = random.choice([True, False])
            type = random.choice(list(mess_price_ranges.keys()))
            cost = mess_price_ranges[type]
            mobile_number = roll_no_mobile_mapping[roll_number]
            if choice_of_payment:
                writer.writerow([i + 1, name, mobile_number, roll_number, cost, 0, cost, fake.date(), fake.random_number(digits=2), fake.random_number(digits=2),fake.random_number(digits=2),fake.random_number(digits=2)])
            else:
                writer.writerow([i + 1, name, mobile_number, roll_number, 0, cost, cost, fake.date(), fake.random_number(digits=2), fake.random_number(digits=2),fake.random_number(digits=2),fake.random_number(digits=2)])

def generate_mess_2_data(num_records):
    with open('./Data/mess_2_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sale ID", "Sale Date", "Coupon Type", "Name", "Phone Number", "Roll NO", "Paytm", "Cash", "Total Amount"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            choice_of_payment = random.choice([True, False])
            type = random.choice(list(mess_price_ranges.keys()))
            cost = mess_price_ranges[type]
            mobile_number = roll_no_mobile_mapping[roll_number]
            if choice_of_payment:
                writer.writerow([i + 1, fake.date_time(), type, name, mobile_number, roll_number, cost, 0, cost])
            else:
                writer.writerow([i + 1, fake.date_time(), type, name, mobile_number, roll_number, 0, cost, cost])

def generate_package_collection_data(num_records):
    with open('./Data/package_collection_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr No", "Date", "Name", "Room", "Delivery driver name", "Driver Contact", "Company", "Quantity", "Pick Up Student", "Pick Up Student Number", "Signature", "Security Signature"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            roll_number_2 = random.choice(roll_numbers)
            pick_student = roll_no_name_mapping[roll_number_2]
            pick_number = roll_no_mobile_mapping[roll_number_2]
            writer.writerow([i + 1, fake.date(), name, f"A-{fake.random_number(digits=3)}", fake.name(), fake.random_number(digits=10), fake.company(), fake.random_number(digits=2), pick_student, pick_number, name, pick_student])

def generate_home_leave_data(num_records):
    with open('./Data/home_leave_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Out Time", "Roll No", "Room No", "To Address", "Return Time", "Return Date", "Signature", "Security Signature"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            number = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, number, fake.time()[:-3], random.choice(roll_numbers), f"A-{fake.random_number(digits=3)}", fake.address(), fake.time()[:-3], fake.date(), name, fake.name()])

def generate_medicine_data(num_records):
    with open('./Data/medicine_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Contact", "Medicine Name", "Quantity", "Room No", "Time", "Roll No", "Signature", "Purpose", "Security Signature"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, mobile, fake.word(), fake.random_number(digits=2), f"A-{fake.random_number(digits=3)}", fake.time()[:-3], roll_number, name, fake.sentence(), fake.name()])

def generate_equipment_loss(num_records):
    with open('./Data/equipment_loss.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "Equipment", "Time", "Remarks"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.word() , fake.time()[:-3], fake.sentence()])

def generate_gym(num_records):
    with open('./Data/gym.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "In_Time", "Out_Time", "Signature"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.time()[:-3] , fake.time()[:-3], name])

def generate_pool(num_records):
    with open('./Data/pool.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr No", "Card Number", "Membership Expiry", "Name", "Roll No", "Sex", "Department", "Presence"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            course = roll_no_course_mapping[roll_number]
            present = random.choice([True, False])
            writer.writerow([i+1, fake.random_number(digits=3), fake.date(), name, roll_number, fake.random.choice(['Male', 'Female']) , course , present])

def generate_equipment_requests(num_records):
    with open('./Data/equipment_requests.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "Equipment Issued", "Quantity", "In_Time", "Out_Time", "Signature", "Remarks"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.word() , fake.random_number(digits=1), fake.time()[:-3], fake.time()[:-3], name, fake.sentence()])

def generate_medicine_sports(num_records):
    with open('./Data/medicine_sports.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Name", "Contact No", "Quantity", "Medicine Name", "Student Sign", "Security Sign"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), fake.time()[:-3], name, mobile, fake.random_number(digits=1), fake.word() , name, fake.name()])

def generate_pool_non_membership(num_records):
    with open('./Data/pool_non_membership.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Tax ID", "Payment", "Roll No", "In_Time", "Sign"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            writer.writerow([fake.date(), name, fake.random_number(digits=4), fake.random_number(digits=3), roll_number, fake.time()[:-3], name])

def check_data_quality():
    # Check if roll numbers are unique
    if len(roll_numbers_generated) != len(set(roll_numbers_generated)):
        print("[ERROR] Duplicate roll numbers detected!")
        return False
    return True

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"[LOG] Deleted existing data source: {filename}")

def run(num):
    # Data Deletion Mechanism
    for data_source, active in DATA_SOURCES.items():
        if not active:
            delete_file_if_exists(f'./Data/{data_source}.csv')
    
    # Data Generation
    if DATA_SOURCES["hostel_data"]:
        generate_hostel_data(num)
    # ... [rest of the if conditions]

    # Data Quality Checks
    if not check_data_quality():
        print("[ERROR] Data quality checks failed!")
    else:
        print("[LOG] Data quality checks passed!")

run(100)
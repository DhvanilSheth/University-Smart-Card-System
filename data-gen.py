from faker import Faker
import csv
import random

fake = Faker()

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
    for _ in range(1, 100):
        newName = fake.name()
        names.append(newName)
    return names

def generate_mobile_no():
    numbers = []
    for _ in range(1, 100):
        newNum = fake.random_number(digits=10)
        numbers.append(newNum)
    return numbers

def generate_genders():
    genders = []
    for _ in range(1, 100):
        gender = fake.random_element(elements=("Male", "Female"))
        genders.append(gender)
    return genders

def generate_mapping_roll_no_to_name(roll_numbers, student_names):
    return {roll_number: name for roll_number, name in zip(roll_numbers, student_names)}

def generate_mapping_roll_no_to_email(roll_numbers, student_names):
    mappings = {}
    for roll_number, student_name in zip(roll_numbers, student_names):
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

def generate_mapping_roll_no_to_gender(roll_numbers, genders):
    mappings = {}
    for i in range(len(roll_numbers)):
        roll_number = roll_numbers[i]
        gender = genders[i]
        mappings[roll_number] = gender
    return mappings

roll_numbers = generate_roll_numbers()
student_names = generate_names()
mobile_numbers = generate_mobile_no()
genders = generate_genders()

mess_price_ranges = { '15 Days' : '1500',  '20 Days': '2000', '25 Days': '2500' }
hostel_fee_ranges = { 'Single' : '40000', 'Double' : '30000', 'Married': '35000'}
course_types = ['BTech', 'Mtech', 'PhD']
room_types = ['Single', 'Double', 'Married']
floors = ['Ground', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
remarks = ['No Remarks', 'Late Fees', 'Property Damage', 'Health Issues']
buildings = ['Academic Block', 'Hostel Block A', 'Hostel Block B', 'Sports Complex']

roll_no_name_mapping = generate_mapping_roll_no_to_name(roll_numbers, student_names)
roll_no_email_mapping = generate_mapping_roll_no_to_email(roll_numbers, student_names)
roll_no_course_mapping = generate_mapping_roll_no_to_course(roll_numbers, course_types)
roll_no_mobile_mapping = generate_mapping_roll_no_to_mobile(roll_numbers, mobile_numbers)
roll_no_gender_mapping = generate_mapping_roll_no_to_gender(roll_numbers, genders)

def generate_student_data():
    filename = './Data/student_data.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Name", "Contact No", "Email ID", "Course", "Gender"])

        for roll_no in roll_numbers:
            name = roll_no_name_mapping[roll_no]
            email = roll_no_email_mapping[roll_no]
            contact_no = roll_no_mobile_mapping[roll_no]
            course = roll_no_course_mapping[roll_no]
            gender = roll_no_gender_mapping[roll_no]
            writer.writerow([roll_no, name, contact_no, email, course, gender])

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
    with open('./Data/equipment_loss_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "Equipment", "Time", "Remarks"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.word() , fake.time()[:-3], fake.sentence()])

def generate_gym(num_records):
    with open('./Data/gym_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "In_Time", "Out_Time", "Signature"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.time()[:-3] , fake.time()[:-3], name])

def generate_pool(num_records):
    with open('./Data/swimming_pool_data.csv', mode='w', newline='') as file:
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
    with open('./Data/equipment_requests_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll No", "Room No", "Contact", "Equipment Issued", "Quantity", "In_Time", "Out_Time", "Signature", "Remarks"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), name, roll_number, f"A-{fake.random_number(digits=3)}", mobile, fake.word() , fake.random_number(digits=1), fake.time()[:-3], fake.time()[:-3], name, fake.sentence()])

def generate_medicine_sports(num_records):
    with open('./Data/medicine_sports_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Name", "Contact No", "Quantity", "Medicine Name", "Student Sign", "Security Sign"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            mobile = roll_no_mobile_mapping[roll_number]
            writer.writerow([fake.date(), fake.time()[:-3], name, mobile, fake.random_number(digits=1), fake.word() , name, fake.name()])

def generate_pool_non_membership(num_records):
    with open('./Data/swimming_pool_non_membership_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Tax ID", "Payment", "Roll No", "In_Time", "Sign"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            writer.writerow([fake.date(), name, fake.random_number(digits=4), fake.random_number(digits=3), roll_number, fake.time()[:-3], name])
            
def generate_access_log_records(num_records):
    with open('./Data/access_logs_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr_No", "Roll_No", "Name", "Building", "Room", "In_Time", "Out_Time", "In_Date", "Out_Date"])
        for i in range(num_records):
            roll_number = random.choice(roll_numbers)
            name = roll_no_name_mapping[roll_number]
            building = fake.random.choice(buildings)
            room = f"A-{fake.random_number(digits=3)}"
            in_time = fake.time()[:-3]
            out_time = fake.time()[:-3]
            in_date = fake.date()
            out_date = fake.date()
            writer.writerow([i + 1, roll_number, name, building, room, in_time, out_time, in_date, out_date])

def run(num):
    generate_student_data()
    generate_hostel_data(num)
    generate_mess_1_data(num)
    generate_mess_2_data(num)
    generate_package_collection_data(num)
    generate_home_leave_data(num)
    generate_medicine_data(num)
    generate_equipment_loss(num)
    generate_gym(num)
    generate_pool(num)
    generate_equipment_requests(num)
    generate_medicine_sports(num)
    generate_pool_non_membership(num)
    generate_access_log_records(num)
    print("Data Generation for CSV's is Complete")
    
run(100)
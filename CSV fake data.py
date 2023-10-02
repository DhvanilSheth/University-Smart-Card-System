from faker import Faker
import csv

fake = Faker()

def generate_hostel_data(num_records):
    with open('hostel_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sr. No", "Room Type", "Floor", "Room No", "Student Name", "Roll No", "Course Type", "Year", "Email ID", "Fees", "Security Amt", "Bank ID", "Contact", "Remarks", "From", "To", "Sharing", "Name", "Roll No", "Course", "Year", "Email ID"])  # header
        for i in range(num_records):
            writer.writerow([i+1, fake.random.choice(['Single', 'Double', 'Married']), fake.word(), f"A-{fake.random_number(digits=3)}", fake.name(), fake.random_number(digits=6), fake.word(), fake.random_number(digits=1), fake.email(), fake.random_number(digits=5), fake.random_number(digits=5), fake.random_number(digits=5), fake.phone_number(), fake.text(), fake.date(), fake.date(), fake.name(), fake.random_number(digits=6), fake.word(), fake.random_number(digits=1), fake.email()])

# Call the function with the number of records you want to generate

def generate_mess_data(num_records):
    with open('mess_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Sale ID", "Sale Date", "Coupon Type", "Name", "Phone Number", "Roll NO", "Paytm", "Cash", "Total Amount"])
        for i in range(num_records):
            writer.writerow([i + 1, fake.date_time(), fake.random.choice(['7 days', '30 days']), fake.name(), fake.phone_number(), fake.random_number(digits=6), fake.random_number(digits=3), fake.random_number(digits=3), fake.random_number(digits=4)])


def generate_bms_hk_visitor_data(num_records):
    with open('bms_hk_visitor_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Date", "Name", "Contact", "Department", "Purpose", "Room and Floor No", "Time In", "Time Out", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.sentence(), f"{fake.word()}-{fake.random_number(digits=2)}", fake.time(), fake.time(), fake.name(), fake.name()])


def generate_package_collection_data(num_records):
    with open('package_collection_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Date", "Name", "Room", "Delivery driver name", "Driver Contact", "Company", "Quantity", "Student Who Picks it", "Above person number", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), f"A-{fake.random_number(digits=3)}", fake.name(), fake.phone_number(), fake.company(), fake.random_number(digits=2), fake.name(), fake.phone_number(), fake.name(), fake.name()])


def generate_home_leave_data(num_records):
    with open('home_leave_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Date", "Name", "Contact", "Out Time", "Roll No", "Room No", "To Address", "Return Time", "Return Date", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.time(), fake.random_number(digits=6), f"A-{fake.random_number(digits=3)}", fake.address(), fake.time(), fake.date(), fake.name(), fake.name()])


def generate_medicine_data(num_records):
    with open('medicine_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Date", "Name", "Contact", "Medicine Name", "Quantity", "Room No", "Time", "Roll No", "Signature", "Purpose", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.random_number(digits=2), f"A-{fake.random_number(digits=3)}", fake.time(), fake.random_number(digits=6), fake.name(), fake.sentence(), fake.name()])


def generate_sports_data(num_records):
    with open('sports_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # header
        writer.writerow(["Date", "Name", "Contact", "Sport", "Equipment", "Room No", "Time", "Roll No", "Signature", "Security Signature"])
        for i in range(num_records):
            writer.writerow([fake.date(), fake.name(), fake.phone_number(), fake.word(), fake.word(), f"A-{fake.random_number(digits=3)}", fake.time(), fake.random_number(digits=6), fake.name(), fake.name()])

# generate_hostel_data(100)
# generate_mess_data(100)
# generate_bms_hk_visitor_data(100)
# generate_package_collection_data(100)
# generate_home_leave_data(100)
# generate_medicine_data(100)
# generate_sports_data(100)



def generate_roll_numbers(year_of_admission, start_roll, end_roll):
    roll_numbers = []
    for roll in range(start_roll, end_roll + 1):
        # Ensure the roll number portion is three digits by padding with zeros if necessary
        roll_number_part = f"{roll:03d}"
        roll_number = f"{year_of_admission}{roll_number_part}"
        roll_numbers.append(roll_number)
    return roll_numbers

# Example usage:
year_of_admission = 2021
start_roll = 1
end_roll = 100  # Adjust this to generate the desired range of roll numbers
roll_numbers = generate_roll_numbers(year_of_admission, start_roll, end_roll)

# Print or use the generated roll numbers
for roll_number in roll_numbers:
    print(roll_number)

import mysql.connector
import json
import pandas as pd

def transform(sports_data, hostel_data, mess_data, admin_data, access_data):
    integrated_data_list = []

    # Assuming student information is in admin_data with key 'Student_Information'
    student_info_df = admin_data['Student_Information']

    # Function to process each table
    def process_table(df, student_info_df):
        # Ensure 'Name' and 'Contact_No' are of type string
        if 'Name' in df.columns:
            df['Name'] = df['Name'].astype(str)
        if 'Contact_No' in df.columns:
            df['Contact_No'] = df['Contact_No'].astype(str)

        # Ensure 'Name' and 'Contact_No' in student_info_df are of type string
        student_info_df['Name'] = student_info_df['Name'].astype(str)
        student_info_df['Contact_No'] = student_info_df['Contact_No'].astype(str)

        # Add Sr_No if it's not present
        if 'Sr_No' not in df.columns:
            df['Sr_No'] = range(1, len(df) + 1)

        # Add Roll_No by mapping from student_info_df if it's not present and 'Name', 'Contact_No' are available
        if 'Roll_No' not in df.columns and {'Name', 'Contact_No'}.issubset(df.columns):
            df = df.merge(student_info_df[['Name', 'Contact_No', 'Roll_No']], on=['Name', 'Contact_No'], how='left')

        return df

    # Process each DataFrame in the dictionaries
    for data_dict in [sports_data, hostel_data, mess_data, admin_data, access_data]:
        for table_name, df in data_dict.items():
            processed_df = process_table(df, student_info_df)
            integrated_data_list.append(processed_df)

    print("Data Integration Complete")
    return integrated_data_list
import mysql.connector
import json
import pandas as pd

def transform(sports_data, hostel_data, mess_data, admin_data, access_data):
    integrated_data_list = []

    # Assuming student information is in admin_data with key 'Student_Information'
    student_info_df = admin_data['Student_Information'].copy()

    # Ensure 'Name' and 'Contact_No' in student_info_df are of type string
    student_info_df['Name'] = student_info_df['Name'].astype(str)
    student_info_df['Contact_No'] = student_info_df['Contact_No'].astype(str)

    # Function to process each table
    def process_table(df, student_info):
        # Add Sr_No if it's not present and move it to the first column
        if 'Sr_No' not in df.columns:
            df.insert(0, 'Sr_No', range(1, len(df) + 1))

        # Check for Contact_No or alternative column name
        contact_column = 'Contact_No'
        if 'Contact_No' not in df.columns and 'Pick_Up_Student_Number' in df.columns:
            contact_column = 'Pick_Up_Student_Number'

        # Ensure 'Name' and contact column are of type string in each df
        if 'Name' in df.columns:
            df['Name'] = df['Name'].astype(str)
        if contact_column in df.columns:
            df[contact_column] = df[contact_column].astype(str)

        # Add Roll_No by mapping from student_info if it's not present
        if 'Roll_No' not in df.columns and {'Name', contact_column}.issubset(df.columns):
            merged_df = df.merge(student_info[['Name', 'Contact_No', 'Roll_No']], left_on=['Name', contact_column], right_on=['Name', 'Contact_No'], how='left')
            df['Roll_No'] = merged_df['Roll_No']

        return df

    # Process each DataFrame in the dictionaries
    for data_dict in [sports_data, hostel_data, mess_data, admin_data, access_data]:
        for table_name, df in data_dict.items():
            processed_df = process_table(df, student_info_df)
            integrated_data_list.append(processed_df)

    print("Data Integration Complete")
    return integrated_data_list

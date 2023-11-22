import mysql.connector
import json
import pandas as pd

def transform(sports_data, hostel_data, mess_data, admin_data, access_data):
    integrated_data_list = []
    student_info_df = admin_data['student_data'].copy()
    student_info_df['Name'] = student_info_df['Name'].astype(str)
    student_info_df['Contact_No'] = student_info_df['Contact_No'].astype(str)

    def process_table(df, student_info):
        if 'Sr_No' not in df.columns:
            df.insert(0, 'Sr_No', range(1, len(df) + 1))
        name_column = 'Pick_Up_Student' if 'Pick_Up_Student' in df.columns else 'Name'
        contact_column = 'Pick_Up_Student_Number' if 'Pick_Up_Student_Number' in df.columns else 'Contact_No'
        if name_column in df.columns:
            df[name_column] = df[name_column].astype(str)
        if contact_column in df.columns:
            df[contact_column] = df[contact_column].astype(str)
        if 'Roll_No' not in df.columns and {name_column, contact_column}.issubset(df.columns):
            df = df.merge(student_info[['Name', 'Contact_No', 'Roll_No']], left_on=[name_column, contact_column], right_on=['Name', 'Contact_No'], how='left')
        return df
    for data_dict in [sports_data, hostel_data, mess_data, admin_data, access_data]:
        for table_name, df in data_dict.items():
            processed_df = process_table(df, student_info_df)
            integrated_data_list.append(processed_df)
    print("Data Integration Complete")
    return integrated_data_list



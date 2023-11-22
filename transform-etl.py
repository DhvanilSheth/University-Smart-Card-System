import mysql.connector
import json
import pandas as pd

def transform(sports_data, hostel_data, mess_data):
    # Identify common columns for entity matching
    common_columns = ['Name', 'Roll_No', 'Contact']  # Modify this list based on actual common columns

    # Create empty dataframe for integrated data
    integrated_data = pd.DataFrame()

    # Example of how to merge data from different tables
    for table_name, df in sports_data.items():
        if set(common_columns).issubset(df.columns):
            integrated_data = integrated_data.append(df[common_columns], ignore_index=True)

    for table_name, df in hostel_data.items():
        if set(common_columns).issubset(df.columns):
            integrated_data = integrated_data.append(df[common_columns], ignore_index=True)

    for table_name, df in mess_data.items():
        if set(common_columns).issubset(df.columns):
            integrated_data = integrated_data.append(df[common_columns], ignore_index=True)

    # Remove duplicates and reset index
    integrated_data = integrated_data.drop_duplicates().reset_index(drop=True)

    # Add a new primary key column
    integrated_data['ID'] = range(1, len(integrated_data) + 1)

    print("Data Integration Complete")
    return integrated_data
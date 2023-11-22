import mysql.connector
from sqlalchemy import create_engine

def load(dfs, host, user, password, database="UniDB"):
    # Create a connection to the database
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()

    # Drop existing tables in UniDB (Be cautious with this step)
    cursor.execute("DROP DATABASE IF EXISTS UniDB")
    cursor.execute("CREATE DATABASE UniDB")
    cursor.execute("USE UniDB")

    connection.commit()

    # SQLAlchemy engine for Pandas
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}', echo=False)

    # Load data into the new table
    table_names = {0:"swimming_pool_data", 1:"swimming_pool_non_membership_data", 2:"gym_data", 3:"equipment_data", 4:"equipment_loss_data", 
                   5:"sports_medicine_data", 6:"home_leave_data", 7:"hostel_data", 8:"hostel_medicine_data", 9:"courier_data",
                   10:"mess_1_data", 11:"mess_2_data", 12:"student_data", 13:"access_logs_data", 14:"integrated_data"}

    for df_index, df in enumerate(dfs):
        table_name = table_names[df_index]

        # Standardize Roll_No to VARCHAR if it's not already
        if 'Roll_No' in df.columns:
            df['Roll_No'] = df['Roll_No'].astype(str)

        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        # Modify the Roll_No column type
        alter_table_sql = f"ALTER TABLE `{table_name}` MODIFY `Roll_No` VARCHAR(255);"
        cursor.execute(alter_table_sql)

        # Check if primary key exists, and if not, add it
        cursor.execute(f"SHOW KEYS FROM `{table_name}` WHERE Key_name = 'PRIMARY'")
        if not cursor.fetchone():
            alter_table_sql = f"ALTER TABLE `{table_name}` ADD PRIMARY KEY (`Roll_No`, `Sr_No`);"
            cursor.execute(alter_table_sql)

    create_equipment = """
        CREATE VIEW Equipment_Global AS
        SELECT 
            Sr_No,
            Date,
            Name,
            Roll_No,
            Room_No,
            Contact,
            Equipment_Issued AS Equipment,
            Quantity,
            In_Time,
            Out_Time,
            Signature,
            Remarks
        FROM equipment_data

        UNION ALL

        SELECT 
            Sr_No,
            Date,
            Name,
            Roll_No,
            Room_No,
            Contact,
            Equipment,
            NULL AS Quantity,
            NULL AS In_Time,
            NULL AS Out_Time,
            NULL AS Signature,
            Remarks
        FROM equipment_loss_data;
    """
    cursor.execute(create_equipment)
    connection.commit()

    create_mess = """
        CREATE VIEW Mess_Global AS
        SELECT
            CONCAT(Roll_No, '-', Sr_No) AS UniqueID,
            Sr_No,
            Roll_No,
            Name,
            Phone_Number,
            Cash,
            PayTM,
            Total AS TotalAmount,
            Date_of_Purchase AS TransactionDate,
            Breakfast AS BreakfastCoupons,
            Lunch AS LunchCoupons,
            Snack AS SnackCoupons,
            Dinner AS DinnerCoupons,
            NULL AS CouponType
        FROM
            mess_1_data
        UNION ALL
        SELECT
            CONCAT(Roll_No, '-', Sr_No) AS UniqueID,
            Sr_No,
            Roll_No,
            Name,
            Phone_Number,
            Cash,
            Paytm,
            Total_Amount,
            Sale_Date AS TransactionDate,
            NULL AS BreakfastCoupons,
            NULL AS LunchCoupons,
            NULL AS SnackCoupons,
            NULL AS DinnerCoupons,
            Coupon_Type
        FROM
            mess_2_data;
    """

    cursor.execute(create_mess)
    connection.commit()

    create_pool = """
        CREATE VIEW Pool_Global AS
        SELECT
            CONCAT(Roll_No, '-', Sr_No) AS CompositeKey,
            Sr_No, 
            Roll_No,
            Name,
            NULL AS Date,
            NULL AS InTime,
            Card_Number,
            Membership_Expiry,
            Sex,
            Department,
            Presence,
            NULL AS TaxID,
            NULL AS Payment,
            NULL AS Sign
        FROM
            swimming_pool_data
        UNION ALL
        SELECT
            CONCAT(Roll_No, '-', Sr_No) AS CompositeKey,
            Sr_No,
            Roll_No,
            Name,
            Date,
            NULL AS InTime,
            NULL AS CardNo,
            NULL AS MembershipExpiry,
            NULL AS Sex,
            NULL AS Department,
            NULL AS Presence,
            Tax_ID,
            Payment,
            NULL AS Sign
        FROM
            swimming_pool_non_membership_data;
    """

    cursor.execute(create_pool)
    connection.commit()

    create_medicine = """
        CREATE VIEW Medicine_Global AS
        SELECT 
            CONCAT(hmd.Roll_No, '-', hmd.Sr_No) AS composite_key,
            'Hostel' AS Source,
            hmd.Name,
            hmd.Date,
            hmd.Time,
            hmd.Medicine_Name,
            hmd.Quantity,
            hmd.Contact,
            hmd.Room_No,
            hmd.Purpose
        FROM 
            hostel_medicine_data hmd
        UNION ALL
        SELECT 
            CONCAT(smd.Roll_No, '-', smd.Sr_No) AS composite_key,
            'Sports' AS Source,
            smd.Name,
            smd.Date,
            smd.Time,
            smd.Medicine_Name,
            smd.Quantity,
            smd.Contact_No AS Contact,
            NULL AS Room_No,
            NULL AS Purpose
        FROM 
            sports_medicine_data smd;
    """

    cursor.execute(create_medicine)
    connection.commit()

    cursor.close()
    connection.close()
    print("Data Loaded into UniDB Warehouse")

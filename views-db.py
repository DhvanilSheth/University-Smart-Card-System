import mysql.connector
def create_pool_union_view(host, user, password):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()

    view_sql = """
    CREATE VIEW PoolDataView AS
    SELECT
        'pool_non_membership' AS TableType,
        Date AS EventDate,
        Name,
        NULL AS Membership_Expiry,
        Tax_ID AS Identifier,
        Payment AS Amount,
        Roll_No AS MemberID,
        In_Time AS Time,
        Sign AS Signature
    FROM pool_non_membership

    UNION ALL

    SELECT
        'pool' AS TableType,
        Membership_Expiry AS EventDate,
        Name,
        NULL AS Identifier,
        NULL AS Amount,
        Roll_No AS MemberID,
        NULL AS Time,
        NULL AS Signature
    FROM pool;
    """

    cursor.execute("CREATE DATABASE IF NOT EXISTS SportsDB")
    cursor.execute("USE SportsDB")
    cursor.execute(view_sql)
    cursor.close()
    connection.close()

    return "PoolDataView created successfully."



def run():
    host = "localhost"
    user = "root"
    password = "#"
    result = create_pool_union_view(host, user, password)

run()

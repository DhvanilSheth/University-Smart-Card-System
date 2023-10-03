# pip install Flask pandas mysql-connector-python


from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

app = Flask(__name__)

def get_insert_query(table_name, row):
    # This function generates an SQL query based on the table name and row data
    columns = ", ".join(row.index)
    placeholders = ", ".join(["%s"] * len(row))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    return query

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    table_name = request.form['table_name']
    
    if uploaded_file.filename != '':
        data = pd.read_csv(uploaded_file)
        conn = mysql.connector.connect(
            host='your_host',
            user='your_username',
            password='your_password',
            database='IIITD_DB'
        )
        cursor = conn.cursor()
        
        for index, row in data.iterrows():
            query = get_insert_query(table_name, row)
            cursor.execute(query, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Data uploaded successfully!'}), 200
    else:
        return jsonify({'message': 'Invalid file'}), 400

if __name__ == "__main__":
    app.run(debug=True)

# pip install Flask pandas mysql-connector-python

from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector
import os

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
        # Check if the uploaded file is a CSV file
        if uploaded_file.filename.split('.')[-1].lower() != 'csv':
            return jsonify({'message': 'Invalid file format. Only CSV files are allowed.'}), 400
        
        data = pd.read_csv(uploaded_file)
        
        # Get database credentials from environment variables
        host = os.environ.get('DB_HOST')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_DATABASE')
        
        if not all([host, user, password, database]):
            return jsonify({'message': 'Database credentials not found.'}), 500
        
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        cursor = conn.cursor()
        
        # Check if the table exists in the database
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': f"Table '{table_name}' does not exist."}), 400
        
        try:
            for index, row in data.iterrows():
                query = get_insert_query(table_name, row)
                cursor.execute(query, tuple(row))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({'message': 'Data uploaded successfully!'}), 200
        except Exception as e:
            return jsonify({'message': f"Error uploading data: {str(e)}"}), 500
    else:
        return jsonify({'message': 'Invalid file'}), 400

if __name__ == "__main__":
    app.run(debug=True)
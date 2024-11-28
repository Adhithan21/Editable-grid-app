from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("records.db")
    conn.row_factory = sqlite3.Row
    return conn

# Get all records
@app.route('/records', methods=['GET'])
def get_records():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records').fetchall()
    conn.close()
    return jsonify([dict(record) for record in records])

# Add a new record
@app.route('/records', methods=['POST'])
def add_record():
    new_record = request.get_json()
    name = new_record['name']
    age = new_record['age']
    email = new_record['email']
    gender = new_record['gender']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO records (name, age, email, gender) VALUES (?, ?, ?, ?)', 
                 (name, age, email, gender))
    conn.commit()
    conn.close()
    return '', 201

# Update an existing record
@app.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    updated_record = request.get_json()
    new_id = updated_record['id']
    name = updated_record['name']
    age = updated_record['age']
    email = updated_record['email']
    gender = updated_record['gender']
    
    conn = get_db_connection()
    conn.execute('UPDATE records SET id = ?, name = ?, age = ?, email = ?, gender = ? WHERE id = ?',
                 (new_id, name, age, email, gender, id))
    conn.commit()
    conn.close()
    return '', 200

# Delete a record
@app.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 200

# Delete all records and reset ID counter
@app.route('/records/delete_all', methods=['DELETE'])
def delete_all_records():
    conn = get_db_connection()
    conn.execute('DELETE FROM records')  
    conn.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "records"')  
    conn.commit()
    conn.close()
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)

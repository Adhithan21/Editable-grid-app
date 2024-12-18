pip install --upgrade pip
pip install --upgrade gunicorn
import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/records"

# Fetch all records from the Flask API
def fetch_records():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        records = response.json()
        if records:
            df = pd.DataFrame(records)
            df.index = df.index + 1  # Set the index to start from 1
            return df
        else:
            return pd.DataFrame(columns=["id", "name", "age", "email", "gender"])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching records: {e}")
        return pd.DataFrame()

# Add a new record
def add_record(name, age, email, gender):
    data = {"name": name, "age": age, "email": email, "gender": gender}
    response = requests.post(API_URL, json=data)
    return response.status_code == 201

# Update a record
def update_record(record_id, new_id, name, age, email, gender):
    data = {"id": new_id, "name": name, "age": age, "email": email, "gender": gender}
    response = requests.put(f"{API_URL}/{record_id}", json=data)
    return response.status_code == 200

# Delete a record
def delete_record(record_id):
    response = requests.delete(f"{API_URL}/{record_id}")
    return response.status_code == 200

# Delete all records
def delete_all_records():
    response = requests.delete(f"{API_URL}/delete_all")
    return response.status_code == 200

# Streamlit UI
st.title(":red[Editable Records with Flask API]")

# Form to add a new record
with st.form("add_form"):
    st.subheader(":green[Add a New Record]")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    email = st.text_input("Email")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    submit_button = st.form_submit_button("Add Record")
    if submit_button:
        if add_record(name, age, email, gender):
            st.success("Record added successfully!")
        else:
            st.error("Failed to add record.")

# Display existing records
records = fetch_records()

if not records.empty:
    st.subheader(":blue[Existing Records]")
    st.dataframe(records)

    # Buttons to edit or delete records
    for _, record in records.iterrows():
        st.write(f"**ID:** {record['id']} - **Name:** {record['name']} - **Age:** {record['age']} - **Email:** {record['email']} - **Gender:** {record['gender']}")
        
        with st.expander(f"Edit Record ID {record['id']}"):
            col1, col2 = st.columns([3, 1])  # Create two columns: 3 for inputs, 1 for buttons

            with col1:
                # Editable fields
                new_id = st.number_input("New ID", value=record['id'], min_value=1, key=f"edit_id_{record['id']}")
                new_name = st.text_input("New Name", value=record['name'], key=f"edit_name_{record['id']}")
                new_age = st.number_input("New Age", value=record['age'], min_value=1, max_value=120, key=f"edit_age_{record['id']}")
                new_email = st.text_input("New Email", value=record['email'], key=f"edit_email_{record['id']}")
                new_gender = st.selectbox("New Gender", ["Male", "Female", "Other"], key=f"edit_gender_{record['id']}")

            with col2:
                # Update button (right side)
                if st.button("Update", key=f"update_{record['id']}"):
                    if update_record(record['id'], new_id, new_name, new_age, new_email, new_gender):
                        st.success(f"Record {record['id']} updated!")
                        st.rerun()  # Reload to reflect changes

                # Delete button (right side)
                if st.button("Delete", key=f"delete_{record['id']}"):
                    if delete_record(record['id']):
                        st.success(f"Record {record['id']} deleted!")
                        st.rerun()  # Reload after deletion

# Button to delete all records
if st.button(":red[Delete All Records]"):
    if delete_all_records():
        st.success("All records deleted and ID reset to 1!")
        st.rerun()  # Reload to reflect changes
    else:
        st.error("Failed to delete all records.")

import streamlit as st
import requests

API_URL = "http://localhost:8002/query"

st.title("Doctor Appointment AI")

user_id = st.text_input("Enter your ID number:", "")
query = st.text_area("Enter your query:", "Can you check if a dentist is available tomorrow at 10 AM?")

if st.button("Submit Query"):
    if user_id and query:
        try:
            response = requests.post(API_URL, json={'messages': query, 'id_number': int(user_id)}, verify=False)
            if response.status_code == 200:
                st.success("Query submitted successfully!")
                print("================== My response ==================")
                print(response.json())
                st.write(response.json()["messages"])
            else:
                st.error(f"Error: {response.status_code}: Could not process the query.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter both ID number and query.")
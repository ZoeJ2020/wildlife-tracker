import streamlit as st


abspath = os.path.abspath(__file__)

dname = os.path.dirname(abspath)

print(dname)

os.chdir(dname)


from st_files_connection import FilesConnection
import os
# import ai_detection

print(os.getcwd())

# os.chdir('/workspaces/wildlife-tracker')

from ai_detection import detect_objects

st.set_page_config(page_title="Add Wildlife Sighting")

st.markdown("# Add Wildlife Sighting")
st.sidebar.header("Add Wildlife Sighting")

import sqlite3

conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# c.execute("DROP TABLE user_data")

c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        type TEXT,
        breed TEXT,
        condition TEXT,
        location TEXT,
        age INTEGER,
        height INTEGER,
        weight INTEGER
    )
''')
conn.commit()

UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

import streamlit as st

on = st.toggle("Activate AI-powered Animal Detection")

if on:
    with st.form("data_form"):
        uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        date = st.date_input("Date Photographed")
        # type = st.text_input("Type")
        # breed = st.text_input("Breed")
        condition = st.selectbox(
        "Health condition",
        ("Healthy", "Injured", "Unknown")
        )
        location = st.text_input("Location found")
        age = st.number_input("Optional: Age (in years)")
        height = st.number_input("Optional: Height (in metres)")
        weight = st.number_input("Optional: Weight (in kg)")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if uploaded_image is not None:
                image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)

                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                type, breed = detect_objects('./uploaded_images/' + uploaded_image.name)

                c.execute('''
                    INSERT INTO user_data (image_path, date, type, breed, condition, location, age, height, weight) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (image_path, date, type, breed, condition, location, age, height, weight))
                conn.commit()

                st.success(f"Sighting submitted successfully!")
            else:
                st.warning("Please upload an image.")



else:
    with st.form("data_form"):
        uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        date = st.date_input("Date Photographed")
        type = st.text_input("Type")
        breed = st.text_input("Breed")
        condition = st.selectbox(
        "Health condition",
        ("Healthy", "Injured", "Unknown")
        )
        location = st.text_input("Location found")
        age = st.number_input("Optional: Age (in years)")
        height = st.number_input("Optional: Height (in metres)")
        weight = st.number_input("Optional: Weight (in kg)")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if uploaded_image is not None:
                image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())

                c.execute('''
                    INSERT INTO user_data (image_path, date, type, breed, condition, location, age, height, weight) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (image_path, date, type, breed, condition, location, age, height, weight))
                conn.commit()

                st.success(f"Sighting submitted successfully!")
            else:
                st.warning("Please upload an image.")


conn.close()

#st.markdown('<style>' + open('styling.css').read() + '</style>', unsafe_allow_html=True)
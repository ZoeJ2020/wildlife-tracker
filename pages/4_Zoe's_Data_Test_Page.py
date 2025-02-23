
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(page_title="Zoe's Data Test")

st.markdown("# Zoe's Data Test")
st.sidebar.header("Zoe's Data Test")
st.write(
    """test for data retrieval from database"""
)

# CODE BELOW!!!
import sqlite3
import os

# Setup SQLite database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# c.execute('''DROP TABLE user_data''')

# Create a table for storing user data along with image path (if not exists)
c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
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

# Define the folder to store images
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit form for user data and image upload
with st.form("data_form"):
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
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
            # Save the image to the local folder
            image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            # Insert user data and image path into the database
            c.execute('''
                INSERT INTO user_data (image_path, type, breed, condition, location, age, height, weight) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (image_path, type, breed, condition, location, age, height, weight))
            conn.commit()

            st.success(f"Form submitted successfully! Image saved at {image_path}")
        else:
            st.warning("Please upload an image.")

# Display submitted data from the database
st.subheader("Submitted User Data")

# Query data from SQLite
c.execute("SELECT * FROM user_data")
rows = c.fetchall()

for row in rows:
    st.image(row[1], caption= row[2] + ", " + row[3])
    st.title(row[3])
    st.title(row[2])

# Display data
# import pandas as pd
# df = pd.DataFrame(rows, columns=["Image", "Type", "Breed", "Condition", "Age", "Height", "Weight"])
# st.dataframe(df)

# Close the connection
conn.close()
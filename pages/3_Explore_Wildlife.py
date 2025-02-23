import streamlit as st
from st_files_connection import FilesConnection

os.chdir('/workspaces/wildlife-tracker/pages')

st.set_page_config(page_title="Explore Wildlife")

st.markdown("# Explore Wildlife")
st.sidebar.header("Explore Wildlife")

import sqlite3
import os

image_width = 200

conn = sqlite3.connect('user_data.db')
c = conn.cursor()

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

st.subheader("Filter Wildlife")

search_type = st.text_input("Search by Type")
search_breed = st.text_input("Search by Breed")

submit_button = st.button("Submit")

if submit_button:
    if search_type or search_breed:
        query = "SELECT * FROM user_data WHERE"
        filters = []
        params = []

        if search_type:
            query += " type LIKE ?"
            filters.append("type")
            params.append(f"%{search_type}%")

        if search_breed:
            if filters:
                query += " AND"
            query += " breed LIKE ?"
            filters.append("breed")
            params.append(f"%{search_breed}%")

        c.execute(query, params)
        rows = c.fetchall()

        if rows:
            for row in rows:
                print(row)
                st.image(row[1], width=image_width)
                st.caption(row[4] + " - " + row[6] + " - " + row[2] + " - " + row[5])
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a type or breed to search.")

else:
    st.header("All Wildlife")

    c.execute("SELECT * FROM user_data;")
    rows = c.fetchall()

    for row in rows:
        print(row)
        st.subheader(row[4])
        st.image(row[1], width=image_width)
        st.caption(row[3] + " - " + row[6] + " - " + row[2] + " - " + row[5])
        #st.subheader(row[2])

conn.close()

#st.markdown('<style>' + open('styling.css').read() + '</style>', unsafe_allow_html=True)
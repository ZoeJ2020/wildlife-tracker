import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🌿",
)

st.write("# HOME")

with st.container():
    st.write("")


# code to fetch recently spotted here.
import sqlite3

# Setup SQLite database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Display submitted data from the database
st.subheader("Recently Spotted in Aberdeen")

# Query data from SQLite
c.execute("SELECT * FROM user_data WHERE location = 'Aberdeen' ORDER BY date DESC LIMIT 1;")
rows = c.fetchall()

for row in rows:
    st.image(row[1])
    st.title(row[4])
    st.title(row[2])

# Close the connection
conn.close()

# Setup SQLite database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Display submitted data from the database
st.subheader("Most Recent Sighting")

# Query data from SQLite
c.execute("SELECT * FROM user_data ORDER BY date DESC LIMIT 1;")
rows = c.fetchall()

for row in rows:
    st.image(row[1])
    st.title(row[4])
    st.title(row[6])
    st.title(row[2])

# Close the connection
conn.close()

st.markdown('<style>' + open('styling.css').read() + '</style>', unsafe_allow_html=True)
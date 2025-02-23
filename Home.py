import streamlit as st

image_width = 200

st.set_page_config(
    page_title="Home",
    page_icon="🌿",
)

st.write("# HOME")


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
    st.image(row[1], width=image_width)
    st.caption(row[4] + " - " + row[2])

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
    st.image(row[1], width=image_width)
    st.caption(row[4] + " in " + row[6] + " at " + row[2])

# Close the connection
conn.close()

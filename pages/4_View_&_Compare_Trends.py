import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="View & Compare Trends")

st.markdown("# View & Compare Trends")
st.sidebar.header("View & Compare Trends")


@st.cache_data
def get_animal_data():
    data = {
        "Animal" : ["Bird", "Squirrel", "Cat", "Fox", "Wolf"],
        2018 : [100, 80, 20, 50, 25],
        2019 : [70, 50, 18, 80, 35],
        2020 : [90, 100, 15, 60, 32]
    }

    return pd.DataFrame(data).set_index("Animal")


try:
    df = get_animal_data()
    animals = st.multiselect(
        "Choose animals", list(df.index), ["Bird", "Fox"]
    )
    if not animals:
        st.error("Please select at least one animal.")
    else:
        data = df.loc[animals]
        st.write("Population of animals in area", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "variable" : "Animal", "value": "Sightings of specific animal in area"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Sightings of specific animal in area:Q", stack=None),
                color="Animal:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )


st.markdown('<style>' + open('css/dataframe.css').read() + '</style>', unsafe_allow_html=True)
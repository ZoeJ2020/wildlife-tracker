import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data
def get_animal_data():
    data = {
        "Animal" : ["Dog", "Cat"],
        2018 : [100, 80],
        2019 : [70, 50],
        2020 : [90, 100]
    }

    return pd.DataFrame(data).set_index("Animal")


try:
    df = get_animal_data()
    animals = st.multiselect(
        "Choose animals", list(df.index), ["Dog", "Cat"]
    )
    if not animals:
        st.error("Please select at least one animal.")
    else:
        data = df.loc[animals]
        # data /= 1000000.0
        st.write("Sightings of anials in area", data.sort_index())

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
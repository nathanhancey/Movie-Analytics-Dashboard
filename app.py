import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import graph

# Some base variables for OMDb API
# (Personal note) Get key at: http://www.omdbapi.com/apikey.aspx
API_KEY = "1fc7cba6"
BASE_URL = "http://www.omdbapi.com/"

st.title("Movie Rating Dashboard")

# Example Dataset Button
use_example = st.button("Use Example Dataset")

# Get User Input
keyword = st.text_input("Enter a movie keyword:")

def fetch_ratings(title):
    # Fetch movie data from OMDb API
    params = {"t": title, "apikey": API_KEY}
    data = requests.get(BASE_URL, params=params).json()

    # Handle case where movie is not found
    if data.get("Response") == "False":
        return None

    # Parse the ratings from the api response
    imdb = data.get("imdbRating")
    imdb = float(imdb) if imdb and imdb != "N/A" else None

    rt = None
    meta = None
    for rating in data.get("Ratings", []):
        if rating["Source"] == "Rotten Tomatoes":
            rt = rating["Value"].replace("%", "")
            rt = float(rt) / 10
        if rating["Source"] == "Metacritic":
            meta = rating["Value"].split("/")[0]
            meta = float(meta) / 10

    return {
        "Title": data["Title"],
        "IMDb": imdb,
        "Rotten Tomatoes": rt,
        "Metacritic": meta
    }

if use_example:
    st.subheader("Using Example Dataset (test.csv)")

    df_raw = pd.read_csv("test.csv")

    # convert dataset to long format
    df_plot = pd.melt(
        df_raw,
        id_vars=["Title"],
        value_vars=["IMDb", "Rotten Tomatoes", "Metacritic"],
        var_name="Source",
        value_name="Rating"
    ).dropna()

    fig = graph.bar_charts(df_plot, "Example Movies")
    st.pyplot(fig)

    # Display style legend table
    """
    legend_df = pd.DataFrame([
        {"Title": title, "Color": str(style["color"]), "Marker": style["marker"]}
        for title, style in styles.items()
    ])

    st.subheader("Plot Legend (Movie → Color → Marker)")
    st.dataframe(legend_df)
    """

    st.stop()

# *Broken* Does not work with free API key due unkown issue
if keyword:
    st.write(f"Searching OMDb for: **{keyword}**")

    search_data = requests.get(BASE_URL, params={"s": keyword, "apikey": API_KEY}).json()

    if search_data.get("Response") == "False":
        st.error(f"OMDb Error: {search_data.get('Error')}")
        st.stop()

    # Let the user choose among multiple search results
    titles = [m["Title"] for m in search_data["Search"]]
    selected_title = st.selectbox("Choose a movie:", titles)

    ratings = fetch_ratings(selected_title)
    if ratings is None:
        st.error("Rating data not found.")
        st.stop()

    df_plot = pd.DataFrame({
        "Source": ["IMDb", "Rotten Tomatoes", "Metacritic"],
        "Rating": [ratings["IMDb"], ratings["Rotten Tomatoes"], ratings["Metacritic"]]
    }).dropna()

    fig = graph.multi_dot_plot(df_plot, selected_title)
    st.pyplot(fig)

    st.dataframe(df_plot)
else:
    st.info("Type in a keyword to search movies and plot ratings. (DOES NOT FUNCTION)")

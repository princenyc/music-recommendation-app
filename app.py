import streamlit as st
import requests

# Load API key from secrets
api_key = st.secrets["lastfm"]["api_key"]

# Title of the app
st.title("Music Recommendation App")

# User inputs
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

# API call function
def get_recommendations(song, artist):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getsimilar",
        "artist": artist,
        "track": song,
        "api_key": api_key,
        "format": "json",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Display recommendations
if st.button("Submit"):
    recommendations = get_recommendations(song, artist)
    if recommendations and "similartracks" in recommendations:
        st.write("Here are some similar songs:")
        for track in recommendations["similartracks"]["track"][:5]:
            st.write(f"{track['name']} by {track['artist']['name']}")
    else:
        st.write("No recommendations found.")


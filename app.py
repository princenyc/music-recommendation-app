import streamlit as st
import requests
from datetime import datetime, timedelta

# Spotify API credentials
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]

# Global token variables
access_token = None
token_expiry_time = datetime.now()

def get_spotify_token():
    global access_token, token_expiry_time
    if access_token is None or datetime.now() >= token_expiry_time:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {st.secrets['spotify']['client_id']}:{st.secrets['spotify']['client_secret']}"
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info["access_token"]
            token_expiry_time = datetime.now() + timedelta(seconds=token_info["expires_in"])
        else:
            st.error("Failed to retrieve Spotify token")
    return access_token

def search_spotify(song, artist):
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/search?q=track:{song}%20artist:{artist}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Spotify Search Error: {response.status_code} - {response.text}")
        return None

def get_spotify_recommendations(track_id):
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/recommendations?limit=5&seed_tracks={track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Spotify Recommendations Error: {response.status_code} - {response.text}")
        return None

# Streamlit App UI
st.title("Music Recommendation App")
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

if st.button("Submit"):
    if song and artist:
        search_results = search_spotify(song, artist)
        if search_results:
            track_id = search_results["tracks"]["items"][0]["id"]
            st.write("Spotify Search Results:", search_results)
            recommendations = get_spotify_recommendations(track_id)
            if recommendations:
                st.write("Recommendations:", recommendations)
    else:
        st.error("Please enter both a song and an artist.")

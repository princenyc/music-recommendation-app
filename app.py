
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials from Streamlit secrets
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))


# Load API key from secrets
api_key = st.secrets["lastfm"]["api_key"]

# Title of the app
st.title("Music Recommendation App")

# User inputs
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

def get_spotify_recommendations(song, artist):
    # Search for the track
    results = sp.search(q=f"track:{song} artist:{artist}", type="track", limit=1)
    if results["tracks"]["items"]:
        track_id = results["tracks"]["items"][0]["id"]

        # Get recommendations based on the track
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        tracks = []
        for track in recommendations["tracks"]:
            tracks.append({
                "name": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "url": track["external_urls"]["spotify"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            })
        return tracks
    return None


if st.button("Submit"):
    recommendations = get_spotify_recommendations(song, artist)
    if recommendations:
        st.write("Here are some similar songs:")
        for track in recommendations:
            st.markdown(f"**{track['name']}** by *{track['artist']}*")
            if track["url"]:
                st.markdown(f"[Listen here]({track['url']})")
            if track["image"]:
                st.image(track["image"], width=200)
    else:
        st.write("No recommendations found.")


# Display recommendations
if st.button("Submit"):
    recommendations = get_recommendations(song, artist)
    if recommendations:
        st.write("Here are some similar songs:")
        for track in recommendations:
            st.markdown(f"**{track['name']}** by *{track['artist']}*")  # Song and artist name
            if track["url"]:
                st.markdown(f"[Listen here]({track['url']})")  # Link to song
            if track["image"]:
                st.image(track["image"], width=200)  # Display image
    else:
        st.write("No recommendations found.")



import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai

# Spotify credentials from Streamlit secrets
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]

# OpenAI API Key
openai.api_key = st.secrets["openai"]["api_key"]

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Title of the app
st.title("Music Recommendation App")

# User inputs
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

# Function to get recommendations from Spotify
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

# Function to get additional recommendations from OpenAI
def get_openai_recommendations(song, artist, recommendations):
    track_descriptions = "\n".join([f"{track['name']} by {track['artist']}" for track in recommendations])
    prompt = f"Here is a list of songs similar to '{song}' by '{artist}':\n{track_descriptions}\n\nCan you suggest 5 more obscure songs based on this list?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response["choices"][0]["text"].strip()

# Display recommendations
if st.button("Submit"):
    recommendations = get_spotify_recommendations(song, artist)
    if recommendations:
        st.write("Here are some similar songs from Spotify:")
        for track in recommendations:
            st.markdown(f"**{track['name']}** by *{track['artist']}*")
            if track["url"]:
                st.markdown(f"[Listen here]({track['url']})")
            if track["image"]:
                st.image(track["image"], width=200)

        # Get additional obscure tracks from OpenAI
        st.write("Here are some additional obscure tracks:")
        obscure_tracks = get_openai_recommendations(song, artist, recommendations)
        st.markdown(obscure_tracks)
    else:
        st.write("No recommendations found.")

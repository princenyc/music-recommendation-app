import streamlit as st
import openai

# Load API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Function to get song recommendations using OpenAI
def get_recommendations(song, artist):
    try:
        # Use the latest ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music recommendation assistant. Suggest obscure songs similar to the user's input."},
                {"role": "user", "content": f"I like the song '{song}' by {artist}. Can you recommend similar songs?"}
            ]
        )
        recommendations = response["choices"][0]["message"]["content"]
        return recommendations
    except Exception as e:
        return f"Error fetching recommendations from OpenAI: {e}"

# Streamlit app UI
st.title("Music Recommendation App")

# Input fields
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

# Submit button
if st.button("Submit"):
    if song and artist:
        st.subheader(f"Recommendations for '{song}' by {artist}:")
        recommendations = get_recommendations(song, artist)
        st.write(recommendations)
    else:
        st.error("Please enter both a song and an artist.")

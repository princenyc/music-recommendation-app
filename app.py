import openai
import streamlit as st

# OpenAI API key
openai.api_key = "your_openai_api_key"

def get_music_recommendations(song, artist):
    """
    Use OpenAI API to get music recommendations based on the input song and artist.
    """
    try:
        prompt = (
            f"I am creating a music recommendation app. A user entered the song '{song}' by the artist '{artist}'. "
            "Suggest 5 obscure but high-quality songs similar in sound or theme to this input. "
            "Provide each recommendation as 'Song Title by Artist'."
        )
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            n=1,
        )
        recommendations = response.choices[0].text.strip().split("\n")
        return recommendations
    except Exception as e:
        st.error(f"Error fetching recommendations from OpenAI: {e}")
        return []

# Streamlit App Layout
st.title("Music Recommendation App")

st.write("Enter a song and artist to get obscure, high-quality recommendations!")

# Input fields
song = st.text_input("Enter a song:", value="Personal Jesus")
artist = st.text_input("Enter the artist:", value="Depeche Mode")

if st.button("Submit"):
    if song and artist:
        st.write(f"Recommendations for **{song}** by **{artist}**:")
        
        # Fetch recommendations
        recommendations = get_music_recommendations(song, artist)
        
        if recommendations:
            for rec in recommendations:
                st.write(f"- {rec}")
        else:
            st.write("No recommendations found. Try another input.")
    else:
        st.error("Please provide both a song and an artist!")

import openai
import streamlit as st

# OpenAI API key
openai.api_key = "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"

def get_music_recommendations(song, artist):
    """
    Use OpenAI API to get music recommendations based on the input song and artist.
    """
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a music expert that provides obscure yet high-quality song recommendations based on user input.",
            },
            {
                "role": "user",
                "content": f"A user entered the song '{song}' by the artist '{artist}'. Suggest 5 obscure but high-quality songs similar in sound or theme to this input. Provide each recommendation as 'Song Title by Artist'.",
            },
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )
        recommendations = response.choices[0].message["content"].strip().split("\n")
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

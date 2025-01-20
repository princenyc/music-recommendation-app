import openai
import streamlit as st

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

def get_recommendations(song, artist):
    try:
        # Use the ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music recommendation assistant. Suggest obscure songs similar to the user's input."},
                {"role": "user", "content": f"I like the song '{song}' by {artist}. Can you recommend similar songs?"}
            ]
        )
        recommendations = response['choices'][0]['message']['content']
        return recommendations
    except Exception as e:
        return f"Error fetching recommendations from OpenAI: {e}"

# Streamlit app
st.title("Music Recommendation App")

song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")
if st.button("Submit"):
    if song and artist:
        st.subheader(f"Recommendations for {song} by {artist}:")
        recommendations = get_recommendations(song, artist)
        st.write(recommendations)
    else:
        st.error("Please enter both a song and an artist.")

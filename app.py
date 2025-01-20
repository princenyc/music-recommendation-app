import streamlit as st
import openai

# Load API key from Streamlit secrets
try:
    openai.api_key = st.secrets["openai"]["api_key"]
except KeyError:
    st.error("OpenAI API key not found. Please configure secrets.")

# Function to generate song recommendations
def get_song_recommendations(song, artist):
    try:
        # Query OpenAI for recommendations
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music expert recommending obscure songs."},
                {"role": "user", "content": f"I love the song '{song}' by {artist}. Can you recommend 5 obscure but similar songs? Provide them as a list with brief descriptions."}
            ]
        )
        # Extract recommendations
        recommendations = response["choices"][0]["message"]["content"]
        return recommendations
    except Exception as e:
        return f"Error fetching recommendations: {str(e)}"

# Function to convert song titles to clickable links (YouTube or Spotify)
def generate_links(recommendations):
    song_links = []
    for line in recommendations.split("\n"):
        if line.strip():
            song_name = line.strip()
            query = song_name.replace(" ", "+")
            link = f"https://www.youtube.com/results?search_query={query}"
            song_links.append(f"- [{song_name}]({link})")
    return "\n".join(song_links)

# Streamlit app
st.title("Music Recommendation App")

# User input
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

# Submit button
if st.button("Submit"):
    if song and artist:
        st.subheader(f"Recommendations for '{song}' by {artist}:")
        recommendations = get_song_recommendations(song, artist)
        if "Error" not in recommendations:
            st.markdown(generate_links(recommendations), unsafe_allow_html=True)
        else:
            st.error(recommendations)
    else:
        st.error("Please provide both song and artist names.")

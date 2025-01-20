import streamlit as st

# Title of the app
st.title("Music Recommendation App")

# User inputs
song = st.text_input("Enter a song:")
artist = st.text_input("Enter the artist:")

# Display the input back to the user
if st.button("Submit"):
    st.write(f"You entered: {song} by {artist}")

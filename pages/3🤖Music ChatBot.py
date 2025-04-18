import streamlit as st
from utils import get_song_features, ask_gemini_about_song
import google.generativeai as genai

# Initialize chat history if not already stored
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page title and intro
st.title("🎵 Song Vibe Chatbot 🤖")
st.markdown("""
Welcome to our AI-powered music chatbot!

**Ask our AI about any song’s vibe**—whether it’s a sad jam or an upbeat bop, it’ll give you a mood check with personality!
""")

# Show chat history
for msg in st.session_state.chat_history:
    st.write(f"🗣️ You: {msg['user']}")
    st.write(f"🤖 AI: {msg['bot']}")

# User input
song_query = st.text_input("Ask about a song's vibe:")

# Response sanitizer to keep things appropriate
def sanitize_response(response):
    flagged_words = ["explicit", "violence", "drugs"]
    for word in flagged_words:
        if word in response.lower():
            return "⚠️ This response was flagged for inappropriate content."
    return response

if song_query:
    try:
        with st.spinner("Thinking..."):
            # Get audio features from Spotify
            features, track_name, artist = get_song_features(song_query)

            if not features:
                bot_response = "Sorry, I couldn't find that song. Please try another one."
            else:
                # Prepare prompt for Gemini
                prompt = f"""
                The user wants to know the vibe of a song. Based on these Spotify audio features:
                - Danceability: {features['danceability']}
                - Energy: {features['energy']}
                - Valence (happiness): {features['valence']}
                - Tempo: {features['tempo']}
                - Acousticness: {features['acousticness']}

                Provide a personality-rich, casual response about what vibe this song gives off.
                Song: {track_name} by {artist}
                """

                # Ask Gemini
                raw_response = ask_gemini_about_song(prompt)
                bot_response = sanitize_response(raw_response)

            # Update chat history and rerun
            st.session_state.chat_history.append({
                "user": song_query,
                "bot": bot_response
            })
            st.experimental_rerun()

    except Exception as e:
        st.error("Oops! Something went wrong. Please try again later.")
        st.code(str(e))


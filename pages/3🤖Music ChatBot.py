import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import google.generativeai as genai
import os

# 🔐 Set up credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"]
))

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# 🎧 Function to get song features
def get_song_features(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        artist = track['artists'][0]['name']
        name = track['name']
        features = sp.audio_features(track_id)[0]
        return features, name, artist
    else:
        return None, None, None

# 🤖 Function to ask Gemini
def ask_gemini_about_song(prompt):
    response = model.generate_content(prompt)
    return response.text

# 🔁 Track chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎀 Page layout
st.title("🎵 Song Vibe Chatbot 🤖")
st.markdown(\"\"\"
Welcome to our AI-powered music chatbot!  
**Ask our AI about any song’s vibe**—whether it’s a sad jam or an upbeat bop, it’ll give you a mood check with personality!
\"\"\")

# 🧼 Content filter
def sanitize_response(response):
    flagged_words = ["explicit", "violence", "drugs"]
    for word in flagged_words:
        if word in response.lower():
            return "⚠️ This response was flagged for inappropriate content."
    return response

# 🗣️ Show chat history
for msg in st.session_state.chat_history:
    st.write(f"🗣️ You: {msg['user']}")
    st.write(f"🤖 AI: {msg['bot']}")

# 🎤 User input
song_query = st.text_input("Ask about a song's vibe:")

if song_query:
    try:
        with st.spinner("Thinking..."):
            features, track_name, artist = get_song_features(song_query)

            if not features:
                bot_response = "Sorry, I couldn't find that song. Please try another one."
            else:
                prompt = f\"\"\"
                The user wants to know the vibe of a song. Based on these Spotify audio features:
                - Danceability: {features['danceability']}
                - Energy: {features['energy']}
                - Valence (happiness): {features['valence']}
                - Tempo: {features['tempo']}
                - Acousticness: {features['acousticness']}

                Provide a personality-rich, casual response about what vibe this song gives off.
                Song: {track_name} by {artist}
                \"\"\"
                raw_response = ask_gemini_about_song(prompt)
                bot_response = sanitize_response(raw_response)

            # 💬 Update chat history
            st.session_state.chat_history.append({
                "user": song_query,
                "bot": bot_response
            })
            st.experimental_rerun()

    except Exception as e:
        st.error("Oops! Something went wrong. Please try again later.")
        st.code(str(e))



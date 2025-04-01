import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #ffe6f0, #ffe6fa);
        color: #4d0039;
        font-family: 'Trebuchet MS', sans-serif;
    }

    h1, h2, h3, h4 {
        color: #cc0066;
    }

    .stButton>button {
        background-color: #ff66a3;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #ff3385;
    }

    .stTextInput>div>div>input {
        background-color: #fff0f5;
        border-radius: 10px;
        border: 1px solid #ff99cc;
    }

    img {
        border-radius: 20px;
        box-shadow: 0px 4px 20px rgba(204, 0, 102, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title Page
st.markdown("## 💕 Welcome to the Spotify Visualizer 💽")
st.markdown("Discover your favorite tracks in style! Search for a song or artist and enjoy the aesthetic 🎀")

# 🔑 Spotify Credentials (add yours here!)
CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# User Input
query = st.text_input("✨ Enter a song or artist name:")

# Search and Display
if query:
    with st.spinner("Finding your perfect track... 💫🎵"):
        results = sp.search(q=query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])

        if tracks:
            track = tracks[0]
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            album_cover_url = track['album']['images'][0]['url']

            # Layout with columns
            col1, col2 = st.columns([1, 2])

            with col1:
                response = requests.get(album_cover_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Album Cover", use_column_width=True)

            with col2:
                st.markdown(f"### 💖 {track_name} by {artist_name}")
                st.write(f"*From the album:* **{album_name}**")
        else:
            st.warning("No tracks found. Try a different search term 💔")

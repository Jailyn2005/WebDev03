import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
CLIENT_ID = "ebacc0035f8647088fd24e64db4ccd01"
CLIENT_SECRET = "b3c67ed940414fef919d08cef920e3df"

# Streamlit Page Config
st.set_page_config(page_title="Spotify Track Visualizer", layout="centered")

# Title and Description
st.title("🎶 Spotify Track Visualizer")
st.write("Enter a song or artist name to see the top result and its album cover.")

# Set up Spotify API client
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# User Input
query = st.text_input("🔍 Search for a song or artist:")

if query:
    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])

    if tracks:
        track = tracks[0]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        album_cover_url = track['album']['images'][0]['url']

        st.subheader(f"🎧 {track_name} by {artist_name}")
        st.write(f"From the album: *{album_name}*")

        # Display album cover
        response = requests.get(album_cover_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="Album Cover", use_container_width=True)
    else:
        st.warning("No tracks found. Please try a different search term.")

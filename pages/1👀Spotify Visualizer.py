import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt


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

    .stSelectbox > div {
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
st.markdown("Discover your favorite tracks in style! Search for a song or artist to enjoy the aesthetic and receive info and recommendations 🎀")

# 🔑 Spotify Credentials 
CLIENT_ID = "ebacc0035f8647088fd24e64db4ccd01"
CLIENT_SECRET = "b3c67ed940414fef919d08cef920e3df"


# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# User Input 1
query = st.text_input("✨ Enter a song or artist name:")

# Search and Display 1
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
                st.image(image, width=400)

            with col2:
                st.markdown(f"### 💖 {track_name} by {artist_name}")
                st.write(f"*From the album:* **{album_name}**")

            st.markdown("### 📀 Album Cover")
        else:
            st.warning("No tracks found. Try a different search term 💔")
st.markdown("---")
#User Input 2
st.markdown("Pick a genre and we'll show the most popular artists in that genre!🎤")

genres = {"Pop": "pop", "Rock": "rock", "Jazz":"jazz", "Hip-Hop":"hip hop", "EDM": "edm", "Reggaeton": "reggaeton", "Latin Pop": "latin pop", "Indie": "indie", "R&B": "r&b"}
selectedGenre= st.selectbox("🎼Choose a Genre:", list(genres.keys()))
def getPopularity(artist):
    return artists['popularity']


if st.button("Show Top Artists"):
    genre_for_spotify=genres[selectedGenre]
    results= sp.search(q=f"genre: {genre_for_spotify}", type='artist', limit=50)
    artists= results['artists']['items']

    all_artists=[]
    for artist in artists:
        name = artist['name']
        popularity= artist['popularity']
        all_artists.append((name, popularity))

    for i in range (len(all_artists)):
        for j in range(i+1, len (all_artists)):
            if all_artists[j][1] > all_artists[i][1]:
                all_artists[i], all_artists[j] = all_artists[j], all_artists[i]
    
    top_10= all_artists[:10]

    artist_names=[]
    popularity_scores=[]

    for artist in top_10:
        artist_names.append(artist[0])
        popularity_scores.append(artist[1])

        fig, ax= plt.subplots()
        ax.barh(artist_names, popularity_scores, color="pink")
        ax.invert_yaxis()
        ax.set_title(f"Top 10 {selectedGenre} Aristis by Popularity")
        ax.set_xlabel("Popularity Score")

        for index in range (len(artist_names)):
            ax.text (popularity_scores[index]+1, index, str(popularity_scores[index]), va='center')
    st.pyplot(fig)

st.markdown("---")
st.markdown("Enter your favorite artist to discover their top 10 tracks!🎙️")

name_artist= st.text_input("🎶 Enter the name of an artist:")

if st.button("Search Top Tracks") and name_artist:
    result2=sp.search(q=name_artist, type='artist', limit=1)
    artists2=result2['artists']['items']

    if len(artists2)==0:
        st.write("Artist not found. Try a different name.")
    else: 
        artist2= artists2[0]
        id_artist=artist2['id']
        name_artist=artist2['name']

        st.subheader(f"🏅Top Tracks for {name_artist}:")
        top_tracks=sp.artist_top_tracks(id_artist, country="US")["tracks"]

        for index in range(min(10, len(top_tracks))):
            track2=top_tracks[index]
            track_name2= track2['name']
            preview_url=track2['preview_url']
            album_image= track2['album']['images'][0]['url']
            spotify_url=track2['external_urls']['spotify']

            st.write(f"**{index + 1}. {track_name2}**")
            st.image(album_image, width=200)

            if preview_url:
                st.audio(preview_url)
            else: 
                st.markdown(
                    f' <a href="{spotify_url}" traget="_blank">👂Listen on Spotify!</a>',
                    unsafe_allow_html=True
                )






import streamlit as st
import google.generativeai as genai
import traceback
import base64
import requests

# ---- API Keys ----
CLIENT_ID = "ebacc0035f8647088fd24e64db4ccd01"
CLIENT_SECRET = "b3c67ed940414fef919d08cef920e3df"
GEMINI_API_KEY = "AIzaSyAR8fzlgtlQbc8I80Cf6XcqBtFg4EJ-pPA"

# ---- Setup Gemini ----
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- Helper: Get Spotify Token ----
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, headers=headers, data=data)
    token = response.json().get("access_token")
    return token

# ---- Helper: Get Track Features ----
def get_track_features(song_name):
    token = get_spotify_token()
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }

    search_url = f"https://api.spotify.com/v1/search"
    params = {
        "q": song_name,
        "type": "track",
        "limit": 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    tracks = response.json().get("tracks", {}).get("items", [])
    if not tracks:
        return None

    track = tracks[0]
    track_id = track["id"]
    audio_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    audio_response = requests.get(audio_url, headers=headers)
    audio_features = audio_response.json()

    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "valence": audio_features.get("valence", 0.0),
        "energy": audio_features.get("energy", 0.0),
        "danceability": audio_features.get("danceability", 0.0),
        "tempo": audio_features.get("tempo", 0.0)
    }

# ---- Helper: Get Gemini Response ----
def get_gemini_response(prompt, song_data):
    system_prompt = f"""
You are DJ Vibez, an AI music expert who gives fun and insightful breakdowns of song moods.
Use the following Spotify data to answer questions about the song's vibe:

🎵 Song: {song_data['name']}
🎤 Artist: {song_data['artist']}
💖 Valence: {song_data['valence']} (how happy/positive it is)
⚡ Energy: {song_data['energy']} (how intense or active it is)
🕺 Danceability: {song_data['danceability']} (how easy it is to dance to)
🎶 Tempo: {song_data['tempo']} BPM (beats per minute)

Answer the user’s questions with a confident, cheerful tone, like a music-obsessed bestie!
Now here’s the convo:
User: {prompt}
DJ Vibez:"""
    response = model.generate_content(system_prompt)
    return response.text.strip()

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="🎧 DJ Vibez: Your Song Mood Buddy", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #fff0f5;
        }
        .stChatMessage {
            background-color: #ffe6f0;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stButton > button {
            background-color: #ff69b4 !important;
            color: white !important;
            border-radius: 10px;
            font-weight: bold;
        }
        .css-1aumxhk {
            background: linear-gradient(to right, #ffdde1, #ee9ca7) !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Title + Description ----
st.title("🎧 Meet DJ Vibez 🎧")
st.write("Ask DJ Vibez about any song’s mood—whether it’s a sad jam or an upbeat bop, she’ll give you the vibe check with personality!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

song_query = st.text_input("💽 Enter a song name:")

if song_query:
    try:
        song_data = get_track_features(song_query)

        if song_data:
            st.success(f"🎶 Loaded: *{song_data['name']}* by *{song_data['artist']}*")

            st.subheader("🔍 Quick Vibe Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💖 Valence", f"{song_data['valence']*100:.1f}%", help="How positive the song feels")
                st.metric("⚡ Energy", f"{song_data['energy']*100:.1f}%", help="Intensity of the track")
            with col2:
                st.metric("🕺 Danceability", f"{song_data['danceability']*100:.1f}%", help="How danceable it is")
                st.metric("🎵 Tempo", f"{song_data['tempo']} BPM", help="Beats per minute")

            st.markdown("---")
            st.subheader("💡 Ask DJ Vibez a Question")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Is this a sad song?"):
                    st.session_state.user_input = "Is this a sad song?"
            with col2:
                if st.button("Would this fit a workout playlist?"):
                    st.session_state.user_input = "Would this fit a workout playlist?"
            with col3:
                if st.button("Describe this song’s energy"):
                    st.session_state.user_input = "Describe this song’s energy"

            user_input = st.chat_input("Type your own question about the vibe 💬")
            if "user_input" in st.session_state and st.session_state.user_input:
                user_input = st.session_state.user_input
                st.session_state.user_input = ""

            if user_input:
                try:
                    with st.spinner("DJ Vibez is listening... 🎧"):
                        history = "\n".join([f"User: {u}\nDJ Vibez: {a}" for u, a in st.session_state.chat_history])
                        prompt = f"{history}\nUser: {user_input}\nDJ Vibez:"
                        ai_response = get_gemini_response(prompt, song_data)
                    st.chat_message("user").write(user_input)
                    st.chat_message("assistant").write(ai_response)
                    st.session_state.chat_history.append((user_input, ai_response))
                except Exception as e:
                    st.error("⚠️ DJ Vibez ran into a hiccup.")
                    st.code(traceback.format_exc())

        else:
            st.warning("❗ Couldn’t fetch song info. Try again with a different song!")
    except Exception as e:
        st.error("🚨 Error fetching song data.")
        st.code(traceback.format_exc())


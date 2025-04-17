import streamlit as st
st.markdown(
    """
    <style>
        .main {
            background-color: #fff0f5;
        }
        h1, h2, h3, p {
            color: #cc0066;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        .intro-box {
            background-color: #ffe6f0;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px #f5c0d1;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of App
st.markdown("<h1 style='text-align: center;'>💖 Web Development Lab03 💖</h1>", unsafe_allow_html=True)

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 58, Web Development - Section A")
st.subheader("Jailyn Camille Wilkinson, Silvana Aristizabal Moreno")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.markdown("""
<div style="background-color: #ffe6f0; padding: 25px; border-radius: 20px; box-shadow: 0 0 10px #f5c0d1; margin-top: 20px;">

<h3 style="color: #cc0066;">🌟 Welcome to our Streamlit App!</h3>

<p style="color: #d63384; font-size: 16px;">
We're excited to have you here! Use the sidebar on the left to explore different pages in our interactive music app. Here's what each page does:
</p>

<ol style="color: #e60073; font-size: 16px;">
<li>🎧 <strong>Spotify Visualizer</strong><br>
Search for a song, artist, or genre to discover top tracks and visualize popular albums with cover art and vibes.
</li><br>

<li>🎵 <strong>Playlist Generator</strong><br>
Enter your mood, favorite genre, or artist and we’ll generate a personalized playlist just for you using live Spotify data.
</li><br>

<li>🤖 <strong>Music ChatBot</strong><br>
Ask our AI about any song’s vibe—whether it’s a sad jam or an upbeat bop, it’ll give you a mood check with personality!
</li>
</ol>

</div>
""", unsafe_allow_html=True)



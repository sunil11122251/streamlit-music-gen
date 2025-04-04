# app.py
import streamlit as st
import mido
import numpy as np
import pygame
import os
from mido import MidiFile, MidiTrack, Message

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to generate distinct MIDI melodies based on mood
def generate_music(mood, tempo, duration=12):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

    # Define unique note patterns and characteristics for each mood
    if mood == "Happy":
        notes = [60, 62, 64, 67, 69, 71, 72]  # C Major scale (C4 to C5)
        velocity = 100
        time_on = 400  # Fast, upbeat rhythm
        time_off = 100
    elif mood == "Sad":
        notes = [57, 59, 60, 62, 64, 65, 67]  # A Minor scale (A3 to G4)
        velocity = 60
        time_on = 800  # Slow, mournful rhythm
        time_off = 200
    elif mood == "Calm":
        notes = [60, 64, 67, 71, 74]  # C Major pentatonic (C4 to D5)
        velocity = 80
        time_on = 600  # Gentle, flowing rhythm
        time_off = 150
    elif mood == "Energetic":
        notes = [62, 65, 67, 69, 72, 74, 77]  # D Major scale (D4 to F#5)
        velocity = 110
        time_on = 300  # Quick, driving rhythm
        time_off = 50
    elif mood == "Mysterious":
        notes = [58, 61, 63, 66, 68, 70, 73]  # F# Minor scale (F#3 to E5)
        velocity = 70
        time_on = 500  # Erratic, suspenseful rhythm
        time_off = 300

    # Generate melody with variation
    time = 0
    for _ in range(duration):
        np.random.shuffle(notes)  # Randomize note order for variety
        for note in notes[:4]:   # Use 4 notes per cycle
            track.append(Message('note_on', note=note, velocity=velocity, time=time))
            time = time_on
            track.append(Message('note_off', note=note, velocity=0, time=time))
            time = time_off

    # Save MIDI file
    output_file = "generated_music.mid"
    mid.save(output_file)
    return output_file

# Inject attractive CSS styles
st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle, #ff6b6b, #4ecdc4, #45b7d1);
        padding: 40px;
        border-radius: 20px;
        max-width: 1000px;
        margin: 30px auto;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 40px;
        text-transform: uppercase;
        text-shadow: 0 0 10px #ffeb3b, 0 0 20px #ff5722, 0 0 30px #e91e63;
        margin-bottom: 15px;
    }
    .stMarkdown p {
        color: #f0f0f0;
        text-align: center;
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        margin-bottom: 25px;
    }
    .stSelectbox, .stSlider {
        background-color: rgba(255, 255, 255, 0.9);
        border: 3px solid #ffeb3b;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stSelectbox:hover, .stSlider:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #ffeb3b;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff5722, #ffeb3b);
        color: #ffffff;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-family: 'Montserrat', sans-serif;
        font-size: 16px;
        font-weight: bold;
        text-transform: uppercase;
        transition: all 0.3s ease;
        animation: pulse 1.5s infinite;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #e91e63, #ffeb3b);
        transform: scale(1.1);
        box-shadow: 0 0 20px #ff5722;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stDownloadButton>button {
        background-color: #4ecdc4;
        color: #ffffff;
        border-radius: 15px;
        padding: 10px 20px;
        font-family: 'Lato', sans-serif;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #45b7d1;
        transform: scale(1.05);
    }
    .stError {
        background: linear-gradient(90deg, #ff9999, #ff6666);
        color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-family: 'Lato', sans-serif;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Lato:wght@400;700&display=swap');
    </style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.title("Music Mood Generator")
st.write("Pick a mood and tempo to create your own melody!")

# User inputs
mood = st.selectbox("Choose a Mood", ["Happy", "Sad", "Calm", "Energetic", "Mysterious"])
tempo = st.slider("Select Tempo (BPM)", 60, 180, 120)

# Generate music button
if st.button("Generate Music"):
    try:
        # Generate the MIDI file
        midi_file = generate_music(mood, tempo)
        
        # Play the music locally (pygame)
        pygame.mixer.music.load(midi_file)
        pygame.mixer.music.play()
        
        # Inform user and provide download
        st.write("Music is playing! Check your system audio.")
        with open(midi_file, "rb") as f:
            st.download_button("Download Your Melody (MIDI)", f, file_name="my_melody.mid")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Clean up
if os.path.exists("generated_music.mid"):
    os.remove("generated_music.mid")
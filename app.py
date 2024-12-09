import streamlit as st
import soundfile as sf
import io
import os
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime

# Function 1: Play "engineer_diagnosis.wav" file from GitHub repo (local directory)
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Record voice, save as mp3, and allow playback
def record_voice():
    st.header("Function 2: Record Voice")
    
    # Record audio
    audio_bytes = st.file_uploader("Record or upload your voice", type=["wav"])
    if audio_bytes is not None:
        # Save the recorded audio as MP3
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes.read()), format="wav")
        file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio.export(file_name, format="mp3")
        st.success(f"Audio recorded and saved as {file_name}")
        st.audio(file_name, format="audio/mp3")

# Function 3: Play "electric_unit_heater.wav" file from GitHub repo (local directory)
def play_electric_unit_heater():
    st.header("Function 3: Play 'electric_unit_heater.wav'")
    file_path = "electric_unit_heater.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'electric_unit_heater.wav' not found!")

# Main App
st.title("Audio Demo App")

# Sequential execution of functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

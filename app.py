import streamlit as st
import soundfile as sf
import io
import os
import wave
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np
import zipfile
import subprocess
from st_audiorecorder import audio_recorder
from pydub import AudioSegment

# Function 1: Play "engineer_diagnosis.wav" file from GitHub repo (local directory)
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Record voice, save as wav, and allow playback
def record_voice():
    st.header("Function 2: Record Voice")
# Record audio
    audio_data = audio_recorder()
    
    if audio_data:
        # Save the recorded audio as WAV
        wav_file = io.BytesIO(audio_data)  # Convert byte data to file-like object for pydub
        audio = AudioSegment.from_file(wav_file, format="wav")
    
        # Convert and save as MP3
        mp3_file_path = "recorded_audio.mp3"
        audio.export(mp3_file_path, format="mp3")
    
        # Display success message and play the MP3
        st.success("Audio recorded and saved successfully as MP3!")
        st.audio(mp3_file_path, format="audio/mp3")

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

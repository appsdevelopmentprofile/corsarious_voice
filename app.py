import streamlit as st
import soundfile as sf
import io
import os
import wave
from datetime import datetime
from st_audiorecorder import st_audiorecorder
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
    # Record audio using Streamlit Audio Recorder
    audio_data = st_audiorecorder()

    if audio_data:
        # Save the recorded audio as WAV
        wav_file = io.BytesIO(audio_data)  # Convert byte data to file-like object for pydub
        audio = AudioSegment.from_file(wav_file, format="wav")
    
        # Save WAV file
        wav_file_path = "recorded_audio.wav"
        audio.export(wav_file_path, format="wav")
    
        # Display success message and play the WAV file
        st.success("Audio recorded and saved successfully as WAV!")
        st.audio(wav_file_path, format="audio/wav")

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

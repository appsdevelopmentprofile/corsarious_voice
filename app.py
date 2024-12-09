import streamlit as st
import sounddevice as sd
import soundfile as sf
import os
import wave
import numpy as np
from datetime import datetime

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
    
    # Recording parameters
    sample_rate = 44100  # Sample rate in Hz
    duration = 5  # Duration of recording in seconds

    st.write("Press the button below to start recording.")
    
    if st.button("Start Recording"):
        st.write("Recording... Speak into your microphone.")
        
        # Record the audio
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is finished

        # Save the recorded audio to a file
        file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        sf.write(file_name, audio_data, sample_rate)

        st.success(f"Audio recorded and saved as {file_name}")
        st.audio(file_name, format="audio/wav")

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

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

    # Path to the ZIP file containing the pyaudio package
    zip_file_path = "pyaudio.zip"
    extract_dir = "pyaudio"

    # Step 1: Extract the ZIP file if it hasn't been extracted yet
    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        st.success("pyaudio.zip extracted successfully.")

    # Step 2: Run setup.py from the extracted directory
    try:
        result = subprocess.run(
            ['python', f'{extract_dir}/setup.py', 'install'],
            check=True,
            text=True,
            capture_output=True
        )
        st.success("pyaudio setup completed successfully.")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to run setup.py: {e.output}")
        return  # Stop further execution if setup fails

    # Using WebRTC for real-time audio recording
    webrtc_ctx = webrtc_streamer(
        key="record-voice",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    )
    
    if webrtc_ctx and webrtc_ctx.state.playing:
        audio_frames = []
        sample_rate = 16000  # Default sample rate

        # Mock recording logic for demonstration
        st.write("Recording... Speak into your microphone.")

        # Placeholder for actual audio data
        audio_data = np.random.randn(sample_rate * 5).astype(np.float32)  # Simulating 5 seconds of audio
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

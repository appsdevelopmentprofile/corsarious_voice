import streamlit as st
import soundfile as sf
import os
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np

# Function 1: Play "engineer_diagnosis.wav" file from GitHub repo (local directory)
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Continuously record voice, save as wav, and allow playback
def record_voice():
    st.header("Function 2: Record Voice")

    # Using WebRTC for real-time audio recording
    webrtc_ctx = webrtc_streamer(
        key="record-voice",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    )

    if webrtc_ctx and webrtc_ctx.state.playing:
        st.write("Recording... Speak into your microphone.")
        
        # Retrieve audio frames and process
        audio_frames = webrtc_ctx.audio_frames
        if audio_frames:
            audio_data = np.concatenate(audio_frames)
            sample_rate = 16000  # Adjust if needed

            # Save the recording to a file
            file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            sf.write(file_name, audio_data, sample_rate)
            
            st.success(f"Audio recorded and saved as {file_name}")
            st.audio(file_name, format="audio/wav")
        else:
            st.warning("No audio data available. Make sure your microphone is active.")

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

# Initialize the recording function to run as soon as the app starts
record_voice()

# Display buttons for other functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 3: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

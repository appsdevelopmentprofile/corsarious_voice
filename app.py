import streamlit as st
import soundfile as sf
import os
import wave
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, WebRtcStreamerContext
import numpy as np

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

    # Using WebRTC for real-time audio recording
    webrtc_ctx = webrtc_streamer(
        key="record-voice",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    )

    # A variable to hold recorded audio data in chunks
    audio_frames = []
    sample_rate = 16000  # Set the sample rate for audio recording

    # If the context is active, keep recording
    while webrtc_ctx and webrtc_ctx.state.playing:
        # Capture audio frames
        if webrtc_ctx.audio_frames:
            audio_frames.extend(webrtc_ctx.audio_frames)

        # When recording is done or user stops the app, save the file
        if not webrtc_ctx.state.playing:
            if audio_frames:
                audio_data = np.concatenate(audio_frames)
                file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                sf.write(file_name, audio_data, sample_rate)
                st.success(f"Audio recorded and saved as {file_name}")
                st.audio(file_name, format="audio/wav")
                break  # Exit the loop once recording is done

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
play_engineer_diagnosis()
record_voice()  # Start the recording function when the app loads
play_electric_unit_heater()

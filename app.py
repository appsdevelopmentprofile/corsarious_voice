import streamlit as st
import soundfile as sf
import os
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

    # Wait until the context is initialized and ready for recording
    if webrtc_ctx is not None:
        if webrtc_ctx.state.playing:
            st.write("Recording... Speak into your microphone.")
            
            # Capture and save audio data
            audio_frames = []
            sample_rate = 16000  # Set a sample rate for audio recording

            # Monitor the audio frame state
            while webrtc_ctx.state.playing:
                if webrtc_ctx.audio_frames:
                    audio_frames.extend(webrtc_ctx.audio_frames)
                
                # Break the loop if user stops the app or disconnects
                if not webrtc_ctx.state.playing:
                    break

            if audio_frames:
                # Concatenate all audio frames to form the complete audio
                audio_data = np.concatenate(audio_frames)
                file_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                sf.write(file_name, audio_data, sample_rate)
                st.success(f"Audio recorded and saved as {file_name}")
                st.audio(file_name, format="audio/wav")
        else:
            st.error("WebRTC context is not in a playing state. Please check your connection.")
    else:
        st.error("Failed to initialize the WebRTC context. Ensure your browser has microphone access and WebRTC is supported.")

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

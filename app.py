import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import soundfile as sf
import numpy as np
import os
from datetime import datetime

# Function 1: Play "engineer_diagnosis.wav" file from GitHub repo (local directory)
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Record voice, save as WAV, and allow playback
def record_voice():
    st.header("Function 2: Record Voice")

    # Using WebRTC for audio recording
    def audio_callback(frame: np.ndarray, sample_rate: int):
        return frame, sample_rate

    webrtc_ctx = webrtc_streamer(
        key="record-voice",
        mode=WebRtcMode.SENDRECV,
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"audio": True, "video": False},
        ),
        audio_receiver_size=1024,
        sendback_audio=False,
    )

    if webrtc_ctx and webrtc_ctx.audio_receiver:
        audio_frames = []
        sample_rate = None

        # Fetch audio frames
        while True:
            try:
                audio_frame = webrtc_ctx.audio_receiver.get_audio_frame(timeout=1)
                if sample_rate is None:
                    sample_rate = audio_frame.sample_rate
                audio_frames.append(audio_frame.to_ndarray())
            except:
                break

        if audio_frames:
            # Combine and save audio
            audio_data = np.concatenate(audio_frames, axis=0)
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

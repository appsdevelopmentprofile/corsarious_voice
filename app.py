import streamlit as st
import soundfile as sf
import pydub
import os
import wave
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

# Function 2: Record voice, save as MP3, and allow playback
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
        audio_frames = []

        # Collect audio data in real-time
        for audio_frame in webrtc_ctx.audio_frames:
            audio_frames.append(audio_frame)

        if audio_frames:
            # Combine audio frames into a single NumPy array
            audio_data = np.concatenate(audio_frames)
            sample_rate = 16000  # Adjust if necessary

            # Save the audio data as a WAV file temporarily
            temp_wav_file = f"temp_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            sf.write(temp_wav_file, audio_data, sample_rate)

            # Convert the WAV file to MP3 format using pydub
            mp3_file_name = temp_wav_file.replace(".wav", ".mp3")
            audio_segment = pydub.AudioSegment.from_wav(temp_wav_file)
            audio_segment.export(mp3_file_name, format="mp3")

            # Clean up the temporary WAV file
            os.remove(temp_wav_file)

            st.success(f"Audio recorded and saved as {mp3_file_name}")
            st.audio(mp3_file_name, format="audio/mp3")
        else:
            st.warning("No audio data available. Ensure your microphone is active.")

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

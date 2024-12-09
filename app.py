import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode, ClientSettings
import soundfile as sf
import io
import os
import wave
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
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv_audio(self, frame):
        self.audio_frames.append(frame.to_ndarray())
        return frame

def record_voice():
    st.header("Function 2: Record Voice")
    
    audio_processor = webrtc_streamer(
        key="voice-recorder",
        mode=WebRtcMode.SENDONLY,
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"audio": True, "video": False},
        ),
        audio_processor_factory=AudioProcessor,
    )

    if audio_processor and audio_processor.audio_frames:
        # Save the recorded audio
        audio_frames = audio_processor.audio_frames
        audio_file_path = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        with sf.SoundFile(audio_file_path, mode='w', samplerate=44100, channels=1, subtype="PCM_16") as f:
            for frame in audio_frames:
                f.write(frame)
        
        st.success(f"Audio recorded and saved as {audio_file_path}")
        st.audio(audio_file_path, format="audio/wav")

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

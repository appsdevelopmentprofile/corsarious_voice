import streamlit as st
import os
import subprocess
from pydub import AudioSegment

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/"

# Function to check if ffmpeg is accessible
def check_ffmpeg():
    try:
        # Run ffmpeg command to check its version
        result = subprocess.run(['sudo', 'ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Display the output in Streamlit
        ffmpeg_version = result.stdout
        st.write("FFmpeg version detected successfully:")
        st.write(ffmpeg_version)
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not found in the specified path.")
    except PermissionError:
        st.error("Permission denied while trying to run ffmpeg with sudo.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app title
st.title("FFmpeg Integration Example")

# Button to check FFmpeg version
if st.button("Check FFmpeg Version"):
    check_ffmpeg()

# Function 1: Play "engineer_diagnosis.wav" file from GitHub repo (local directory)
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Record voice, save as wav, and allow playback
import streamlit as st
import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
from pydub import AudioSegment

# Globals
recording = None
recording_state = False

# Set audio properties
SAMPLE_RATE = 44100  # Sample rate for recording
CHANNELS = 1         # Mono audio

# Function to start recording
def start_recording():
    global recording, recording_state
    st.session_state["recording"] = []
    st.session_state["recording_state"] = True

    # Callback to capture audio chunks
    def audio_callback(indata, frames, time, status):
        st.session_state["recording"].append(indata.copy())

    # Start audio recording
    st.session_state["stream"] = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback
    )
    st.session_state["stream"].start()

    st.success("Recording started! Click 'Stop Recording' to finish.")

# Function to stop recording and save as MP3
def stop_recording():
    if "stream" in st.session_state and st.session_state["stream"].active:
        st.session_state["stream"].stop()
        st.session_state["stream"].close()
        st.session_state["recording_state"] = False

        # Combine audio chunks
        audio_data = np.concatenate(st.session_state["recording"])
        wav_file_path = "recorded_audio.wav"
        write(wav_file_path, SAMPLE_RATE, audio_data)

        # Convert to MP3
        mp3_file_path = "recorded_audio.mp3"
        audio_segment = AudioSegment.from_wav(wav_file_path)
        audio_segment.export(mp3_file_path, format="mp3")

        st.success(f"Recording saved as {mp3_file_path}!")
        st.audio(mp3_file_path, format="audio/mp3")

# Streamlit App
st.title("Audio Recorder Example")

# Button to start recording
if st.button("Start Recording"):
    if "recording_state" in st.session_state and st.session_state["recording_state"]:
        st.warning("Recording is already in progress!")
    else:
        start_recording()

# Button to stop recording
if st.button("Stop Recording"):
    if "recording_state" in st.session_state and st.session_state["recording_state"]:
        stop_recording()
    else:
        st.warning("No recording in progress to stop.")


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

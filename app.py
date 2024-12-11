import streamlit as st
import os
import subprocess
import io
from pydub import AudioSegment
import speech_recognition as sr

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/"

# Set the path to the ffprobe binary
os.environ["FFPROBE_BINARY"] = "/Users/juanrivera/Downloads/ffmpeg-7.0.2-i686-static/ffprobe"


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
def record_voice():
    st.header("Function 2: Record Voice")

    # Upload an audio file (only wav or mp3)
    uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])
        
    if uploaded_file is not None:
        # Convert uploaded audio to AudioSegment
        audio = AudioSegment.from_file(uploaded_file)
            
        # Save the uploaded audio as WAV
        wav_file_path = "uploaded_audio.wav"
        audio.export(wav_file_path, format="wav")
            
        # Display success message and play the audio
        st.success(f"Audio uploaded and saved as {wav_file_path}!")
        st.audio(wav_file_path, format="audio/wav")
            
        # Optionally save as MP3 as well
        mp3_file_path = "uploaded_audio.mp3"
        audio.export(mp3_file_path, format="mp3")
        st.audio(mp3_file_path, format="audio/mp3")

# Function 3: Play "electric_unit_heater.wav" file from GitHub repo (local directory)
def play_electric_unit_heater():
    st.header("Function 3: Play 'electric_unit_heater.wav'")
    file_path = "electric_unit_heater.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'electric_unit_heater.wav' not found!")

# Function 4: Speech-to-Text from "engineer_equipment.mp3"
def transcribe_engineer_equipment():
    st.header("Function 4: Transcribe 'engineer_equipment.mp3'")
    file_path = "engineer_equipment.mp3"
    if os.path.exists(file_path):
        st.success(f"Processing file: {file_path}")
        
        # Convert MP3 to WAV for compatibility
        audio = AudioSegment.from_file(file_path)
        wav_file_path = "engineer_equipment_converted.wav"
        audio.export(wav_file_path, format="wav")
        
        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_recorded = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_recorded)
                st.subheader("Recognized Text:")
                st.write(text)
            except sr.UnknownValueError:
                st.error("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
    else:
        st.error("File 'engineer_equipment.mp3' not found!")

# Main App
st.title("Audio Demo App")

# Sequential execution of functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

if st.button("Start Function 4: Transcribe 'engineer_equipment.mp3'"):
    transcribe_engineer_equipment()

import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
import io

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/local/bin/ffprobe"

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
st.title("FFmpeg and Speech-to-Text Integration Example")

# Button to check FFmpeg version
if st.button("Check FFmpeg Version"):
    check_ffmpeg()

# Function 1: Play "electric_unit_heater.wav" file from GitHub repo (local directory)
def play_electric_unit_heater():
    st.header("Function 1: Play 'electric_unit_heater.wav'")
    file_path = "electric_unit_heater.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'electric_unit_heater.wav' not found!")

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

# Function 3: Convert speech from wav file to text using Google Speech Recognition
def recognize_speech_from_wav(wav_file):
    recognizer = sr.Recognizer()

    # Load the .wav file
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)
        try:
            # Use Google Web Speech API to recognize the speech
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Speech not recognized"
        except sr.RequestError as e:
            return f"Error with the request: {e}"

# Function 4: Process the "electric_unit_heater.wav" file
def process_electric_unit_heater():
    st.header("Function 4: Recognize Speech from 'engineer_equipment.wav'")

    wav_file = "engineer_equipment.wav"
   
    if os.path.exists(wav_file):
        # Convert the speech in the .wav file to text
        recognized_text = recognize_speech_from_wav(wav_file)
        st.write(f"Recognized Text: {recognized_text}")
    else:
        st.error(f"File '{wav_file}' not found!")

# Main App
st.title("Audio Demo App with Speech-to-Text")

# Sequential execution of functions
if st.button("Start Function 1: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Recognize Speech from 'engineer_equipment.wav'"):
    process_electric_unit_heater()

import time
import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
import io
from docx import Document

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/local/bin/ffprobe"

# Function to check if ffmpeg is accessible
def check_ffmpeg():
    try:
        result = subprocess.run(['sudo', 'ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
    uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])

    if uploaded_file is not None:
        audio = AudioSegment.from_file(uploaded_file)
        wav_file_path = "uploaded_audio.wav"
        audio.export(wav_file_path, format="wav")
        st.success(f"Audio uploaded and saved as {wav_file_path}!")
        st.audio(wav_file_path, format="audio/wav")
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
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Speech not recognized"
        except sr.RequestError as e:
            return f"Error with the request: {e}"

# Function 4: Process the "electric_unit_heater.wav" file
def process_electric_unit_heater():
    st.header("Function 4: Recognize Speech from 'electric_unit_heater.wav'")
    wav_file = "electric_unit_heater.wav"
    if os.path.exists(wav_file):
        recognized_text = recognize_speech_from_wav(wav_file)
        st.write(f"Recognized Text: {recognized_text}")
    else:
        st.error(f"File '{wav_file}' not found!")

# Function 5: Generate a checklist document after phases 1-4
def create_checklist_doc_from_speech(text):
    # Create a new Document
    doc = Document()
    doc.add_heading('Field Engineer Questionnaire', 0)

    # Add a table with 2 columns
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Question'
    hdr_cells[1].text = 'Answer (YES/NO)'

    lines = text.split(".")  # Split by periods for simplicity
    for line in lines:
        line = line.strip()
        if line:
            row_cells = table.add_row().cells
            row_cells[0].text = line  # Add the question
            row_cells[1].text = '☐ YES ☐ NO'  # Placeholder for the "YES/NO" selection

    # Save the document
    doc.save('field_engineer_checklist_from_speech.docx')
    st.success("Checklist document created successfully based on speech recognition.")

# Main function to process the WAV file and create the document
def process_audio_and_create_doc(file_path):
    st.write("Recognizing speech from audio file...")
    recognized_text = recognize_speech_from_wav(file_path)
    st.write(f"Recognized text: {recognized_text}")

    st.write("Creating checklist document...")
    create_checklist_doc_from_speech(recognized_text)

# Main App
st.title("Audio Demo App with Speech-to-Text")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file (WAV/MP3)", type=["wav", "mp3"])

if uploaded_file is not None:
    audio = AudioSegment.from_file(uploaded_file)
    wav_file_path = "uploaded_audio.wav"
    audio.export(wav_file_path, format="wav")
    st.success(f"Audio uploaded and saved as {wav_file_path}!")

    # Option to process the audio and generate a document
    if st.button("Generate Checklist Document"):
        process_audio_and_create_doc(wav_file_path)

# Sequential execution of functions
if st.button("Start Function 1: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Recognize Speech from 'electric_unit_heater.wav'"):
    process_electric_unit_heater()

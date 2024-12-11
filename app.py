import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
from docx import Document
from io import BytesIO

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/usr/local/bin/ffprobe"

# Function to check if ffmpeg is accessible
def check_ffmpeg():
    try:
        # Run ffmpeg command to check its version
        result = subprocess.run(['sudo', 'ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        st.write("FFmpeg version detected successfully:")
        st.write(result.stdout)
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not found in the specified path.")
    except PermissionError:
        st.error("Permission denied while trying to run ffmpeg with sudo.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function 1: Play "engineer_diagnosis.wav" file from local directory
def play_engineer_diagnosis():
    st.header("Stage 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Function 2: Record voice, save as wav, and allow playback
def record_voice():
    st.header("Stage 2: Record Voice")
    uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])
    if uploaded_file:
        audio = AudioSegment.from_file(uploaded_file)
        wav_file_path = "uploaded_audio.wav"
        audio.export(wav_file_path, format="wav")
        st.success(f"Audio uploaded and saved as {wav_file_path}!")
        st.audio(wav_file_path, format="audio/wav")

# Function 3: Convert speech from "electric_unit_heater.wav" file to text using Google Speech Recognition
def process_speech_to_text():
    st.header("Stage 3: Recognize Speech from 'electric_unit_heater.wav'")
    wav_file = "electric_unit_heater.wav"
    if os.path.exists(wav_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.write("Recognized Text:")
                sentences = text.split('.')
                for i, sentence in enumerate(sentences, 1):
                    st.write(f"{i}. {sentence.strip()}")
                return sentences
            except sr.UnknownValueError:
                st.error("Speech not recognized.")
            except sr.RequestError as e:
                st.error(f"Error with the request: {e}")
    else:
        st.error(f"File '{wav_file}' not found!")
    return []

# Function 4: Create a checklist from recognized speech
def create_checklist_document(sentences):
    st.header("Stage 4: Create Checklist from Recognized Speech")
    if not sentences:
        st.error("No sentences provided to generate the checklist.")
        return

    # Create document
    document = Document()
    document.add_heading('Field Engineer Checklist', level=1)

    table = document.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Question'
    hdr_cells[1].text = 'Answer (YES/NO)'

    for sentence in sentences:
        if sentence.strip():
            row_cells = table.add_row().cells
            row_cells[0].text = sentence.strip()
            row_cells[1].text = '☐ YES ☐ NO'

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Display first page content in Streamlit
    st.write("Preview of Checklist Document (First Page):")
    for para in document.paragraphs[:5]:  # Display first 5 paragraphs as an approximation of the first page
        st.write(para.text)

    # Download button
    st.download_button(
        label="Download Checklist Document",
        data=buffer,
        file_name="field_engineer_checklist.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# Main App
st.title("Audio Processing App with Stages")

if st.button("Stage 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Stage 2: Record Voice"):
    record_voice()

# Trigger Stage 4 automatically after Stage 3 (if text is recognized)
if st.button("Stage 3: Recognize Speech from 'electric_unit_heater.wav'"):
    sentences = process_speech_to_text()
    if sentences:
        create_checklist_document(sentences)  # Automatically trigger Stage 4 once text is recognized

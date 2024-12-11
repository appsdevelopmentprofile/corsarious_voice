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

# Function 3: Convert speech from "electric_unit_heater.wav" file to text using Google Speech Recognition
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

# Function 4: Process the "electric_unit_heater.wav" file and create a checklist
def process_and_create_checklist():
    st.header("Stage 4: Create Checklist from Recognized Speech")

    wav_file = "electric_unit_heater.wav"
    
    if os.path.exists(wav_file):
        # Convert the speech in the .wav file to text
        recognized_text = recognize_speech_from_wav(wav_file)
        st.write(f"Recognized Text: {recognized_text}")

        # Create a checklist document
        document = Document()
        document.add_heading('Field Engineer Checklist', level=1)

        # Add a table to the document
        table = document.add_table(rows=1, cols=2)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Question'
        hdr_cells[1].text = 'Answer (YES/NO)'

        # Split the text into sentences to create questions
        questions = recognized_text.split('.')
        for question in questions:
            question = question.strip()
            if question:
                row_cells = table.add_row().cells
                row_cells[0].text = question
                row_cells[1].text = '☐ YES ☐ NO'

        # Save the document to a BytesIO buffer
        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)

        # Allow download of the file
        st.download_button(
            label="Download Checklist Document",
            data=buffer,
            file_name="field_engineer_checklist.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error(f"File '{wav_file}' not found!")

# Main App
st.title("Audio Processing App with Stages")

# Stage execution
if st.button("Stage 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Stage 2: Record Voice"):
    record_voice()

if st.button("Stage 3: Recognize Speech from 'electric_unit_heater.wav'"):
    recognize_speech_from_wav("electric_unit_heater.wav")

if st.button("Stage 4: Create Checklist Document"):
    process_and_create_checklist()

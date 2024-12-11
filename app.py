import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
import io
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import time

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

# Function 3: Play "engineer_equipment.wav" file from GitHub repo (local directory) and recognize speech
def recognize_speech_from_wav(file_path):
    recognizer = sr.Recognizer()
    
    # Export the audio as raw audio data in bytes (for speech_recognition to process)
    audio_data = io.BytesIO()
    audio = AudioSegment.from_wav(file_path)
    audio.export(audio_data, format="wav")
    audio_data.seek(0)  # Go to the beginning of the audio data

    # Recognize speech from the audio data
    with sr.AudioFile(audio_data) as source:
        audio_recorded = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_recorded)
            return text.lower()  # Return the recognized text in lowercase
        except sr.UnknownValueError:
            return "unrecognized"
        except sr.RequestError as e:
            return f"error: {e}"

def play_electric_unit_heater():
    st.header("Function 3: Play 'engineer_equipment.wav' and recognize speech")

    file_path = "engineer_equipment.wav"
    if os.path.exists(file_path):
        # Show and play the audio file in the frontend
        st.audio(file_path, format="audio/wav")

        # Recognize speech from the audio file
        recognized_text = recognize_speech_from_wav(file_path)
        st.subheader("Recognized Text:")
        st.write(recognized_text)

    else:
        st.error("File 'engineer_equipment.wav' not found!")

# Function 5: Create checklist document and display progress
def create_checklist_doc(text):
    # Create a new Document
    doc = Document()

    # Title of the document
    doc.add_heading('Field Engineer Questionnaire', 0)

    # Split the text from the MP3 file into checklist items (assumes text is already formatted appropriately)
    lines = text.split(".")  # Basic split by periods. Adjust if needed for your specific use case.

    # Create a checklist based on the extracted text
    for line in lines:
        line = line.strip()
        if line:
            p = doc.add_paragraph(style='List Checkmark')  # Adding a checkbox-style paragraph
            p.add_run(f'☐ {line}')  # Use checkbox character for the checklist item

    # Add a comment section at the bottom
    doc.add_paragraph("\n")
    doc.add_heading('Comments', level=2)
    doc.add_paragraph("Please add any additional comments here:")

    # Save the document
    doc.save("field_engineer_checklist.docx")
    st.success("Document 'field_engineer_checklist.docx' created successfully.")

# Function to simulate the progress of Phase 5 (document creation)
def phase_5_progress():
    st.header("Phase 5: Generate Document")
    st.subheader("Creating the checklist from speech text...")
    
    # Simulate progress
    progress_bar = st.progress(0)
    
    # Generate the text for document creation (using speech recognition)
    text = recognize_speech_from_wav("engineer_equipment.wav")
    
    # Simulate document generation process
    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i + 1)
    
    # Create the checklist document with the recognized text
    create_checklist_doc(text)
    
    st.write("Document generation complete. Download it below:")
    st.download_button("Download field_engineer_checklist.docx", "field_engineer_checklist.docx")

# Main App
st.title("Audio Demo App")

# Sequential execution of functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Play 'engineer_equipment.wav' and Recognize Speech"):
    play_electric_unit_heater()

if st.button("Start Function 5: Generate Document from 'engineer_equipment.wav'"):
    phase_5_progress()

# Button to check FFmpeg version
if st.button("Check FFmpeg Version"):
    check_ffmpeg()

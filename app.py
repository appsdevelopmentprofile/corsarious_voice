import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import io
import speech_recognition as sr

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

# Function 4: Play "electric_unit_heater.wav" and extract text
def play_and_extract_electric_unit_heater():
    st.header("Function 4: Play and Extract Text from 'electric_unit_heater.wav'")
    file_path = "electric_unit_heater.wav"
    
    if os.path.exists(file_path):
        # Play the audio
        st.audio(file_path, format="audio/wav")
        
        # Extract text
        with st.spinner("Extracting text from the audio..."):
            extracted_text = extract_text_from_audio(file_path)
        
        # Display extracted text
        st.subheader("Extracted Text:")
        st.write(extracted_text)
    else:
        st.error("File 'electric_unit_heater.wav' not found!")

def extract_text_from_audio(file_path):
    """Extract text from the provided audio file using Google Speech Recognition."""
    # Initialize recognizer
    recognizer = sr.Recognizer()

    try:
        # Convert the audio file to a compatible format
        audio = AudioSegment.from_file(file_path)
        audio_data = io.BytesIO()
        audio.export(audio_data, format="wav")
        audio_data.seek(0)

        # Recognize speech from the audio data
        with sr.AudioFile(audio_data) as source:
            audio_recorded = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_recorded)
                return text.lower()  # Return recognized text in lowercase
            except sr.UnknownValueError:
                return "Unrecognized: Google Speech could not understand the audio."
            except sr.RequestError as e:
                return f"Error: Could not request results from Google Speech Recognition service. {e}"

    except Exception as e:
        return f"Error processing the audio file: {e}"

# Main App
st.title("Audio Demo App")

# Sequential execution of functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

if st.button("Start Function 4: Play and Extract Text from 'electric_unit_heater.wav'"):
    play_and_extract_electric_unit_heater()

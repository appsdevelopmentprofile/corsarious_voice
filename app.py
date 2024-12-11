import os
import subprocess
import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import io

# Set the FFMPEG_BINARY and FFPROBE_BINARY to the direct paths
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/Users/juanrivera/Downloads/ffprobe"

# Function to check if ffprobe is accessible
def check_ffprobe():
    try:
        # Check if ffprobe is available by running a command
        result = subprocess.run(['ffprobe', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # If ffprobe is found, return its version
        if result.returncode == 0:
            ffprobe_version = result.stdout
            st.write("FFprobe version detected successfully:")
            st.write(ffprobe_version)
        else:
            st.error("FFprobe not found or could not execute.")
            return False
    except FileNotFoundError:
        st.error("FFprobe is not installed or not found in the specified path.")
        return False
    except PermissionError:
        st.error("Permission denied while trying to run ffprobe.")
        return False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False
    return True

# Function to load audio (if ffprobe is available, use it)
def load_audio_file(file_path):
    if check_ffprobe():
        try:
            # Proceed to load the audio file
            audio = AudioSegment.from_file(file_path)
            st.success("Audio file loaded successfully!")
            return audio
        except Exception as e:
            st.error(f"Error loading audio file: {e}")
    else:
        st.warning("Skipping ffprobe-related operations. Proceeding without ffprobe.")
        # Fallback logic if ffprobe is not available
        try:
            # Attempt to load audio without ffprobe (using basic pydub methods)
            audio = AudioSegment.from_file(file_path)
            st.success("Audio file loaded successfully (using fallback method)!")
            return audio
        except Exception as e:
            st.error(f"Error loading audio file: {e}")
    
    return None

# Function 1: Play 'engineer_diagnosis.wav'
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

# Function 3: Play 'engineer_equipment.wav' and recognize speech
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
        st.error("File 'electric_unit_heater.wav' not found!")

# Main App
st.title("Audio Demo App")

# Sequential execution of functions
if st.button("Start Function 1: Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

if st.button("Start Function 2: Record Voice"):
    record_voice()

if st.button("Start Function 3: Play 'engineer_equipment.wav'"):
    play_electric_unit_heater()

# Check and provide FFmpeg info
if st.button("Check FFmpeg Version"):
    check_ffprobe()

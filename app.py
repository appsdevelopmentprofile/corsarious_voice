import streamlit as st
import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
import io

# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/Users/juanrivera/Downloads/ffprobe"

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

# Function 3: Play "electric_unit_heater.wav" file from GitHub repo (local directory) and recognize speech
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

# Button to check FFmpeg version
if st.button("Check FFmpeg Version"):
    check_ffmpeg()

import streamlit as st
import os
import subprocess
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import sys
import io
import speech_recognition as sr


# Add the paths to portaudio and sounddevice
sys.path.append('/opt/anaconda3/envs/base/lib/python3.11/site-packages')
sys.path.append('/opt/anaconda3/lib/python3.11/site-packages')

# Now import sounddevice or portaudio

# Test if the sounddevice package works
print(sd.query_devices())


# Set the FFMPEG_BINARY to the direct path of ffmpeg executable
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/"

# Function to check if ffmpeg is accessible
def check_ffmpeg():
    try:
        # Run ffmpeg command to check its version
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ffmpeg_version = result.stdout
        st.write("FFmpeg version detected successfully:")
        st.code(ffmpeg_version)
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not found in the specified path.")
    except PermissionError:
        st.error("Permission denied while trying to run ffmpeg.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function 1: Play "engineer_diagnosis.wav" file from local directory
def play_engineer_diagnosis():
    st.header("Function 1: Play 'engineer_diagnosis.wav'")
    file_path = "engineer_diagnosis.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'engineer_diagnosis.wav' not found!")

# Globals for recording
SAMPLE_RATE = 44100  # Sample rate for recording
CHANNELS = 1         # Mono audio

# Function to start recording
def start_recording():
    st.session_state["recording"] = []
    st.session_state["recording_state"] = True

    # Callback to capture audio chunks
    def audio_callback(indata, frames, time, status):
        if status:
            st.error(f"Audio stream error: {status}")
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
        audio_data = np.concatenate(st.session_state["recording"], axis=0)
        wav_file_path = "recorded_audio.wav"
        write(wav_file_path, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))  # Convert to PCM format

        # Convert to MP3
        mp3_file_path = "recorded_audio.mp3"
        audio_segment = AudioSegment.from_wav(wav_file_path)
        audio_segment.export(mp3_file_path, format="mp3")

        st.success(f"Recording saved as {mp3_file_path}!")
        st.audio(mp3_file_path, format="audio/mp3")

# Function 3: Play "electric_unit_heater.wav" file from local directory
def play_electric_unit_heater():
    st.header("Function 3: Play 'electric_unit_heater.wav'")
    file_path = "electric_unit_heater.wav"
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/wav")
    else:
        st.error("File 'electric_unit_heater.wav' not found!")
        
# Fucntion 4: Get the text from the recording the engineer made


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

def play_and_extract_electric_unit_heater():
    """Streamlit function to play and extract text from 'electric_unit_heater.wav'."""
    st.header("Function 4: Play and Extract Text from 'electric_unit_heater.wav'")
    
    file_path = "electric_unit_heater.wav"  # Ensure the file is in the same directory or provide a relative path
    
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

# Add the function to your Streamlit app
if __name__ == "__main__":
    play_and_extract_electric_unit_heater()



# Streamlit App
st.title("Audio Demo App")

# Check FFmpeg Version
if st.button("Check FFmpeg Version"):
    check_ffmpeg()

# Audio Recorder
st.header("Audio Recorder")
if "recording_state" not in st.session_state:
    st.session_state["recording_state"] = False

if st.button("Start Recording"):
    if st.session_state["recording_state"]:
        st.warning("Recording is already in progress!")
    else:
        start_recording()

if st.button("Stop Recording"):
    if st.session_state["recording_state"]:
        stop_recording()
    else:
        st.warning("No recording in progress to stop.")

# Play 'engineer_diagnosis.wav'
if st.button("Play 'engineer_diagnosis.wav'"):
    play_engineer_diagnosis()

# Play 'electric_unit_heater.wav'
if st.button("Play 'electric_unit_heater.wav'"):
    play_electric_unit_heater()

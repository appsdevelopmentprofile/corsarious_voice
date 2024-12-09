import os
import streamlit as st
from gtts import gTTS  # For text-to-speech
import speech_recognition as sr
import soundfile as sf
import io
from datetime import datetime
import pathlib
import pygame
import shutil


# Helper function to combine ffprobe parts
def combine_ffprobe_parts():
    """Combine ffprobe split parts (if applicable)"""
    # Paths to the ffprobe split parts in the GitHub repository
    ffprobe_part_aa_path = pathlib.Path("ffprobe_part_aa")  # Path to the first part
    ffprobe_part_ab_path = pathlib.Path("ffprobe_part_ab")  # Path to the second part
    combined_ffprobe_path = pathlib.Path("ffprobe")  # The name for the combined ffprobe file

    # Check if both parts exist
    if ffprobe_part_aa_path.exists() and ffprobe_part_ab_path.exists():
        try:
            # Use shutil to combine parts directly
            with open(combined_ffprobe_path, "wb") as combined_file:
                with open(ffprobe_part_aa_path, "rb") as part_aa:
                    shutil.copyfileobj(part_aa, combined_file)
                with open(ffprobe_part_ab_path, "rb") as part_ab:
                    shutil.copyfileobj(part_ab, combined_file)
            st.info(f"ffprobe parts combined into {combined_ffprobe_path}")
            return combined_ffprobe_path
        except Exception as e:
            st.error(f"An error occurred while combining ffprobe parts: {e}")
            return None
    else:
        st.error("ffprobe part files are missing!")
        return None


# Function to play the questions via gTTS and stream audio
def play_questionnaire(questions):
    """Play the questionnaire using gTTS and soundfile."""
    for i, question in enumerate(questions, 1):
        st.info(f"Question {i}: {question}")
        tts = gTTS(text=question, lang='en')
        mp3_audio = io.BytesIO()
        tts.save(mp3_audio)
        mp3_audio.seek(0)
        
        # Convert MP3 to WAV format using soundfile
        wav_audio_path = "temp.wav"
        with open(wav_audio_path, "wb") as temp_wav:
            mp3_audio.seek(0)
            temp_wav.write(mp3_audio.read())
        
        # Play audio using pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(wav_audio_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish before proceeding
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Optional: Delete temporary file after playback
        os.remove(wav_audio_path)


# Function to record responses using speech recognition
def record_responses(questions):
    """Record engineer responses to each question."""
    recognizer = sr.Recognizer()
    responses = []
    
    with sr.Microphone() as source:
        for i, question in enumerate(questions, 1):
            st.info(f"Listening for response to Question {i}...")
            try:
                audio = recognizer.listen(source, timeout=10)
                response = recognizer.recognize_google(audio)
                responses.append(response)
                st.success(f"Recorded response: {response}")
            except sr.UnknownValueError:
                st.warning(f"Could not understand the audio for Question {i}.")
                responses.append("N/A")
            except sr.RequestError as e:
                st.error(f"Error with the speech recognition service: {e}")
                responses.append("Error")
    
    return responses


# Function to save responses as MP3
def save_responses_as_mp3(responses, filename):
    """Save responses as an MP3 file."""
    response_text = "\n".join(responses)
    tts = gTTS(text=response_text, lang='en')
    tts.save(filename)
    st.success(f"Responses saved as {filename}")


# Streamlit Interface
st.title("Virtual Assistant for Project Checklist")
questions = [
    "What is the project?",
    "What is the type of document?",
    "What is the operation?",
    "What is the type of equipment?",
    "What is the label of the equipment or tag of the process?"
]

# Load ffprobe if needed (combine the parts if they exist)
ffprobe_path = combine_ffprobe_parts()  # Path to the combined ffprobe file
if ffprobe_path:
    st.info(f"ffprobe found at: {ffprobe_path}")

# Start the process
if st.button("Start Virtual Assistant"):
    st.info("Playing the questionnaire...")
    play_questionnaire(questions)
    
    st.info("Recording responses...")
    responses = record_responses(questions)
    
    st.info("Identifying the checklist...")
    checklist_name = f"{'_'.join(responses)}.jpg"
    st.success(f"Checklist identified: {checklist_name}")
    
    st.info("Saving the responses...")
    filename = f"{'_'.join(responses)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    save_responses_as_mp3(responses, filename)
    
    st.success("Checklist saved! Virtual Assistant process completed.")

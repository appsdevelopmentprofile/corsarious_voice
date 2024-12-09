import os
import streamlit as st
from gtts import gTTS  # For text-to-speech
import speech_recognition as sr
from pydub import AudioSegment
import io
from datetime import datetime
import shutil
import subprocess

# Define helper functions
def combine_ffprobe_parts():
    """Combine ffprobe split parts (if applicable)"""
    # Paths to the ffprobe split parts in the GitHub repository
    ffprobe_part_aa_path = "ffprobe_part_aa"  # Path to the first part
    ffprobe_part_ab_path = "ffprobe_part_ab"  # Path to the second part
    combined_ffprobe_path = "ffprobe"  # The name for the combined ffprobe file

    # Check if both parts exist
    if os.path.exists(ffprobe_part_aa_path) and os.path.exists(ffprobe_part_ab_path):
        try:
            # Use shutil to copy the contents of both parts into the combined file
            with open(combined_ffprobe_path, "wb") as combined_file:
                shutil.copyfileobj(open(ffprobe_part_aa_path, 'rb'), combined_file)
                shutil.copyfileobj(open(ffprobe_part_ab_path, 'rb'), combined_file)
            st.info(f"ffprobe parts combined into {combined_ffprobe_path}")
            return combined_ffprobe_path
        except Exception as e:
            st.error(f"An error occurred while combining ffprobe parts: {e}")
            return None
    else:
        st.error("ffprobe part files are missing!")
        return None

def play_questionnaire(questions):
    """Play the questionnaire using pydub."""
    for i, question in enumerate(questions, 1):
        st.info(f"Question {i}: {question}")
        tts = gTTS(text=question, lang='en')
        mp3_audio = io.BytesIO()
        tts.save(mp3_audio)
        mp3_audio.seek(0)
        
        # Convert the MP3 into a playable format using pydub
        audio = AudioSegment.from_mp3(mp3_audio)
        audio.export("temp.wav", format="wav")
        
        # Stream the audio as WAV file for playback
        st.audio("temp.wav", format="audio/wav")
        
        # Optional: Delete temporary file
        os.remove("temp.wav")

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

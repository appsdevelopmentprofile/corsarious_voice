import os
import streamlit as st
from gtts import gTTS  # For text-to-speech
import speech_recognition as sr
from pydub import AudioSegment
import io
from datetime import datetime

# Define helper functions
def combine_ffmpeg_parts():
    """Combine ffmpeg split parts (if applicable)"""
    ffmpeg_part_aa_path = "/content/ffmpeg_part_aa"  # Path to the first part
    ffmpeg_part_ab_path = "/content/ffmpeg_part_ab"  # Path to the second part (if it exists)
    combined_ffmpeg_path = "/content/ffmpeg"

    # Ensure both parts exist before combining
    if os.path.exists(ffmpeg_part_aa_path) and os.path.exists(ffmpeg_part_ab_path):
        # Combine parts using 'cat' command
        os.system(f"cat {ffmpeg_part_aa_path} {ffmpeg_part_ab_path} > {combined_ffmpeg_path}")
        st.info(f"ffmpeg parts combined into {combined_ffmpeg_path}")
        return combined_ffmpeg_path
    else:
        st.error("ffmpeg part files are missing!")
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

# Load ffmpeg if needed (combine the parts if they exist)
ffmpeg_path = combine_ffmpeg_parts()  # Path to the combined ffmpeg file
if ffmpeg_path:
    st.info(f"FFmpeg found at: {ffmpeg_path}")

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

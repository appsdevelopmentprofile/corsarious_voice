import speech_recognition as sr
from docx import Document
from pydub import AudioSegment
import io

# Function to recognize speech from the WAV file
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

# Function to create a checklist document from recognized speech
def create_checklist_doc_from_speech(text):
    # Create a new Document
    doc = Document()

    # Title of the document
    doc.add_heading('Field Engineer Questionnaire', 0)

    # Add a table with 2 columns
    table = doc.add_table(rows=1, cols=2)

    # Set the table header (first row)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Question'
    hdr_cells[1].text = 'Answer (YES/NO)'

    # Split the recognized text into checklist items (basic split by periods for demo)
    lines = text.split(".")  # Split by periods for simplicity, customize as needed

    # Add questions and the YES/NO options in the table
    for line in lines:
        line = line.strip()
        if line:
            row_cells = table.add_row().cells
            row_cells[0].text = line  # Add the question
            row_cells[1].text = '☐ YES ☐ NO'  # Placeholder for the "YES/NO" selection

    # Save the document
    doc.save('field_engineer_checklist_from_speech.docx')
    print("Checklist document created successfully based on speech recognition.")

# Main function to process the WAV file and create the document
def process_audio_and_create_doc(file_path):
    print("Recognizing speech from audio file...")
    recognized_text = recognize_speech_from_wav(file_path)

    print("Creating checklist document...")
    create_checklist_doc_from_speech(recognized_text)

# Path to the WAV file (engineer_equipment.wav)
file_path = "engineer_equipment.wav"

# Run the process
process_audio_and_create_doc(file_path)

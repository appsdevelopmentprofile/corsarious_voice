import streamlit as st
from docx import Document
from io import BytesIO

# Function 4: Create a checklist from recognized speech
def create_checklist_document(sentences):
    st.header("Stage 4: Create Checklist from Recognized Speech")
    if not sentences:
        st.error("No sentences provided to generate the checklist.")
        return

    # Create document
    document = Document()
    document.add_heading('Field Engineer Checklist', level=1)

    table = document.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Question'
    hdr_cells[1].text = 'Answer (YES/NO)'

    for sentence in sentences:
        if sentence.strip():
            row_cells = table.add_row().cells
            row_cells[0].text = sentence.strip()
            row_cells[1].text = '☐ YES ☐ NO'

    # Save the document to a buffer
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Display the document content (Full Document)
    display_docx(buffer)

    # Download button
    st.download_button(
        label="Download Checklist Document",
        data=buffer,
        file_name="field_engineer_checklist.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# Function to read and display the content of a .docx file
def display_docx(docx_buffer):
    try:
        # Load the .docx file from the buffer
        document = Document(docx_buffer)

        # Display the content of the .docx file
        st.subheader("Document Preview:")
        for paragraph in document.paragraphs:
            st.write(paragraph.text)

    except Exception as e:
        st.error(f"An error occurred while reading the document: {e}")

# Main App
st.title("Audio Processing App with Stages")

# Assuming you have recognized sentences from stage 3
sentences = ["Is the equipment functioning properly?", "Are there any safety concerns?", "Is the area secure?"]

if st.button("Stage 3: Recognize Speech from 'electric_unit_heater.wav'"):
    # This would normally be the result of the speech-to-text process
    if sentences:
        create_checklist_document(sentences)  # Automatically trigger Stage 4 once text is recognized

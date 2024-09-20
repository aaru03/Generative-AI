import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# Configure the API with your API key for text summarization
genai.configure(api_key='AIzaSyCMpDnXD7Ti-fzbFI4Ubz2bZN7u6FiMOw8')  # Replace with your actual API key
model = genai.GenerativeModel('gemini-pro')

# Set the cache directory to a location with more space
os.environ['HF_HOME'] = '/path/to/your/cache_directory'  # Update with your path

def describe_topic(text):
    response = model.generate_content(f"Provide a detailed description about the topic: {text}")
    description = getattr(response, 'text', 'No description found')
    return description

def summarize_large_text(text, chunk_size=1000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for chunk in chunks:
        response = model.generate_content(f"Summarize the text: {chunk}")
        summary = getattr(response, 'text', 'No summary found')
        summaries.append(summary)
    final_summary = " ".join(summaries)
    return final_summary

def generate_audio(text, filename="audio.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# Streamlit App Configuration
st.set_page_config(
    page_title="GenAudio Studio",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for additional styling
st.markdown("""
    <style>
    .css-1aumxhk {
        background-color: #f0f0f5;
    }
    .css-18e3th9 {
        font-family: 'Arial', sans-serif;
    }
    .css-1d391kg {
        color: #2a9d8f;
    }
    .css-1n8n8tb {
        font-size: 1.2em;
        color: #2a9d8f;
    }
    .stButton button {
        background-color: #2a9d8f;
        color: white;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #1f7a6f;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for inputs and outputs
if "user_input_description" not in st.session_state:
    st.session_state["user_input_description"] = ""
if "user_input_text" not in st.session_state:
    st.session_state["user_input_text"] = ""
if "feedback" not in st.session_state:
    st.session_state["feedback"] = ""

# Sidebar Instructions
st.sidebar.markdown("## How to Use")
st.sidebar.markdown("1. Enter a topic to get a description.")
st.sidebar.markdown("2. Summarize your text by entering it into the text area.")
st.sidebar.markdown("3. Generate audio for both the description and summary.")

# Input box for user text to generate a description
st.session_state["user_input_description"] = st.text_input(
    "Enter a topic to get a description:",
    value=st.session_state["user_input_description"]
)

# Button to trigger description generation
if st.button("Generate Description :memo:"):
    if st.session_state["user_input_description"]:
        with st.spinner("Generating description..."):
            try:
                description = describe_topic(st.session_state["user_input_description"])
                st.session_state["description"] = description
            except Exception as e:
                st.error(f"An error occurred while generating the description: {e}")
    else:
        st.warning("Please enter a topic to get a description.")

# Display the description if it exists in the session state
if "description" in st.session_state:
    st.subheader("Description :")
    st.write(st.session_state["description"])

    # Button to generate audio from the description
    if st.button("Generate Audio for Description :sound:"):
        description_text = st.session_state["description"]
        audio_file = generate_audio(description_text, filename="description_audio.mp3")
        st.session_state["description_audio"] = audio_file
        st.audio(audio_file)
        st.success("Audio for description generated successfully!")

# Input box for user text to summarize
# Retrieve text from session state if it exists
st.session_state["user_input_text"] = st.text_area(
    "Enter the text you want to summarize:",
    height=200,
    value=st.session_state["user_input_text"]
)

# Button to trigger summarization
if st.button("Summarize :page_with_curl:"):
    if st.session_state["user_input_text"]:
        with st.spinner("Summarizing text..."):
            try:
                summary = summarize_large_text(st.session_state["user_input_text"])
                st.session_state["summary"] = summary
            except Exception as e:
                st.error(f"An error occurred while summarizing the text: {e}")
    else:
        st.warning("Please enter some text to summarize.")

# Display the summary if it exists in the session state
if "summary" in st.session_state:
    st.subheader("Summary :")
    st.write(st.session_state["summary"])
    
    # Button to generate audio from the summary
    if st.button("Generate Audio for Summary :sound:"):
        summary_text = st.session_state["summary"]
        audio_file = generate_audio(summary_text, filename="summary_audio.mp3")
        st.session_state["summary_audio"] = audio_file
        st.audio(audio_file)
        st.success("Audio for summary generated successfully!")

# Feedback Section
st.session_state["feedback"] = st.text_area(
    "Leave your feedback or suggestions:",
    value=st.session_state["feedback"]
)

if st.button("Submit Feedback"):
    if st.session_state["feedback"]:
        st.success("Thank you for your feedback!")
    else:
        st.warning("Please enter your feedback before submitting.")



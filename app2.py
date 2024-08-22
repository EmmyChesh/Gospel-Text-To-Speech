import streamlit as st
import os
import time
import glob
import requests
from gtts import gTTS
from googletrans import Translator
from datetime import datetime
import speech_recognition as sr
import re

# Directory setup
if not os.path.exists("temp"):
    os.mkdir("temp")

# Set up Streamlit page configuration
st.set_page_config(page_title="Gospel Text-to-Speech By EmmyChesh", page_icon="✝️")

# Add custom CSS styling for a Christian theme
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>textarea {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        font-size: 15px;
        height: 120px;
    }
    .stTextInput>label {
        font-size: 15px;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    .stSelectbox>label {
        font-size: 15px;
    }
    .stButton>button {
        background-color: #FFD700;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 20px;
    }
    .stButton>button:hover {
        background-color: #FF8C00;
    }
    .stCheckbox>div>label {
        color: #4CAF50;
    }
    .stMarkdown {
        font-family: Arial, sans-serif;
    }
    .custom-title {
        margin-bottom: 20px;
        text-align: center;
        color: #FFD700;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="custom-title">✝️ Gospel Text-to-Speech ✝️</h1>', unsafe_allow_html=True)

translator = Translator()

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    
    # Sanitize the file name by removing or replacing invalid characters
    my_file_name = re.sub(r'[\\/*?:"<>|\n\r]', "", text[:20]) if text else "audio"
    
    file_path = f"temp/{my_file_name}.mp3"
    
    try:
        tts.save(file_path)
    except OSError as e:
        st.error(f"Error saving file: {e}")
        return None, None

    return my_file_name, trans_text

# Default values for languages
input_language = "en"
output_language = "en"

# Daily Bible Verse or Devotional
today_verse = "Psalm 118:24: This is the day the Lord has made; let us rejoice and be glad in it."
st.markdown(f"### Daily Verse for {datetime.today().strftime('%Y-%m-%d')}:")
st.markdown(f"**{today_verse}**")

# Bible Verses Dictionary
bible_verses = {
    "John 3:16": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
    "Psalm 23:1": "The Lord is my shepherd, I lack nothing.",
    "Matthew 28:19": "Therefore go and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit.",
}

selected_verse = st.selectbox("Select a Bible verse", list(bible_verses.keys()))

# Bible Verse Search
st.markdown("### Search for any Bible Verse")
verse_search = st.text_input("Enter Bible verse (e.g., John 3:16):")

text = ""

if verse_search:
    response = requests.get(f"https://bible-api.com/{verse_search}")
    if response.status_code == 200:
        verse_data = response.json()
        verse_text = f"{verse_data['reference']}: {verse_data['text']}"
        st.write(f"**{verse_text}**")
        text = verse_text
    else:
        st.error("Verse not found. Please enter a valid reference.")
else:
    use_custom_text = st.checkbox("Use custom text", value=True)
    if use_custom_text:
        # Voice input section
        st.write("**Or use your voice to input text:**")
        record_voice = st.button("Record Voice", key="record_voice_button")
        
        if record_voice:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Listening...")
                audio = recognizer.listen(source)
                st.write("Processing...")
                try:
                    text = recognizer.recognize_google(audio)
                    st.text_area("Enter text", value=text, height=120)
                except sr.UnknownValueError:
                    st.error("Sorry, I could not understand the audio.")
                except sr.RequestError:
                    st.error("Sorry, there was an error with the speech recognition service.")
        else:
            text = st.text_area("Enter text", height=120)
    else:
        text = bible_verses[selected_verse]

# Expanded Language Dictionary including African languages
language_dict = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Spanish": "es",
    "Portuguese": "pt",
    "Swahili": "sw",
    "Amharic": "am",
    "Hausa": "ha",
    "Afrikaans": "af",
    "Arabic": "ar",
    "French": "fr",
}

# Input and Output Language Selection
col1, col2 = st.columns(2)

with col1:
    in_lang = st.selectbox("Select your input language", list(language_dict.keys()), key="input_language_select")
    input_language = language_dict.get(in_lang, "en")

with col2:
    out_lang = st.selectbox("Select your output language", list(language_dict.keys()), key="output_language_select")
    output_language = language_dict.get(out_lang, "en")

# English Accent Selection
english_accent = st.selectbox(
    "Select your English accent",
    (
        "Default",
        "India",
        "United Kingdom",
        "United States",
        "Canada",
        "Australia",
        "Ireland",
        "South Africa",
    ),
    key="accent_select"
)

accent_dict = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za"
}

tld = accent_dict.get(english_accent, "com")

# Checkbox to display output text
display_output_text = st.checkbox("Display output text", key="display_output_text_checkbox")

# Convert Button
if st.button("Convert", key="convert_button"):
    if text:
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        if result:
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown("## Your audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if display_output_text:
                st.markdown("## Output text:")
                st.write(output_text)

            # Move the download button inside the convert block
            st.markdown("### Share your gospel message:")
            st.download_button("Download Audio", audio_bytes, file_name=f"{result}.mp3")
            st.markdown(f"[Share on WhatsApp](https://api.whatsapp.com/send?text={output_text})", unsafe_allow_html=True)
    else:
        st.error("Please enter text to convert.")

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

# Footer
st.markdown("---")
st.write("© 2024 EmmyChesh. All rights reserved.")

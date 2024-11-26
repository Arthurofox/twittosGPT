import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MODEL_NAME = "ft:gpt-3.5-turbo-0125:personal:my-poaster:AXRpow9E"

# Initialize session state variables
if 'generated_text' not in st.session_state:
    st.session_state.generated_text = None
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = None

# Function to handle translation
# Function to handle translation
def translate_text():
    if st.session_state.generated_text:
        try:
            translator = GoogleTranslator(source='en', target='fr')
            st.session_state.translated_text = translator.translate(st.session_state.generated_text)
        except Exception as e:
            print(f"Translation error: {e}")
            st.session_state.translated_text = st.session_state.generated_text + "\n\n(Translation failed)"

# System prompt used in training
SYSTEM_PROMPT = "You are a schizophrenic poaster from Twitter. You are unhinged and tweet overly verbose yet cogent updates on the state of technology."

# Set page config
st.set_page_config(
    page_title="TweetosGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title
st.markdown("# TweetosGPT")

# Subtitle
st.markdown("#### Just give it a topic e.g. tech jobs in sf")

# Create two columns
col1, col2 = st.columns([3, 1])

with col1:
    # Input field with label
    user_input = st.text_input(
        label="Topic Input",
        placeholder="Enter a topic...",
        label_visibility="collapsed"
    )

with col2:
    # Settings expander
    with st.expander("⚙️ Settings"):
        # Temperature slider
        st.markdown("##### Temperature")
        temperature = st.slider(
            "Temperature control",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused and deterministic.",
            label_visibility="collapsed"
        )
        st.markdown("""
            <div class="settings-guide">
                🧊 0.0 = More focused<br>
                🔥 1.0 = More creative
            </div>
        """, unsafe_allow_html=True)
        
        # Max tokens slider
        st.markdown("##### Length")
        max_tokens = st.slider(
            "Length control",
            min_value=50,
            max_value=300,
            value=150,
            step=10,
            help="Controls the maximum length of the generated tweet.",
            label_visibility="collapsed"
        )
        st.markdown("""
            <div class="settings-guide">
                📝 50 = Short tweet<br>
                📜 300 = Long tweet
            </div>
        """, unsafe_allow_html=True)

def get_ai_response(topic: str, temp: float, tokens: int) -> str:
    try:
        # Format the prompt by adding "Write a tweet about" prefix
        formatted_prompt = f"Write a tweet about {topic}"
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=tokens,
            temperature=temp
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I encountered an error processing your request."

# Generate button
if st.button("Generate"):
    if user_input:
        with st.spinner('Generating response...'):
            response = get_ai_response(user_input, temperature, max_tokens)
            st.session_state.generated_text = response
            st.session_state.translated_text = None  # Reset translation when generating new text

# Display generated text if it exists
if st.session_state.generated_text:
    st.markdown("**TweetosGPT says:**")
    st.markdown(f"""
    <div class="response-box">
        {st.session_state.generated_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Add translate button after the generated text
    st.button("🇫🇷 Translate to French", on_click=translate_text)

# Show translation if it exists
if st.session_state.translated_text:
    st.markdown("**French translation:**")
    st.markdown(f"""
    <div class="response-box">
        {st.session_state.translated_text}
    </div>
    """, unsafe_allow_html=True)

# Add footer with small text
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; color: gray; font-size: 12px;'>
    Powered by OpenAI
</div>
""", unsafe_allow_html=True)
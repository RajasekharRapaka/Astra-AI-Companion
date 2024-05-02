import streamlit as st
import google.generativeai as genai
import time

# Set page title and favicon
st.set_page_config(page_title="Astra", page_icon="🤖")

# Title and description
st.title("🤖Astra: Your AI Companion")
st.markdown("*Powered by Gemini 1.5 Pro🚀*")
st.markdown(
    "Hello! I'm Astra, your friendly AI companion. I can answer your questions, "
    "generate creative text formats, and help you stay organized. Ask me anything!"
)

# Read the api key
# with open("Key.txt", "r") as f:
#     key = f.read().strip()

# # Configure the API Key
# genai.configure(api_key=key)

# Github Deployment Key
st.write("DB_USERNAME:", st.secrets["DB_USERNAME"])
st.write("DB_TOKEN:", st.secrets["DB_TOKEN"])
# DB_USERNAME = "Astra"
# DB_TOKEN = "AIzaSyAcalgnhVWxVE9ZOsSsKb3UySxGw1TIdKA"

# Initiate a Gen AI Model with system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are Astra, a helpful and informative AI companion. "
        "Provide accurate and relevant information, generate creative text formats, "
        "and assist users with their tasks."
)

# Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat Object
chat = model.start_chat(history=st.session_state["chat_history"])

for msg in chat.history:
    st.chat_message(msg.role).write(msg.parts[0].text)

# Function to stream response data
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.06)

user_prompt = st.chat_input()

if user_prompt:
    st.chat_message("user").write(user_prompt)
    try:
        response = chat.send_message(user_prompt).parts[0].text
        st.chat_message("AI").write(stream_data(response))
    except Exception as e:
        st.warning(f"An error occurred: {e}")
    st.session_state["chat_history"] = chat.history

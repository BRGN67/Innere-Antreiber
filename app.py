import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Meine AI App", page_icon="🤖")
st.title("🤖 Mein AI Assistent")

# API Key laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Key fehlt in den Secrets.")
    st.stop()

# WICHTIG: Wir nutzen hier "gemini-1.5-flash", da dies am stabilsten ist.
# Falls das nicht geht, probieren Sie später "gemini-1.5-pro"
model_name = "gemini-1.5-flash" 

try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Fehler beim Laden des Modells: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Frage stellen..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            stream = model.generate_content(prompt, stream=True)
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"⚠️ Google API Fehler: {e}")
            st.info("Tipp: Prüfen Sie, ob der API Key korrekt ist und 'Gemini API' im Google Cloud Projekt aktiviert ist.")

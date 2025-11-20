import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="Meine AI App", page_icon="🤖")
st.title("🤖 Mein AI Assistent")

# API Key laden
try:
    # Versucht, den Key aus den Streamlit Secrets zu laden
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    # Falls kein Key da ist, zeige Fehler
    st.error("Fehler: Der API-Key wurde nicht in den Secrets gefunden.")
    st.stop()

# Modell laden
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat-Verlauf initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Alten Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Eingabe des Nutzers verarbeiten
if prompt := st.chat_input("Schreiben Sie hier Ihre Frage..."):
    # 1. Nutzer-Nachricht anzeigen
    with st.chat_message("user"):
        st.markdown(prompt)
    # 2. Ins Gedächtnis speichern
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Antwort generieren
    with st.chat_message("assistant"):
        try:
            stream = model.generate_content(prompt, stream=True)
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

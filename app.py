import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="Meine AI App", page_icon="✨")
st.title("✨ Meine AI App")
st.markdown("---") # Trennlinie für bessere Übersicht

# API Key laden
try:
    # Der API-Key wird sicher aus den Streamlit Secrets geladen.
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Fehler: API Key konnte nicht aus den Secrets geladen werden.")
    st.stop()

# --- 2. DAS MODELL & SYSTEM-ANWEISUNGEN ---

# HIER fügen Sie Ihre speziellen Anweisungen aus AI Studio ein, um das Verhalten des Bots zu steuern.
meine_system_instruction = """
Du bist ein hilfreicher Assistent. 
Antworte bitte immer freundlich und professionell.
"""

# Das Modell, das auf der Diagnose-Liste stand und den höchsten Zugriff hat.
model_name = "models/gemini-3-pro-preview" 

try:
    # Das Modell wird mit der spezifischen Rollenanweisung erstellt.
    model = genai.GenerativeModel(
        model_name,
        system_instruction=meine_system_instruction
    )
except Exception as e:
    st.error(f"Fehler beim Laden des Modells '{model_name}'.")
    st.error(f"Detail-Fehler: {e}")
    st.stop()

# --- 3. CHAT LOGIK ---

# Initialisierung des Chat-Verlaufs (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Anzeigen des bisherigen Verlaufs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Eingabefeld für den Nutzer
if prompt := st.chat_input("Geben Sie hier Ihre Nachricht ein..."):
    
    # 1. Nutzer-Nachricht im Chat anzeigen
    with st.chat_message("user"):
        st.markdown(prompt)
    # 2. Nachricht in den Speicher des Chats aufnehmen
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Antwort der AI generieren
    with st.chat_message("assistant"):
        try:
            # Senden des aktuellen Prompts an das Modell (ohne direkten Verlaufsspeicher 
            # in der API, da dies einfacher zu debuggen ist).
            stream = model.generate_content(prompt, stream=True)
            
            # Die Antwort streamen (schreibmaschinen-Effekt)
            response_text = st.write_stream(stream)
            
            # Die vollständige Antwort speichern
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

st.markdown("---") 
st.caption(f"Aktives Modell: `{model_name}`. Diese App ist öffentlich zugänglich.")

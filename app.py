import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="Meine AI App", page_icon="✨")
st.title("✨ Meine AI App")

# API Key laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Fehler: API Key fehlt in den Secrets.")
    st.stop()

# --- 2. DAS MODELL & IHRE ANWEISUNGEN ---

# HIER fügen Sie Ihre speziellen Anweisungen aus AI Studio ein.
# Wenn Sie keine haben, lassen Sie das Feld einfach leer "".
meine_system_instruction = """
Du bist ein hilfreicher Assistent. 
Antworte bitte immer freundlich und professionell.
"""

# Das Modell, das Sie auf der Liste gesehen haben
model_name = "models/gemini-3-pro-preview" 

try:
    # Wir erstellen das Modell mit Ihrer speziellen Anweisung
    model = genai.GenerativeModel(
        model_name,
        system_instruction=meine_system_instruction
    )
except Exception as e:
    st.error(f"Fehler beim Laden des Modells '{model_name}'. Bitte prüfen Sie die Schreibweise exakt anhand der Diagnose-Liste.")
    st.error(f"Detail-Fehler: {e}")
    st.stop()

# --- 3. CHAT LOGIK ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Eingabefeld
if prompt := st.chat_input("Geben Sie hier Ihre Nachricht ein..."):
    
    # Nachricht des Nutzers anzeigen
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Antwort der AI generieren
    with st.chat_message("assistant"):
        try:
            # Wir erstellen einen Chat-Verlauf für das Modell
            # (Hinweis: Streamlit speichert den Verlauf für die Anzeige, 
            # aber wir müssen ihn hier für das Modell neu aufbauen, damit es sich erinnert)
            history = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1] # Alle außer der allerletzten (die kommt jetzt)
            ]
            
            # Da die Modelle manchmal "user" und "model" als Rollennamen erwarten, mappen wir das ggf.
            # Für diesen einfachen Code senden wir den Prompt direkt.
            # Für komplexe Chats mit Gedächtnis nutzt man chat = model.start_chat(history=...)
            
            # Einfache Variante (Model antwortet auf aktuellen Prompt):
            stream = model.generate_content(prompt, stream=True)
            response_text = st.write_stream(stream)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

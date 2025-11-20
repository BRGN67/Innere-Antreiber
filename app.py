import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="Meine AI App", page_icon="✨")
st.title("✨ Meine AI App")
st.markdown("---") 

# API Key laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Fehler: API Key konnte nicht aus den Secrets geladen werden.")
    st.stop()

# --- 2. DAS MODELL & SYSTEM-ANWEISUNGEN ---

meine_system_instruction = """
Du bist ein hilfreicher Assistent. 
Antworte bitte immer freundlich und professionell.
"""

# Das bestätigte Modell
model_name = "models/gemini-3-pro-preview" 

# Initialisiere den Chat-Client in der Streamlit Session
if "chat_session" not in st.session_state:
    try:
        # Starte die Chat-Session mit dem Modell und System Instruction
        model = genai.GenerativeModel(
            model_name,
            system_instruction=meine_system_instruction
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Fehler beim Laden des Modells '{model_name}'.")
        st.error(f"Detail-Fehler: {e}")
        st.stop()

# --- 3. CHAT LOGIK ---

# Anzeigen des bisherigen Verlaufs aus der ChatSession
# Die history wird in der Session gespeichert, sodass sich die AI "erinnert"
for message in st.session_state.chat_session.history:
    # Die Rollennamen müssen für Streamlit angepasst werden (user/assistant)
    role = "assistant" if message.role == "model" else message.role
    
    # Der Inhalt ist ein "Part", wir extrahieren den Text
    if message.parts and message.parts[0].text:
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

# Eingabefeld für den Nutzer
if prompt := st.chat_input("Geben Sie hier Ihre Nachricht ein..."):
    
    # 1. Nutzer-Nachricht im Chat anzeigen
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Antwort der AI generieren und streamen
    with st.chat_message("assistant"):
        try:
            # Senden der Nachricht an die Chat-Session (die den Verlauf intern speichert)
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            
            # 3. Den gestreamten Text robust sammeln und anzeigen
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    # Anzeigen des Textes im Schreibmaschinen-Effekt
                    st.markdown(full_response + "▌", unsafe_allow_html=True) 
            
            # Finalen Text ohne Cursor anzeigen
            st.markdown(full_response, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

st.markdown("---") 
st.caption(f"Aktives Modell: `{model_name}`. Diese App ist öffentlich zugänglich.")

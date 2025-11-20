{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import google.generativeai as genai\
\
# 1. Konfiguration der Seite\
st.set_page_config(page_title="Meine AI App", page_icon="\uc0\u55358 \u56598 ")\
st.title("\uc0\u55358 \u56598  Mein AI Assistent")\
\
# 2. API Key sicher laden (aus den Streamlit Secrets)\
try:\
    api_key = st.secrets["GOOGLE_API_KEY"]\
    genai.configure(api_key=api_key)\
except Exception:\
    st.error("API Key fehlt! Bitte in den Streamlit Secrets hinterlegen.")\
    st.stop()\
\
# 3. Das Modell ausw\'e4hlen\
# Hier k\'f6nnen Sie auch "gemini-1.5-pro" oder Ihre System-Instructions einf\'fcgen\
model = genai.GenerativeModel('gemini-1.5-flash')\
\
# 4. Chat-Verlauf speichern (Session State)\
if "messages" not in st.session_state:\
    st.session_state.messages = []\
\
# 5. Alten Chat-Verlauf anzeigen\
for message in st.session_state.messages:\
    with st.chat_message(message["role"]):\
        st.markdown(message["content"])\
\
# 6. Eingabefeld f\'fcr den Nutzer\
if prompt := st.chat_input("Stellen Sie eine Frage..."):\
    # Nachricht des Nutzers anzeigen\
    with st.chat_message("user"):\
        st.markdown(prompt)\
    # Nachricht zum Verlauf hinzuf\'fcgen\
    st.session_state.messages.append(\{"role": "user", "content": prompt\})\
\
    # 7. Antwort von der AI holen\
    with st.chat_message("assistant"):\
        try:\
            # Stream = True sorgt f\'fcr den Schreibmaschinen-Effekt\
            stream = model.generate_content(prompt, stream=True)\
            response = st.write_stream(stream)\
            \
            # Antwort zum Verlauf hinzuf\'fcgen\
            st.session_state.messages.append(\{"role": "assistant", "content": response\})\
        except Exception as e:\
            st.error(f"Ein Fehler ist aufgetreten: \{e\}")}
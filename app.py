import streamlit as st
import google.generativeai as genai

st.title("🔍 Diagnose-Modus")

# 1. API Key laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # Zeige die ersten 4 Zeichen des Keys zur Kontrolle (der Rest bleibt geheim)
    st.write(f"API Key geladen: {api_key[:4]}... (Länge: {len(api_key)})")
    genai.configure(api_key=api_key)
except Exception:
    st.error("Der API Key fehlt in den Secrets!")
    st.stop()

st.info("Ich frage Google jetzt, welche Modelle für diesen Key verfügbar sind...")

# 2. Liste der Modelle abrufen
try:
    found_models = []
    # Wir iterieren durch alle Modelle, die Google anbietet
    for m in genai.list_models():
        # Wir suchen nur Modelle, die Text generieren können ('generateContent')
        if 'generateContent' in m.supported_generation_methods:
            found_models.append(m.name)
    
    if found_models:
        st.success("✅ Erfolg! Folgende Modelle sind verfügbar:")
        st.code("\n".join(found_models))
        st.write("Bitte kopieren Sie einen dieser Namen (z.B. 'models/gemini-pro') für den nächsten Schritt.")
    else:
        st.warning("⚠️ Die Verbindung steht, aber die Liste der Modelle ist leer. Das deutet auf ein Problem mit dem API-Key hin.")

except Exception as e:
    st.error(f"❌ Kritischer Verbindungsfehler: {e}")
    st.markdown("""
    **Mögliche Ursachen:**
    1. Der API Key ist ungültig.
    2. Sie greifen aus einer Region zu, die blockiert ist (selten bei AI Studio).
    3. Die 'Generative Language API' ist im Google Cloud Projekt nicht aktiviert.
    """)

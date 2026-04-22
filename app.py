import streamlit as st
from google import genai
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ArogyaMitra AI", page_icon="🩺", layout="wide")

# --- INITIALIZE GEMINI CLIENT ---
# Ensure "GEMINI_KEY" is set in your Streamlit Cloud Secrets
client = genai.Client(api_key=st.secrets["GEMINI_KEY"])

# --- UI HEADER ---
st.title("🩺 ArogyaMitra AI")
st.markdown("### National Health Authority: Auto-Adjudication Prototype")

# --- SIDEBAR NAVIGATION ---
option = st.sidebar.selectbox(
    "Select Module",
    ("Chatbot (PS1: Compliance)", "Forensics (PS3: Forgery Detection)")
)

# --- MODULE 1: CLINICAL COMPLIANCE (PS1) ---
if option == "Chatbot (PS1: Compliance)":
    st.header("Clinical Document Classification & STG Compliance")
    st.info("This module converts patient symptoms into structured clinical records.")

    user_query = st.text_input("Describe symptoms (e.g., 'Persistent cough for 3 days, low fever')")

    if user_query:
        # Emergency Red Flag Logic
        emergency_keywords = ["chest pain", "breathless", "unconscious", "heavy bleeding"]
        if any(word in user_query.lower() for word in emergency_keywords):
            st.error("🚨 EMERGENCY DETECTED: Please visit the nearest hospital immediately.")
        else:
            with st.spinner("Processing clinical summary..."):
                prompt = f"""
                Act as a Clinical Data Architect for the National Health Authority. 
                Analyze the following patient input and output a strictly structured JSON summary.

                Input: {user_query}

                JSON Structure:
                {{
                  "clinical_data": {{
                    "symptoms": ["list here"],
                    "duration": "extract here",
                    "severity": "Low/Medium/High"
                  }},
                  "compliance": {{
                    "stg_action": "What the Standard Treatment Guideline suggests",
                    "classification": "Inpatient/Outpatient/Emergency"
                  }}
                }}
                """
                response = client.models.generate_content(
                    model='gemini-1.5-flash-8b',
                    contents=prompt
                )
                
                st.subheader("Structured Clinical Record (JSON)")
                st.code(response.text, language='json')

# --- MODULE 2: FORGERY DETECTION (PS3) ---
elif option == "Forensics (PS3: Forgery Detection)":
    st.header("Document Forgery & Digital Tampering Detection")
    st.info("Upload a medical report or prescription to check for digital tampering.")

    uploaded_file = st.file_uploader("Choose a medical image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        
        # ELA (Error Level Analysis) Logic
        TEMP = 'temp_ela.jpg'
        SCALE = 10
        
        image.save(TEMP, quality=90)
        temporary_image = Image.open(TEMP)
        
        ela_image = ImageChops.difference(image, temporary_image)
        
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        # Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
        with col2:
            st.subheader("ELA (Tamper Analysis)")
            st.image(ela_image, use_container_width=True)
            st.caption("Bright spots or 'noise' around text indicate potential digital editing.")

        # AI Forensics Summary
        with st.spinner("Analyzing document integrity..."):
            forensic_prompt = "Analyze this medical document for signs of forgery, inconsistent fonts, or tampered dates."
            response = client.models.generate_content(
                model='gemini-1.5-flash-8b',
                contents=[forensic_prompt, image]
            )
            st.subheader("Forensic Audit Report")
            st.write(response.text)
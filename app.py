import streamlit as st
import google.generativeai as genai
import cv2
import numpy as np
from PIL import Image, ImageChops

# --- CONFIGURATION ---
# Replace with your actual Gemini API Key from Google AI Studio
# Replace the old genai.configure line with this:
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
# This will show you in the "Manage App" logs if the key is actually loading
if "GEMINI_KEY" not in st.secrets:
    st.error("Secret Key is missing from Streamlit Cloud Settings!")
else:
    st.success("API Key detected in secrets.")

st.set_page_config(page_title="ArogyaMitra AI", page_icon="🩺")
st.title("🩺 ArogyaMitra: Smart Health Ecosystem")
st.markdown("---")

# --- SIDEBAR NAVIGATION ---
option = st.sidebar.selectbox(
    "Select Module",
    ("Chatbot (PS1: Compliance)", "Forensics (PS3: Forgery Detection)")
)

# --- MODULE 1: CLINICAL COMPLIANCE (PS1) ---
if option == "Chatbot (PS1: Compliance)":
    st.header("Clinical Document Classification & STG Compliance")
    st.info("This module converts patient symptoms into structured clinical data.")

    user_query = st.text_input("Describe symptoms (e.g., 'Persistent cough for 2 weeks, mild fever'):")

    if user_query:
        # Emergency Red Flag Logic (from your logic flow)
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
                response = model.generate_content(prompt)
                st.subheader("Structured Clinical Record (JSON)")
                st.code(response.text, language='json') # This makes it look like real code!

# --- MODULE 2: FORGERY DETECTION (PS3) ---
elif option == "Forensics (PS3: Forgery Detection)":
    st.header("Document Forgery & Deepfake Detection")
    st.info("Upload a medical report or prescription to check for digital tampering.")

    uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
        
        if st.button("Run Forensic Analysis"):
            # Logic for Error Level Analysis (ELA)
            original = Image.open(uploaded_file).convert('RGB')
            temp_path = "temp_compressed.jpg"
            original.save(temp_path, 'JPEG', quality=90)
            
            compressed = Image.open(temp_path)
            diff = ImageChops.difference(original, compressed)
            
            # Enhance the difference for visualization
            extrema = diff.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            scale = 255.0 / max_diff if max_diff > 0 else 1
            ela_image = ImageChops.constant(diff, scale)
            
            st.subheader("Error Level Analysis (ELA) Result")
            st.image(ela_image, caption="Highlighted areas show potential digital manipulation.")
            st.warning("Note: Bright white patches in uniform areas suggest the image was edited/tampered.")
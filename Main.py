import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr

# 1. Initialize the AI 'Reader'
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

# 2. Packet Logic based on your resort rules
def get_packets(text_found):
    doubles, singles = 0, 0
    if "1+2" in text_found:
        doubles, singles = 1, 2
    elif "1+1" in text_found:
        doubles, singles = 1, 1
    elif "1+" in text_found:
        doubles, singles = 1, 0
    return doubles, singles

st.title("🧺 AI Highlight & Packet Counter")

# 3. Upload from Gallery
uploaded_file = st.file_uploader("Upload Highlighted List", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    
    with st.spinner("AI is scanning highlights..."):
        # Color Detection for Green Highlighter
        hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
        
        # AI reads the text in the image
        results = reader.readtext(img_np)
        
        final_doubles = 0
        final_singles = 0
        
        st.subheader("Bungalows Detected:")
        for (bbox, text, prob) in results:
            # We only count it if the AI is confident
            if prob > 0.4:
                d, s = get_packets(text)
                if d > 0: # If it found a valid code like 1+
                    st.write(f"✅ Found **{text}**: Adding {d} Double, {s} Single")
                    final_doubles += d
                    final_singles += s

        # 4. Final Packing List
        st.divider()
        st.header("📦 Today's Packing List")
        col1, col2 = st.columns(2)
        col1.metric("Total Double Packets", final_doubles)
        col2.metric("Total Single Packets", final_singles)
        st.success(f"Total Sheets Needed: {final_doubles + final_singles}")

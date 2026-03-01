import streamlit as st
import cv2
import numpy as np
from PIL import Image

def get_count(code):
    mapping = {"1+": 2, "1+1": 3, "1+2": 4, "Vacant": 0}
    return mapping.get(code, 0)

st.title("🧺 Laundry Highlight Scanner")

# Upload from Gallery
uploaded_file = st.file_uploader("Upload photo", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    st.image(img, caption="Original List", use_container_width=True)
    
    # Simple color check for green highlighter
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    st.image(mask, caption="Highlight Detection Map", use_container_width=True)

# Example list for your bungalows
bungalows = ["277", "187", "142", "138", "175"] 
total = 0
for b in bungalows:
    val = st.selectbox(f"Bungalow {b}", ["Vacant", "1+", "1+1", "1+2"])
    total += get_count(val)

st.sidebar.metric("Total Laundry Sets", total)

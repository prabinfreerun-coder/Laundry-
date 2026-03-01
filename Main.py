import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- LOGIC ---
def get_count_from_code(code):
    """Calculates guests: 1+ = 2, 1+1 = 3, 1+2 = 4."""
    mapping = {"1+": 2, "1+1": 3, "1+2": 4, "Vacant": 0}
    return mapping.get(code, 0)

st.set_page_config(page_title="Laundry Gallery Scanner", page_icon="🖼️")
st.title("🖼️ Laundry Gallery Scanner")

# --- STEP 1: UPLOAD FROM PHONE ---
st.subheader("Step 1: Upload List from Gallery")
# This line allows you to pick a photo from your iPhone library
uploaded_file = st.file_uploader("Choose a photo of the laundry list", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Convert the file to an image the AI can see
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    
    # Show the photo on your screen
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    # GREEN COLOR DETECTION (Detecting your highlighter)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    st.write("### Detection Highlight Map:")
    st.image(mask, caption="This shows where you used the green marker", use_container_width=True)

# --- STEP 2: BUNGALOW TRACKER ---
st.divider()
st.subheader("Step 2: Final Guest Count")

# The list of bungalows from your document
bungalows = ["277", "279", "280", "142", "143", "186", "187"]

if 'occupancy' not in st.session_state:
    st.session_state.occupancy = {b: "Vacant" for b in bungalows}

total_guests = 0
cols = st.columns(2)

for i, b_num in enumerate(bungalows):
    with cols[i % 2]:
        choice = st.selectbox(
            f"Bungalow {b_num}", 
            ["Vacant", "1+", "1+1", "1+2"], 
            key=f"sel_{b_num}"
        )
        total_guests += get_count_from_code(choice)

st.sidebar.metric("Total Guest Count", total_guests)
st.sidebar.success(f"🧺 Prepare {total_guests} linen sets!")

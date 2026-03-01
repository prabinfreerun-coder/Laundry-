import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Logic for counting based on your guest codes
def get_count_from_code(code):
    mapping = {"1+": 2, "1+1": 3, "1+2": 4, "Vacant": 0}
    return mapping.get(code, 0)

st.set_page_config(page_title="Laundry AI", page_icon="🧺")
st.title("🧺 Highlight Scanner")

# Upload from Gallery
uploaded_file = st.file_uploader("Upload a photo of the highlighted list", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    
    # Show the photo you uploaded
    st.image(img, caption="Uploaded List", use_container_width=True)
    
    # Look for Green Highlights
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    st.write("### Detection Map (Highlights Found):")
    st.image(mask, caption="White areas show where the AI found green highlights", use_container_width=True)

# List of bungalows from your photo
bungalows = [
    "277", "279", "280", "142", "143", "186", "187", "197", "198", "250"
]

st.divider()
st.subheader("Confirm Occupancy")

if 'occupancy' not in st.session_state:
    st.session_state.occupancy = {b: "Vacant" for b in bungalows}

total_guests = 0
cols = st.columns(2)

for i, b_num in enumerate(bungalows):
    with cols[i % 2]:
        choice = st.selectbox(f"Bungalow {b_num}", ["Vacant", "1+", "1+1", "1+2"], key=f"sel_{b_num}")
        total_guests += get_count_from_code(choice)

st.sidebar.metric("Total Guest Count", total_guests)
st.sidebar.info(f"Prepare {total_guests} sets of linens!")

import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. NEW LOGIC: Counting Packets
def calculate_packets(occupancy_dict):
    doubles = 0
    singles = 0
    for code in occupancy_dict.values():
        if code == "1+":
            doubles += 1
        elif code == "1+1":
            doubles += 1
            singles += 1
        elif code == "1+2":
            doubles += 1
            singles += 2
    return doubles, singles

st.set_page_config(page_title="Laundry Packet Counter", layout="centered")
st.title("🧺 Laundry Packet Counter")

# 2. PHOTO UPLOAD
uploaded_file = st.file_uploader("Upload bungalow list", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Current List", use_container_width=True)

# 3. BUNGALOW SELECTION
st.divider()
st.subheader("Confirm Bungalow Status")

bungalows = ["277", "279", "280", "142", "143", "186", "187"]

if 'occupancy' not in st.session_state:
    st.session_state.occupancy = {b: "Vacant" for b in bungalows}

cols = st.columns(2)
for i, b_id in enumerate(bungalows):
    with cols[i % 2]:
        st.session_state.occupancy[b_id] = st.selectbox(
            f"Bungalow {b_id}", 
            ["Vacant", "1+", "1+1", "1+2"], 
            key=f"b_{b_id}"
        )

# 4. THE PACKING LIST (The New Part!)
total_doubles, total_singles = calculate_packets(st.session_state.occupancy)

st.divider()
st.header("📦 Today's Packing List")
c1, c2 = st.columns(2)
with c1:
    st.metric("Double Packets", total_doubles)
with c2:
    st.metric("Single Packets", total_singles)

st.success(f"Total Linen Sets: {total_doubles + total_singles}")

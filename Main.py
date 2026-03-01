import streamlit as st
from PIL import Image

# --- LOGIC ---
def get_count_from_code(code):
    """Calculates guests based on your resort rules."""
    mapping = {"1+": 2, "1+1": 3, "1+2": 4, "Vacant": 0}
    return mapping.get(code, 0)

# --- APP INTERFACE ---
st.set_page_config(page_title="Laundry AI", page_icon="🧺")
st.title("🧺 Resort Laundry Scanner")

# 1. THE CAMERA FEATURE
st.subheader("Step 1: Take Photo of List")
picture = st.camera_input("Scan your paper list")

if picture:
    st.image(picture, caption="Last Scanned Image", use_container_width=True)
    st.info("Photo captured! You can now use the manual toggles below to confirm the count.")

# 2. THE TRACKER
st.divider()
st.subheader("Step 2: Guest Count Tracker")

# Replace this list with your actual bungalow numbers later!
bungalows = ["277", "279", "142", "143"]

if 'occupancy' not in st.session_state:
    st.session_state.occupancy = {b: "Vacant" for b in bungalows}

cols = st.columns(2)
total_guests = 0

for i, b_num in enumerate(bungalows):
    with cols[i % 2]:
        choice = st.selectbox(
            f"Bungalow {b_num}",
            ["Vacant", "1+", "1+1", "1+2"],
            key=f"select_{b_num}",
            index=["Vacant", "1+", "1+1", "1+2"].index(st.session_state.occupancy[b_num])
        )
        st.session_state.occupancy[b_num] = choice
        total_guests += get_count_from_code(choice)

# 3. SUMMARY
st.divider()
st.metric("Total Guests Today", total_guests)
st.write(f"🧤 Prepare **{total_guests}** sets of linens.")

if st.button("Reset List"):
    for b in bungalows:
        st.session_state.occupancy[b] = "Vacant"
    st.rerun()

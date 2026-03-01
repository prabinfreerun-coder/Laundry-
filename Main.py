import streamlit as st

# --- CORE LOGIC ---
def calculate_guests(code):
    """Translates the bungalow code into a guest count."""
    mapping = {
        "1+": 2,    # Main bedroom only
        "1+1": 3,   # Main + 1 spare
        "1+2": 4,   # Main + 2 spare
        "Vacant": 0
    }
    return mapping.get(code, 0)

# --- APP SETUP ---
st.set_page_config(page_title="Laundry Tracker", layout="wide")
st.title("🏨 Resort Laundry Tracker")

# We will simulate a small section of your list for this example
bungalow_list = ["277", "279", "280", "142", "143", "144"]

# --- SIDEBAR: INPUT DATA ---
st.sidebar.header("Update Bungalow Status")
selected_id = st.sidebar.selectbox("Select Bungalow Number", bungalow_list)
status = st.sidebar.radio("Current Occupancy", ["Vacant", "1+", "1+1", "1+2"])

# In a real app, we'd save this to a file. For now, let's use 'Session State'
if 'data' not in st.session_state:
    st.session_state.data = {b: "Vacant" for b in bungalow_list}

if st.sidebar.button("Update List"):
    st.session_state.data[selected_id] = status
    st.sidebar.success(f"Updated Bungalow {selected_id}!")

# --- MAIN DISPLAY ---
col1, col2 = st.columns(2)

total_guests = 0
occupied_count = 0

with col1:
    st.subheader("Current Occupancy List")
    for b_id, code in st.session_state.data.items():
        guests = calculate_guests(code)
        total_guests += guests
        if code != "Vacant":
            occupied_count += 1
            st.write(f"✅ **Bungalow {b_id}**: {code} ({guests} guests)")
        else:
            st.write(f"⚪ Bungalow {b_id}: Vacant")

with col2:
    st.subheader("Laundry Requirements")
    st.metric("Total Occupied Bungalows", occupied_count)
    st.metric("Total Guests to Prep For", total_guests)
    
    if total_guests > 0:
        st.info(f"💡 You need roughly {total_guests} sets of towels today!")

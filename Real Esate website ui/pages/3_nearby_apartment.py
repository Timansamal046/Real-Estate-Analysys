import pandas as pd
import pickle 
import streamlit as st 

# Load data
df = pickle.load(open("location_dff.pkl", "rb"))

# Page config
st.set_page_config(page_title="Nearby Apartments", page_icon="🏢", layout="centered")

# Header
st.markdown("<h1 style='color: #3366cc;'>🏘️ Find Nearby Apartments</h1>", unsafe_allow_html=True)

# Input section
chooose = st.selectbox("📍 Select a Location", sorted(df.columns.tolist()))
radio = st.number_input("📏 Choose a range (in km)", min_value=0.1, step=0.1)

# Action button
if st.button("🔍 Check Nearby Apartments"):

    with st.spinner("Finding apartments nearby..."):
        filtered = df[chooose].dropna()
        nearloc = filtered[filtered < radio * 1000]  # Keep *1000 if distances are in meters

    if nearloc.empty:
        st.warning("🚫 No apartments found within that distance.")
    else:
        st.success(f"✅ Found {len(nearloc)} apartments within {radio:.1f} km")

        # Display results as metric cards
        for key, value in nearloc.items():
            st.markdown(
                f"""
                <div style='background-color:#f0f8ff;padding:10px;border-radius:10px;margin:10px 0;'>
                    <h4 style='color:#2c3e50;'>{key}</h4>
                    <p style='color:#27ae60;font-size:18px;'>{value / 1000:.2f} km away</p>
                </div>
                """,
                unsafe_allow_html=True
            )

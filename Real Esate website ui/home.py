import streamlit as st

# python -m streamlit run home.py

# Page configuration
st.set_page_config(
    page_title="About Gurugram Properties",
    page_icon="🏙️",
    layout="centered"
)

# Title with emoji
st.title("🏠 Welcome to Gurugram Real Estate Insights")

# Subheader with color
st.markdown("<h3 style='color: #2E86C1;'>Your Gateway to Premium Properties in Gurugram</h3>", unsafe_allow_html=True)

# Description
st.write("""
Explore detailed data visualizations, pricing trends, property features, and more — 
all tailored to help you make smarter real estate decisions in Gurugram.  
""")

# Optional image (you can replace the URL or use a local image)
# st.image("https://cdn.pixabay.com/photo/2017/01/14/10/57/architecture-1972177_1280.jpg", caption="Cityscape of Gurugram", use_column_width=True)


# Footer or highlight box
st.success("✨ Dive into property trends, location insights, and amenities — all in one place!")

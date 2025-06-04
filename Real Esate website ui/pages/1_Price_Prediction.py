import pickle 
import streamlit as st 
import pandas as pd 
import numpy as np 

with open("df.pkl", "rb") as file:
    df = pickle.load(file)
    
with open("pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)
    

st.set_page_config(page_title = "Price Predictior")

st.sidebar.title("Predict Price")

st.header("Enter your requirements for price...")

col1 , col2 = st.columns(2)

with col1:
    propery_type = st.selectbox("Property Type", ["flat", "house"])

with col2:
    sector = st.selectbox("Sector", df["sector"].unique())

x, y, z = st.columns(3)

with x:
    bedroom = float(st.selectbox("Select number of Bedrooms", sorted(df["bedRoom"].unique())))

with y:
    bathroom = float(st.selectbox("Select number of bathroom", df["bathroom"].unique()))

with z:
    balcony = st.selectbox("Select number of balcony", df["balcony"].unique())


p, q = st.columns(2)

with p:
    agePossession = st.selectbox("Choose Propery Age", df["agePossession"].unique())

with q:
    furnishing_type = st.selectbox("Choose furnishing Category", df["furnishing_type"].unique())


p, q = st.columns(2)

with p:
    luxury = st.selectbox("Choose luxury", df["luxury_category"].unique())

with q:
    floor = st.selectbox("Choose Floor Req", df["floor_category"].unique())

p, q = st.columns(2)

with p:
    servant_room = st.selectbox("Need servant room", df["servant room"].unique())

with q:
    store_room = st.selectbox("Need Store Room", df["store room"].unique())

area = float(st.number_input("Enter house/flat area"))


columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony','agePossession', 'built_up_area',
           'servant room', 'store room','furnishing_type', 'luxury_category', 'floor_category']

data = [propery_type, sector, bedroom, bathroom, balcony, agePossession, area, float(servant_room), float(store_room), furnishing_type, luxury, floor]

inp_df = pd.DataFrame([data], columns = columns)

st.sidebar.subheader("📋 Your Inputs")
st.sidebar.write("🏠 Property Type:", propery_type)
st.sidebar.write("📍 Sector:", sector)
st.sidebar.write("🛏️ Bedrooms:", bedroom)
st.sidebar.write("🛁 Bathrooms:", bathroom)
st.sidebar.write("🌅 Balconies:", balcony)
st.sidebar.write("📅 Property Age:", agePossession)
st.sidebar.write("🧹 Furnishing:", furnishing_type)
st.sidebar.write("💎 Luxury Level:", luxury)
st.sidebar.write("📶 Floor:", floor)
st.sidebar.write("🧑‍🍳 Servant Room:", servant_room)
st.sidebar.write("📦 Store Room:", store_room)
st.sidebar.write("📐 Area:", area, "sq ft")

if st.button("🔍 Predict Price"):

    with st.spinner("Processing your input and predicting the price... 🚀"):
        st.subheader("📋 Your Input Summary")
        st.dataframe(inp_df)

        # Predicting the price
        predicted_price = np.expm1(pipeline.predict(inp_df))[0]
        max_price = predicted_price + 0.25
        low_price = predicted_price - 0.25

    st.success("✅ Prediction Complete!")

    st.header("💰 Estimated Price Range")

    # Use metric for a better look
    st.metric(label="Lowest Expected Price", value=f"{round(low_price, 2)} Cr")
    st.metric(label="Highest Expected Price", value=f"{round(max_price, 2)} Cr")

    # Add a styled text
    st.markdown(f"""
    ### 🏡 Based on your preferences:
    - Property Type: **{propery_type}**
    - Sector: **{sector}**
    - Area: **{area} sq.ft**
    - Estimated Price Range: 🟢 **{round(low_price, 2)} Cr** to 🔵 **{round(max_price, 2)} Cr**
    """)

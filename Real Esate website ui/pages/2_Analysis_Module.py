import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st 
import seaborn as sn
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast

st.set_page_config(page_title="🏡 Property Analysis Dashboard", layout="wide")
st.sidebar.title("🔍 Analysis Module")

data = pd.read_csv("datasets/data_viz1.csv")

# Tabs for better navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Geomap", "🔤 WordCloud", "📈 Price Scatter", "🥧 BHK Pie Chart", "📊 Box & Distribution"])

with tab1:
    st.markdown("## 🗺️ Sector-wise Price per Sqft Geomap")
    choice = st.selectbox("Choose Property Type", ["Select any one", "Flat", "House"])

    if choice != "Select any one":
        data = data[data["property_type"] == choice.lower()]

    numeric_cols = ['price','price_per_sqft','built_up_area','latitude','longitude']
    group_df = data[numeric_cols + ['sector']].groupby('sector').mean()

    fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                            mapbox_style="open-street-map", width=1200, height=700,
                            hover_name=group_df.index)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("⬆️ This map shows average property price per sqft by sector.")

with tab2:
    st.markdown("## 🔤 Feature WordCloud")
    forword = pd.read_csv("datasets/for_wordclode.csv")

    main = []
    for item in forword["features"].dropna().apply(ast.literal_eval):
        main.extend(item)

    features_text = ' '.join(main)
    wordcloud = WordCloud(
        width=1000,
        height=800,
        background_color="white",
        stopwords=set(['s']),
        min_font_size=5
    ).generate(features_text)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud)
    ax.axis("off")
    st.pyplot(fig)
    st.caption("⬆️ Most common features across properties.")

with tab3:
    st.markdown("## 📈 Area vs Price Relationship")
    fig3 = px.scatter(data, x="built_up_area", y="price", color="bedRoom")
    st.plotly_chart(fig3)
    st.caption("⬆️ Relationship between built-up area and price, color-coded by bedroom count.")

with tab4:
    st.markdown("## 🥧 Bedroom Distribution per Sector")
    sector_data = data["sector"].unique().tolist()
    sector_data.sort()
    sector_data.insert(0, "All Sectors")

    sector_choice = st.selectbox("Choose Sector", sector_data)

    if sector_choice == "All Sectors":
        fig4 = px.pie(data, names="bedRoom")
    else:
        query = data[data["sector"] == sector_choice]
        fig4 = px.pie(query, names="bedRoom")

    st.plotly_chart(fig4)
    st.caption("⬆️ Bedroom distribution shown as a pie chart.")

with tab5:
    st.markdown("## 📊 Box Plot & Distribution Plot")

    st.subheader("Box Plot: Bedrooms vs Price")
    room_data = data[data["bedRoom"] <= 4]
    fig5 = px.box(room_data, x="bedRoom", y="price")
    st.plotly_chart(fig5)

    st.subheader("Distribution: House vs Flat Prices")
    fig6 = plt.figure(figsize=(10, 4))
    sn.histplot(data[data["property_type"] == "house"]["price"], label="House", kde=True, color="blue")
    sn.histplot(data[data["property_type"] == "flat"]["price"], label="Flat", kde=True, color="orange")
    plt.legend()
    st.pyplot(fig6)
    st.caption("⬆️ Price distribution comparison for houses and flats.")

#for removal warnings
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import streamlit as st 
import pickle

# Load similarity matrices and dataframes
cosine_sim1 = pickle.load(open("cosine_sim1.pkl", "rb"))
cosine_sim2 = pickle.load(open("cosine_sim2.pkl", "rb"))
cosine_sim3 = pickle.load(open("cosine_sim3.pkl", "rb"))
df = pickle.load(open("location_dff.pkl", "rb"))
location_df_normalized = pickle.load(open("location_df_normalized.pkl", "rb"))

# Page config
st.set_page_config(page_title="Recommended Apartments", page_icon="🏢", layout="centered")

# Header
st.markdown("<h1 style='color:#3366cc;'>🏠 Apartment Recommender</h1>", unsafe_allow_html=True)

# Select an apartment
appartment_choice = st.selectbox("🔍 Choose an Apartment", sorted(location_df_normalized.index.tolist()))

# Recommendation function
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3

    sim_scores = list(enumerate(cosine_sim_matrix[location_df_normalized.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    top_properties = location_df_normalized.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        '🏢 Property Name': top_properties,
        '📊 Similarity Score': [round(score, 4) for score in top_scores]
    })

    return recommendations_df

# Button to show recommendations
if st.button("💡 Get Recommendations"):

    with st.spinner("Finding the most similar apartments..."):
        apartments = recommend_properties_with_scores(appartment_choice)

    st.success(f"✅ Top {len(apartments)} recommendations for **{appartment_choice}**")

    # Fancy display
    for idx, row in apartments.iterrows():
        st.markdown(
            f"""
            <div style='background-color:#f0f8ff;padding:12px;border-radius:10px;margin:10px 0;'>
                <h4 style='color:#2c3e50;'>🏢 {row['🏢 Property Name']}</h4>
                <p style='color:#27ae60;font-size:16px;'>📊 Similarity Score: <b>{row['📊 Similarity Score']}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Also show dataframe below
    with st.expander("📋 View Tabular Results"):
        st.dataframe(apartments, use_container_width=True)

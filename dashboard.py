import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Dashboard chi basic setting ---
st.set_page_config(page_title="AI & Data Analytics Dashboard", layout="wide")
st.title("🏥 Advanced Diabetes Risk Analytics Dashboard")

# --- 2. Dataset load karne ---
@st.cache_data
def load_data():
    file_path = r"D:\Diabetes\diabetes_risk_prediction_dataset.csv"
    return pd.read_csv(file_path)

df = load_data()

# --- 3. Sidebar - Filters ---
st.sidebar.header("🔍 Dashboard Filters")
selected_gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
selected_age = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Data Filter Karne
filtered_df = df[
    (df['Gender'].isin(selected_gender)) & 
    (df['Age'] >= selected_age[0]) & 
    (df['Age'] <= selected_age[1])
]

# --- 4. Top KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", f"{len(filtered_df):,}")
col2.metric("Avg Age", round(float(filtered_df['Age'].mean()), 1))
col3.metric("Avg BMI", round(float(filtered_df['BMI'].mean()), 1))
col4.metric("Avg Glucose", round(float(filtered_df['Blood_Glucose'].mean()), 1))

st.markdown("---")

# --- 5. Interactive Charts (Row 1) ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Diabetes Risk Distribution")
    fig1 = px.pie(filtered_df, names="Diabetes_Risk", hole=0.4, color="Diabetes_Risk")
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("📈 Age vs BMI (Hover for details)")
    fig2 = px.scatter(filtered_df, x="Age", y="BMI", color="Diabetes_Risk", 
                      hover_data=['Blood_Glucose', 'Gender'], opacity=0.7)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- 6. Interactive Charts (Row 2) ---
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("🩸 Blood Glucose Levels Based on Risk")
    fig3 = px.box(filtered_df, x="Diabetes_Risk", y="Blood_Glucose", color="Diabetes_Risk")
    st.plotly_chart(fig3, use_container_width=True)
    
with col_chart4:
    st.subheader("🔥 Health Metrics Correlation Heatmap")
    # FIX: Fakt numbers aslele columns aapoaap select karne
    numeric_df = filtered_df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    fig4 = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig4, use_container_width=True)
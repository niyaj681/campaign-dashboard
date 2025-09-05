import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Campaign Dashboard", layout="wide")

# Load Dataset
df = pd.read_csv("campaign_data.csv")
df['ROI'] = df['Conversions'] / df['Ad Spend (₹)']

st.title("📊 Marketing Campaign Dashboard")
st.write("Interactive dashboard for marketing performance analysis.")

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ROI by Platform
st.subheader("Average ROI by Platform")
platform_roi = df.groupby('Platform')['ROI'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='Platform', y='ROI', data=platform_roi, ax=ax)
st.pyplot(fig)

# CTR vs ROI Scatter
st.subheader("CTR vs ROI by Campaign")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='CTR (%)', y='ROI', hue='Platform', ax=ax)
st.pyplot(fig)

# Ad Spend Share Pie
st.subheader("Ad Spend Share by Platform")
fig, ax = plt.subplots()
df.groupby('Platform')['Ad Spend (₹)'].sum().plot.pie(
    autopct='%1.1f%%', startangle=90, ax=ax)
plt.ylabel("")
st.pyplot(fig)

# ROI Trend
st.subheader("ROI Trend by Campaign")
fig, ax = plt.subplots()
sns.lineplot(data=df, x='Campaign ID', y='ROI', marker='o', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit Config
st.set_page_config(page_title="📊 Marketing Analytics Dashboard", layout="wide")
sns.set_style("whitegrid")

# Function to Load Data
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [col.strip() for col in df.columns]
        for col in ['Ad Spend (₹)', 'Conversions', 'CTR (%)']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        if 'Ad Spend (₹)' in df.columns and 'Conversions' in df.columns:
            df['ROI'] = df.apply(
                lambda row: row['Conversions'] / row['Ad Spend (₹)'] if row['Ad Spend (₹)'] > 0 else 0,
                axis=1
            )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load Default Data
df = load_data("campaign_data.csv")

# Sidebar Upload Option
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file is not None:
    df = load_data(uploaded_file)

# If data is empty, stop
if df.empty:
    st.warning("⚠️ No data found. Please upload a valid CSV.")
    st.stop()

# =========================
# DASHBOARD STARTS HERE
# =========================
st.title("📊 Marketing Analytics Dashboard")
st.markdown("Analyze **campaign performance** with KPIs, filters, and advanced charts. "
            "Upload your own data in the sidebar to customize analysis.")

# Sidebar Filters
st.sidebar.subheader("🔍 Filters")
if 'Platform' in df.columns:
    platforms = ['All'] + sorted(df['Platform'].dropna().unique().tolist())
    selected_platform = st.sidebar.selectbox("Filter by Platform", platforms)
else:
    selected_platform = 'All'

campaign_ids = ['All'] + sorted(df['Campaign ID'].dropna().astype(str).unique().tolist()) if 'Campaign ID' in df.columns else ['All']
selected_campaign = st.sidebar.selectbox("Filter by Campaign ID", campaign_ids)

# Apply Filters
filtered_df = df.copy()
if selected_platform != 'All':
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]
if selected_campaign != 'All':
    filtered_df = filtered_df[filtered_df['Campaign ID'].astype(str) == selected_campaign]

# KPIs
st.subheader("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ad Spend (₹)", f"{filtered_df.get('Ad Spend (₹)', pd.Series()).sum():,.0f}")
col2.metric("Total Conversions", f"{filtered_df.get('Conversions', pd.Series()).sum():,.0f}")
avg_roi = filtered_df.get('ROI', pd.Series()).mean()
col3.metric("Avg ROI", f"{avg_roi:.2f}" if pd.notna(avg_roi) else "N/A")
col4.metric("Total Campaigns", filtered_df.get('Campaign ID', pd.Series()).nunique())

# Data Preview
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(10))

# Download Button
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_data.csv',
    mime='text/csv'
)

st.markdown("---")
st.subheader("📊 Visual Analysis")

# ROI by Platform
if 'Platform' in filtered_df.columns and 'ROI' in filtered_df.columns:
    st.markdown("### 🔹 Average ROI by Platform")
    platform_roi = filtered_df.groupby('Platform')['ROI'].mean().reset_index()
    if not platform_roi.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='Platform', y='ROI', data=platform_roi, palette="viridis", ax=ax)
        ax.set_title("Average ROI by Platform")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# CTR vs Conversions Scatter
if {'CTR (%)', 'Conversions'}.issubset(filtered_df.columns):
    st.markdown("### 🔹 CTR vs Conversions (Bubble = ROI)")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=filtered_df, x='CTR (%)', y='Conversions',
        size='ROI' if 'ROI' in filtered_df.columns else None,
        hue='Platform' if 'Platform' in filtered_df.columns else None,
        sizes=(50, 200), ax=ax, legend='brief'
    )
    ax.set_title("CTR vs Conversions")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Ad Spend Share
if 'Platform' in filtered_df.columns and 'Ad Spend (₹)' in filtered_df.columns:
    st.markdown("### 🔹 Ad Spend Share by Platform")
    spend_by_platform = filtered_df.groupby('Platform')['Ad Spend (₹)'].sum()
    if not spend_by_platform.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        spend_by_platform.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, cmap='Set3')
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ROI Trend
if 'Campaign ID' in filtered_df.columns and 'ROI' in filtered_df.columns:
    st.markdown("### 🔹 ROI Trend by Campaign")
    df_sorted = filtered_df.sort_values('Campaign ID')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_sorted, x='Campaign ID', y='ROI', marker='o',
                 hue='Platform' if 'Platform' in df.columns else None, ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Correlation Heatmap
st.markdown("### 🔹 Feature Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
if not numeric_df.empty:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(numeric_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Feature Correlation")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No numeric data available for correlation heatmap.")

# Top Campaigns
if 'ROI' in filtered_df.columns:
    st.markdown("### 🔹 Top 5 Campaigns by ROI")
    top_campaigns = filtered_df.sort_values(by="ROI", ascending=False).head(5)
    st.dataframe(top_campaigns)


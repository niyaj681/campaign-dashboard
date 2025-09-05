import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit & Seaborn Setup
st.set_page_config(page_title="📊 Campaign Dashboard", layout="wide")
sns.set_style("whitegrid")

# Load Dataset Function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("campaign_data.csv")
        # Ensure numeric types
        df['Ad Spend (₹)'] = pd.to_numeric(df['Ad Spend (₹)'], errors='coerce').fillna(0)
        df['Conversions'] = pd.to_numeric(df['Conversions'], errors='coerce').fillna(0)
        # ROI calculation
        df['ROI'] = df.apply(
            lambda row: row['Conversions'] / row['Ad Spend (₹)'] if row['Ad Spend (₹)'] > 0 else 0,
            axis=1
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Check if data is loaded
if not df.empty:
    st.title("📊 Marketing Campaign Dashboard")
    st.markdown("An interactive dashboard for **marketing campaign performance analysis**.")

    # Platform Filter
    platforms = df['Platform'].dropna().unique().tolist()
    selected_platform = st.selectbox("Select Platform", options=['All'] + platforms)
    filtered_df = df if selected_platform == 'All' else df[df['Platform'] == selected_platform]

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(filtered_df.head())

    # KPIs
    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ad Spend (₹)", f"{filtered_df['Ad Spend (₹)'].sum():,.0f}")
    col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,.0f}")
    avg_roi = filtered_df['ROI'].mean()
    col3.metric("Avg ROI", f"{avg_roi:.2f}" if not pd.isna(avg_roi) else "N/A")
    col4.metric("Total Campaigns", filtered_df['Campaign ID'].nunique())

    # ROI by Platform
    if not filtered_df.empty:
        st.subheader("📈 Average ROI by Platform")
        platform_roi = filtered_df.groupby('Platform')['ROI'].mean().reset_index()
        if not platform_roi.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x='Platform', y='ROI', data=platform_roi, palette="viridis", ax=ax)
            ax.set_title("Average ROI by Platform")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    # CTR vs ROI Scatter
    if 'CTR (%)' in filtered_df.columns and not filtered_df.empty:
        st.subheader("📊 CTR vs ROI by Campaign")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=filtered_df,
            x='CTR (%)', y='ROI',
            hue='Platform', size='Conversions',
            sizes=(50, 200), ax=ax, legend='brief'
        )
        ax.set_title("CTR vs ROI (Bubble Size = Conversions)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Ad Spend Share Pie
    st.subheader("🧾 Ad Spend Share by Platform")
    spend_by_platform = filtered_df.groupby('Platform')['Ad Spend (₹)'].sum()
    if not spend_by_platform.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = sns.color_palette('Set3', n_colors=len(spend_by_platform))
        spend_by_platform.plot.pie(
            autopct='%1.1f%%', startangle=90, ax=ax, colors=colors
        )
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No data to display for Ad Spend Share.")

    # ROI Trend by Campaign
    if 'Campaign ID' in filtered_df.columns and not filtered_df.empty:
        st.subheader("📉 ROI Trend by Campaign")
        df_sorted = filtered_df.sort_values('Campaign ID')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_sorted, x='Campaign ID', y='ROI', marker='o', hue='Platform', ax=ax)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Correlation Heatmap
    st.subheader("🔍 Correlation Heatmap")
    numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Feature Correlation Heatmap")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No numeric data available for correlation heatmap.")

    # Top Campaigns Table
    st.subheader("🏆 Top 5 Campaigns by ROI")
    top_campaigns = filtered_df.sort_values(by="ROI", ascending=False).head(5)
    st.dataframe(top_campaigns[['Campaign ID', 'Platform', 'ROI', 'Conversions', 'Ad Spend (₹)']])

else:
    st.warning("No data available to display.")

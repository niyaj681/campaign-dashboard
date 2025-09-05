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
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit & Seaborn Setup
st.set_page_config(page_title="📊 Campaign Dashboard", layout="wide")
sns.set_style("whitegrid")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load Dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("campaign_data.csv")
        df['ROI'] = df['Conversions'] / df['Ad Spend (₹)']
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Title & Description
    st.title("📊 Marketing Campaign Dashboard")
    st.markdown("An interactive dashboard for **marketing campaign performance analysis**.")

    # User input: Platform filter
    platforms = df['Platform'].unique()
    selected_platform = st.selectbox("Select Platform", options=['All'] + list(platforms))

    # Filter data based on selection
    if selected_platform != 'All':
        filtered_df = df[df['Platform'] == selected_platform]
    else:
        filtered_df = df

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(filtered_df.head())

    # KPIs
    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ad Spend (₹)", f"{filtered_df['Ad Spend (₹)'].sum():,.0f}")
    col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,.0f}")
    col3.metric("Avg ROI", f"{filtered_df['ROI'].mean():.2f}")
    col4.metric("Total Campaigns", filtered_df['Campaign ID'].nunique())

    # ROI by Platform
    st.subheader("📈 Average ROI by Platform")
    platform_roi = filtered_df.groupby('Platform')['ROI'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Platform', y='ROI', data=platform_roi, palette="viridis", ax=ax)
    ax.set_title("Average ROI by Platform")
    plt.tight_layout()
    st.pyplot(fig)

    # CTR vs ROI Scatter
    st.subheader("📊 CTR vs ROI by Campaign")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x='CTR (%)', y='ROI', hue='Platform', size='Conversions', sizes=(50, 200), ax=ax)
    ax.set_title("CTR vs ROI (Bubble Size = Conversions)")
    plt.tight_layout()
    st.pyplot(fig)

    # Ad Spend Share Pie
    st.subheader("🧾 Ad Spend Share by Platform")
    fig, ax = plt.subplots(figsize=(6, 6))
    spend_by_platform = filtered_df.groupby('Platform')['Ad Spend (₹)'].sum()
    colors = sns.color_palette('Set3', n_colors=len(spend_by_platform))
    spend_by_platform.plot.pie(
        autopct='%1.1f%%', startangle=90, ax=ax, colors=colors)
    plt.ylabel("")
    plt.tight_layout()
    st.pyplot(fig)

    # ROI Trend by Campaign
    st.subheader("📉 ROI Trend by Campaign")
    df_sorted = filtered_df.sort_values('Campaign ID')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_sorted, x='Campaign ID', y='ROI', marker='o', hue='Platform', ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Heatmap of Correlations
    st.subheader("🔍 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(fig)

    # Top Campaigns by ROI
    st.subheader("🏆 Top 5 Campaigns by ROI")
    top_campaigns = filtered_df.sort_values(by="ROI", ascending=False).head(5)
    st.dataframe(top_campaigns[['Campaign ID', 'Platform', 'ROI', 'Conversions', 'Ad Spend (₹)']])
else:
    st.warning("No data available to display.")




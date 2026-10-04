import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Logistics Analytics (GPT Theme)",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ChatGPT Custom UI Injection
def load_css():
    st.markdown("""
    <style>
    /* ChatGPT Dark Mode Aesthetics */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #343541;
        color: #ECECF1;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #202123 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Headers */
    h1, h2, h3, h4, p, label {
        color: #ECECF1 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Inputs & Selectboxes */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #40414F;
        color: white;
        border: 1px solid #565869;
        border-radius: 6px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #10A37F;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0E906F;
        border: none;
        color: white;
    }
    .stDownloadButton>button {
        background-color: #10A37F;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
    
    /* KPI Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #444654;
        border: 1px solid rgba(255,255,255,0.05);
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
    }
    div[data-testid="metric-container"] > div {
        color: #10A37F !important;
    }
    div[data-testid="metric-container"] label {
        color: #ECECF1 !important;
        font-size: 1rem !important;
        font-weight: 600;
    }
    
    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: #40414F;
        border: 1px dashed #565869;
        border-radius: 8px;
    }
    
    /* Hide top header and footer for cleaner look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        background-color: #444654;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Dividers */
    hr {
        border-color: #565869;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ----------------------------------------
# 3. Introduction Section
# ----------------------------------------
st.markdown("<h1 style='text-align: center;'>📦 Logistics & Delivery AI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8e8ea0 !important; margin-bottom: 30px;'>Powered by Logistics Data • Analyzing performance, delays, and costs instantly.</p>", unsafe_allow_html=True)

# ----------------------------------------
# 4. File Upload Section
# ----------------------------------------
st.sidebar.markdown("### 📡 Data Input")
uploaded_file = st.sidebar.file_uploader("Upload Dataset (.xlsx)", type=['xlsx'])

if uploaded_file is None:
    st.info("👋 **Hello!** Please upload the `sample_logistics_data.xlsx` file in the sidebar to initialize the AI analysis dashboard.")
    st.stop()

# ----------------------------------------
# 5. Data Loading and Cleaning
# ----------------------------------------
@st.cache_data
def load_data(file):
    try:
        df = pd.read_excel(file)
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        if 'Delivery_Date' in df.columns:
            df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
        if df['Shipping_Cost'].isnull().any():
            df['Shipping_Cost'] = df['Shipping_Cost'].fillna(df['Shipping_Cost'].median())
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_data(uploaded_file)

if df is None:
    st.stop()

st.sidebar.success("✅ Data Loaded")

# ----------------------------------------
# 6. Sidebar Filters
# ----------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Parameters")

regions = ['All'] + sorted(df['Region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

statuses = ['All'] + sorted(df['Delivery_Status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Delivery Status", statuses)

modes = ['All'] + sorted(df['Transportation_Mode'].dropna().unique().tolist())
selected_mode = st.sidebar.selectbox("Transportation Mode", modes)

filtered_df = df.copy()

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Delivery_Status'] == selected_status]
    
if selected_mode != 'All':
    filtered_df = filtered_df[filtered_df['Transportation_Mode'] == selected_mode]


# ----------------------------------------
# 7. KPI Dashboard
# ----------------------------------------
st.markdown("### 📊 System Metrics")

total_shipments = len(filtered_df)
delivered_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delivered'])
delayed_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed'])

on_time_rate = (delivered_count / (delivered_count + delayed_count) * 100) if (delivered_count + delayed_count) > 0 else 0
avg_delivery_time = filtered_df['Actual_Delivery_Days'].mean()
avg_cost = filtered_df['Shipping_Cost'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shipments", f"{total_shipments}")
col2.metric("On-Time Rate", f"{on_time_rate:.1f}%")
col3.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} d" if pd.notnull(avg_delivery_time) else "N/A")
col4.metric("Avg Shipping Cost", f"₹{avg_cost:.0f}" if pd.notnull(avg_cost) else "N/A")

# ----------------------------------------
# 8. Data Analysis & Charts
# ----------------------------------------
st.markdown("---")
st.markdown("### 📈 Visual Analysis")

# Use plotly dark theme with ChatGPT accent colors
gpt_colors = ['#10A37F', '#187E65', '#2C3E50', '#8E8EA0']

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    status_counts = filtered_df['Delivery_Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_status = px.pie(status_counts, names='Status', values='Count', 
                        title="Status Distribution", hole=0.5,
                        color_discrete_sequence=gpt_colors,
                        template='plotly_dark')
    fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_status, use_container_width=True)
    
with chart_col2:
    region_counts = filtered_df['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']
    fig_region = px.bar(region_counts, x='Region', y='Count', 
                        title="Shipments by Region", text='Count',
                        color_discrete_sequence=['#10A37F'],
                        template='plotly_dark')
    fig_region.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_region, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    fig_cost = px.box(filtered_df, x='Transportation_Mode', y='Shipping_Cost', 
                      title="Cost Analysis by Mode",
                      color='Transportation_Mode',
                      color_discrete_sequence=gpt_colors,
                      template='plotly_dark')
    fig_cost.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_cost, use_container_width=True)

with chart_col4:
    trend_df = filtered_df.copy()
    trend_df['Month'] = trend_df['Order_Date'].dt.to_period('M').astype(str)
    monthly_counts = trend_df.groupby('Month').size().reset_index(name='Shipments')
    monthly_counts = monthly_counts.sort_values('Month')
    
    fig_trend = px.line(monthly_counts, x='Month', y='Shipments', 
                        title="Volume Timeline", markers=True,
                        color_discrete_sequence=['#10A37F'],
                        template='plotly_dark')
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------------------
# 9. Automated Insights
# ----------------------------------------
st.markdown("---")
st.markdown("### 🧠 AI Generated Insights")

# Wrap insights in a ChatGPT-like "assistant" bubble
if len(filtered_df) > 0:
    top_region = filtered_df['Region'].mode()[0]
    delayed_pct = (len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    expensive_mode = filtered_df.groupby('Transportation_Mode')['Shipping_Cost'].mean().idxmax() if pd.notnull(filtered_df['Shipping_Cost'].mean()) else "Unknown"
    
    st.markdown(f"""
    <div style='background-color: #444654; padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);'>
        <p style='color: #10A37F; font-weight: bold; margin-bottom: 10px;'>Assistant</p>
        <p>Based on the current filtered dataset, here is what I found:</p>
        <ul>
            <li>The <strong>{top_region}</strong> region is handling the largest volume of shipments.</li>
            <li>Currently, <strong>{delayed_pct:.1f}%</strong> of deliveries are experiencing delays. Focus on optimizing these routes.</li>
            <li>The most expensive logistics channel on average is <strong>{expensive_mode}</strong> transportation.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    st.write("No data available to generate insights.")

# ----------------------------------------
# 10. Complete Dataset View & Download
# ----------------------------------------
st.markdown("---")
with st.expander("📁 View Raw Dataset"):
    st.dataframe(filtered_df)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

st.download_button(
    label="Export Data (CSV)",
    data=csv,
    file_name='logistics_export.csv',
    mime='text/csv',
)

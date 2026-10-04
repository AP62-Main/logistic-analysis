import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="AnalyticsGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit header/footer for cleaner app-like feel
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stButton>button { border-radius: 8px; font-weight: 500; }
        .stSelectbox>div>div { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 2. Sidebar (Mimicking ChatGPT History)
# ----------------------------------------
st.sidebar.title("Chat History")
st.sidebar.button("📦 Logistics Analytics", use_container_width=True)
st.sidebar.button("📈 Sales Forecasting (Pro)", use_container_width=True, disabled=True)
st.sidebar.button("⚙️ System Settings", use_container_width=True, disabled=True)
st.sidebar.markdown("---")

st.sidebar.markdown("### Context Parameters")
uploaded_file = st.sidebar.file_uploader("Supply Context Data (.xlsx)", type=['xlsx'])

if uploaded_file is None:
    st.title("AnalyticsGPT")
    st.markdown("### How can I help you analyze your logistics today?")
    
    with st.chat_message("assistant"):
        st.write("Please upload your `sample_logistics_data.xlsx` file in the sidebar to provide me with the context I need to generate your dashboard.")
    st.stop()

# ----------------------------------------
# 3. Data Loading
# ----------------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    if 'Delivery_Date' in df.columns:
        df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
    if df['Shipping_Cost'].isnull().any():
        df['Shipping_Cost'] = df['Shipping_Cost'].fillna(df['Shipping_Cost'].median())
    return df

df = load_data(uploaded_file)

# Sidebar Filters
regions = ['All'] + sorted(df['Region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region Filter", regions)

statuses = ['All'] + sorted(df['Delivery_Status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Status Filter", statuses)

modes = ['All'] + sorted(df['Transportation_Mode'].dropna().unique().tolist())
selected_mode = st.sidebar.selectbox("Mode Filter", modes)

filtered_df = df.copy()
if selected_region != 'All': filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_status != 'All': filtered_df = filtered_df[filtered_df['Delivery_Status'] == selected_status]
if selected_mode != 'All': filtered_df = filtered_df[filtered_df['Transportation_Mode'] == selected_mode]

# ----------------------------------------
# 4. Main Chat Interface
# ----------------------------------------
st.title("AnalyticsGPT")

# User Message
with st.chat_message("user"):
    st.write(f"Analyze the logistics performance for **Region:** `{selected_region}`, **Status:** `{selected_status}`, and **Mode:** `{selected_mode}`.")

# Assistant Message
with st.chat_message("assistant"):
    st.write("Certainly! Here is the detailed logistics analysis based on the parameters you provided:")
    
    # KPIs
    total_shipments = len(filtered_df)
    delivered_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delivered'])
    delayed_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed'])
    on_time_rate = (delivered_count / (delivered_count + delayed_count) * 100) if (delivered_count + delayed_count) > 0 else 0
    avg_delivery_time = filtered_df['Actual_Delivery_Days'].mean()
    avg_cost = filtered_df['Shipping_Cost'].mean()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Shipments", f"{total_shipments}")
    col2.metric("On-Time Rate", f"{on_time_rate:.1f}%")
    col3.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} d" if pd.notnull(avg_delivery_time) else "N/A")
    col4.metric("Avg Shipping Cost", f"₹{avg_cost:.0f}" if pd.notnull(avg_cost) else "N/A")
    st.markdown("<br>", unsafe_allow_html=True)

    # Charts using Plotly Dark
    gpt_colors = ['#10a37f', '#ffffff', '#555555', '#222222']
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        status_counts = filtered_df['Delivery_Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_status = px.pie(status_counts, names='Status', values='Count', 
                            title="Status Distribution", hole=0.6,
                            color_discrete_sequence=gpt_colors,
                            template='plotly_dark')
        fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_status, use_container_width=True)
        
    with chart_col2:
        region_counts = filtered_df['Region'].value_counts().reset_index()
        region_counts.columns = ['Region', 'Count']
        fig_region = px.bar(region_counts, x='Region', y='Count', 
                            title="Shipments by Region", text='Count',
                            color_discrete_sequence=['#10a37f'],
                            template='plotly_dark')
        fig_region.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_region, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        fig_cost = px.box(filtered_df, x='Transportation_Mode', y='Shipping_Cost', 
                          title="Cost Variance by Mode",
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
                            color_discrete_sequence=['#10a37f'],
                            template='plotly_dark')
        fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_trend, use_container_width=True)

    # Key Insights Text
    st.markdown("### Key Findings")
    if len(filtered_df) > 0:
        top_region = filtered_df['Region'].mode()[0]
        delayed_pct = (len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        expensive_mode = filtered_df.groupby('Transportation_Mode')['Shipping_Cost'].mean().idxmax() if pd.notnull(filtered_df['Shipping_Cost'].mean()) else "Unknown"
        
        st.write(f"1. The **{top_region}** region currently holds the highest volume of shipments.")
        st.write(f"2. A total of **{delayed_pct:.1f}%** of deliveries are delayed. I recommend optimizing these routes.")
        st.write(f"3. The most expensive logistics channel on average is **{expensive_mode}**.")
    else:
        st.write("Insufficient data to generate findings.")

    # Dataset View
    st.markdown("### Raw Data")
    st.dataframe(filtered_df)

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(filtered_df)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='analytics_gpt_export.csv',
        mime='text/csv',
    )

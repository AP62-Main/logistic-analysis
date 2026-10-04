import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Logistics & Delivery Analytics",
    page_icon="🚚",
    layout="wide"
)

st.title("📦 Logistics and Delivery Performance Analytics")
st.markdown("""
Welcome to the **Logistics Analytics Dashboard**. 
This project analyzes delivery data to uncover insights about shipment volumes, delivery times, and shipping costs. 
By analyzing this data, businesses can identify delays and improve overall delivery performance.

**Created as a College Minor Project.**
""")

st.sidebar.header("1. Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload Logistics Dataset (Excel .xlsx)", type=['xlsx'])

if uploaded_file is None:
    st.info("👈 Please upload the 'sample_logistics_data.xlsx' file using the sidebar to view the dashboard.")
    st.stop()

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
        st.error(f"Error loading file: {e}. Please ensure it's a valid Excel file.")
        return None

df = load_data(uploaded_file)

if df is None:
    st.stop()

st.success("✅ Dataset loaded and cleaned successfully!")

with st.expander("Preview Uploaded Dataset"):
    st.dataframe(df.head(5))
    st.write(f"**Total Records:** {len(df)} rows and {len(df.columns)} columns.")

st.sidebar.header("2. Dashboard Filters")

regions = ['All'] + sorted(df['Region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

statuses = ['All'] + sorted(df['Delivery_Status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Select Delivery Status", statuses)

modes = ['All'] + sorted(df['Transportation_Mode'].dropna().unique().tolist())
selected_mode = st.sidebar.selectbox("Select Transportation Mode", modes)

filtered_df = df.copy()

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Delivery_Status'] == selected_status]
    
if selected_mode != 'All':
    filtered_df = filtered_df[filtered_df['Transportation_Mode'] == selected_mode]

st.markdown("---")
st.header("📊 Performance Dashboard")

total_shipments = len(filtered_df)
delivered_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delivered'])
delayed_count = len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed'])

on_time_rate = (delivered_count / (delivered_count + delayed_count) * 100) if (delivered_count + delayed_count) > 0 else 0
avg_delivery_time = filtered_df['Actual_Delivery_Days'].mean()
avg_cost = filtered_df['Shipping_Cost'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shipments", f"{total_shipments}")
col2.metric("On-Time Rate", f"{on_time_rate:.1f}%")
col3.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} days" if pd.notnull(avg_delivery_time) else "N/A")
col4.metric("Avg Shipping Cost", f"₹{avg_cost:.2f}" if pd.notnull(avg_cost) else "N/A")

st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    status_counts = filtered_df['Delivery_Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_status = px.pie(status_counts, names='Status', values='Count', 
                        title="Delivery Status Distribution", hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_status, use_container_width=True)
    
with chart_col2:
    region_counts = filtered_df['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']
    fig_region = px.bar(region_counts, x='Region', y='Count', 
                        title="Shipments by Region", text='Count',
                        color='Region', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_region, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    fig_cost = px.box(filtered_df, x='Transportation_Mode', y='Shipping_Cost', 
                      title="Shipping Cost by Transportation Mode",
                      color='Transportation_Mode')
    st.plotly_chart(fig_cost, use_container_width=True)

with chart_col4:
    trend_df = filtered_df.copy()
    trend_df['Month'] = trend_df['Order_Date'].dt.to_period('M').astype(str)
    monthly_counts = trend_df.groupby('Month').size().reset_index(name='Shipments')
    monthly_counts = monthly_counts.sort_values('Month')
    
    fig_trend = px.line(monthly_counts, x='Month', y='Shipments', 
                        title="Monthly Shipment Trend", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.header("💡 Key Insights")

if len(filtered_df) > 0:
    top_region = filtered_df['Region'].mode()[0]
    st.write(f"- 📍 **{top_region}** is the region with the highest number of shipments in the current view.")
    
    if len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed']) > 0:
        delayed_pct = (len(filtered_df[filtered_df['Delivery_Status'] == 'Delayed']) / len(filtered_df)) * 100
        st.write(f"- ⚠️ **{delayed_pct:.1f}%** of all shipments in this selection were delayed.")
        
    if pd.notnull(filtered_df['Shipping_Cost'].mean()):
        expensive_mode = filtered_df.groupby('Transportation_Mode')['Shipping_Cost'].mean().idxmax()
        st.write(f"- 💸 **{expensive_mode}** transportation has the highest average shipping cost.")
else:
    st.write("No data available to generate insights.")

st.markdown("---")
st.header("📄 Filtered Dataset View")
st.dataframe(filtered_df)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_logistics_data.csv',
    mime='text/csv',
)

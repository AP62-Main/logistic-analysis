# Logistics and Delivery Performance Analytics

A data analytics dashboard built for a college minor project. This project allows users to upload an Excel dataset containing logistics data, clean it, and visualize key performance indicators (KPIs) regarding shipments, delivery times, and costs.

## Project Structure

```
logistics_analytics/
│
├── app.py                     # Main Streamlit application file
├── generate_data.py           # Python script to generate sample Excel dataset
├── sample_logistics_data.xlsx # Generated sample dataset for testing
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation (this file)
```

## How to Run Locally

1. **Install Python**: Ensure you have Python 3.8+ installed.
2. **Open Terminal / Command Prompt** and navigate to this folder.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Generate the Sample Data (Optional)**:
   If the `sample_logistics_data.xlsx` file is missing, you can create it by running:
   ```bash
   python generate_data.py
   ```
5. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```
6. **View the App**: The app will automatically open in your web browser (usually at `http://localhost:8501`).

## How to Deploy on Streamlit Community Cloud

1. Create a GitHub account (if you don't have one) and upload this folder (`app.py`, `requirements.txt`, `sample_logistics_data.xlsx`) to a new repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click on **"New app"**.
4. Select your GitHub repository and the branch.
5. In the **Main file path**, type `app.py`.
6. Click **Deploy!** Your app will be live on the internet in a few minutes.

## Viva Explanation Guide

If you are asked to explain this project during a viva, here is a breakdown of what you did:

* **What is this project?** 
  It is a data analytics dashboard built with Python and Streamlit to analyze logistics and delivery data. It helps visualize delays, delivery costs, and shipment volumes.
* **Which libraries did you use?**
  * `pandas` for reading the Excel file, cleaning missing data, and manipulating the dataframe.
  * `plotly.express` for creating interactive charts (bar charts, pie charts, line trends).
  * `streamlit` to build the web interface quickly without writing HTML/CSS.
  * `openpyxl` to support reading Excel files in Pandas.
* **How does data cleaning work?**
  In the `load_data` function, the app converts date strings into proper Datetime objects so we can extract months. It also checks for missing 'Shipping_Cost' values and fills them with the median cost to prevent errors in averages.
* **How do the filters work?**
  Streamlit creates sidebar dropdowns. The app takes the user's selection and filters the pandas dataframe (`df = df[df['Region'] == selected_region]`). The rest of the dashboard automatically recalculates the KPIs and charts based on this filtered dataframe.
* **Why did you use Streamlit?**
  Streamlit is perfect for data science projects. It allows converting Python data scripts into web apps very easily, which is ideal for a college minor project where complex backend architectures (like Django + React + Databases) are not required.

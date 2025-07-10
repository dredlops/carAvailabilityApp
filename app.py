import streamlit as st
import pandas as pd

st.set_page_config(page_title="Car Availability Viewer", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("results.xlsx")
    df['Date'] = df['Pickup'].dt.date
    df['Time'] = df['Pickup'].dt.strftime('%H:%M')
    df['Available'] = df['Available'].str.upper().map({'YES': '🟩', 'NO': '🟥'})
    return df

df = load_data()

# Sidebar
st.sidebar.title("Filter")
selected_date = st.sidebar.date_input("Choose a date", value=pd.to_datetime("2025-08-08"))

# Filter by selected date
filtered = df[df['Pickup'].dt.date == selected_date]

# Pivot table: rows = Time, columns = Car
pivot = filtered.pivot_table(index='Time', columns='Car', values='Available', aggfunc='first').fillna("")

# Title
st.title("🚗 Car Availability Per Hour")
st.subheader(f"Date: {selected_date.strftime('%A, %B %d, %Y')}")

# Display table
st.dataframe(pivot, use_container_width=True, height=600)

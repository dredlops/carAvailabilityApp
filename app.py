import streamlit as st
import pandas as pd

st.set_page_config(page_title="Car Availability Viewer", layout="wide")

# Load and cache the data
@st.cache_data
def load_data():
    df = pd.read_excel("results.xlsx")
    df['Date'] = df['Pickup'].dt.date
    df['Time'] = df['Pickup'].dt.strftime('%H:%M')
    df['Available'] = df['Available'].str.upper().map({'YES': '🟩', 'NO': '🟥'})
    return df

df = load_data()

# Sidebar filtering
st.sidebar.title("Filter")
selected_date = st.sidebar.date_input("Choose a date (optional)", value=None)

# Filter data if a date is selected
if selected_date:
    st.subheader(f"📅 Availability for {selected_date.strftime('%A, %B %d, %Y')}")
    filtered_df = df[df['Date'] == selected_date]
else:
    st.subheader("📅 Full Availability (All Dates)")
    filtered_df = df.copy()

# Pivot: one row per Date + Time
filtered_df['DateTime'] = pd.to_datetime(filtered_df['Date'].astype(str) + " " + filtered_df['Time'])
pivot = filtered_df.pivot_table(index=['Date', 'Time'], columns='Car', values='Available', aggfunc='first').fillna("")

# Reset index so Streamlit can render it well
pivot.reset_index(inplace=True)

# Show table
st.dataframe(pivot, use_container_width=True, height=700)

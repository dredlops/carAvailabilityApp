import streamlit as st
import pandas as pd
from datetime import date

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
today = date.today()

# Sidebar filtering
st.sidebar.title("Filter")

# Always show the date picker, but allow "clear filter" behavior
selected_date = st.sidebar.date_input(
    "Choose a date (optional)",
    value=today,
    min_value=today
)

# Filter logic: if user picked today's date and didn’t interact, show all future dates
# Streamlit doesn’t have a true “None” value for date_input, so we simulate it
if "selected" not in st.session_state:
    st.session_state["selected"] = False

if st.sidebar.button("🔍 Filter by selected date"):
    st.session_state["selected"] = True

if st.session_state["selected"]:
    st.subheader(f"📅 Availability for {selected_date.strftime('%A, %B %d, %Y')}")
    filtered_df = df[df['Date'] == selected_date]
else:
    st.subheader("📅 Full Availability (From Today Onward)")
    filtered_df = df[df['Date'] >= today]

# Prepare data for display
filtered_df['DateTime'] = pd.to_datetime(filtered_df['Date'].astype(str) + " " + filtered_df['Time'])
pivot = filtered_df.pivot_table(
    index=['Date', 'Time'],
    columns='Car',
    values='Available',
    aggfunc='first'
).fillna("")

pivot.reset_index(inplace=True)

# Show the table
st.dataframe(pivot, use_container_width=True, height=700)

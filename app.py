import streamlit as st
import pandas as pd
import json, os

st.set_page_config(page_title="Hybrid WMS Dashboard", layout="wide")

DATA_FILE = "out/hybrid_report.json"
HISTORY_FILE = "out/history.csv"
PASSWORD = "admin123"

# Session State for Authentication
if "auth" not in st.session_state:
    st.session_state.auth = False

# LOGIN SCREEN
if not st.session_state.auth:
    st.title("🔐 Login")
    pwd = st.text_input("Password", type="password")

    # Only one button, with unique key
    if st.button("Login", key="login_btn"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.experimental_rerun()
        else:
            st.error("Wrong password")

    st.stop()

# MAIN DASHBOARD
st.title("🚚 Hybrid WMS Dashboard")

# Ensure report exists
if not os.path.exists(DATA_FILE):
    st.write("⏳ First-time setup... generating initial data.")
    import run_hybrid_full
    run_hybrid_full.main()

if not os.path.exists(DATA_FILE):
    st.warning("Run run_hybrid_full.py first.")
    st.stop()

# Load report
with open(DATA_FILE) as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["run_time"] = pd.to_datetime(df["run_time"])

st.subheader("Latest Run")
st.dataframe(df)

# History file
if os.path.exists(HISTORY_FILE):
    hist = pd.read_csv(HISTORY_FILE)

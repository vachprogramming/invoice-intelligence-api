import streamlit as st
import requests
import pandas as pd
import json

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/upload"

st.set_page_config(page_title="Invoice Intelligence", page_icon="💰")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app uses **Llama-3 (AI)** to extract structured data from PDF invoices.
    
    **Tech Stack:**
    - 🐍 Python & FastAPI
    - 🐳 Docker & PostgreSQL
    - 🧠 HuggingFace Inference
    """)
    st.success("Backend Status: Online")

# Main Content
st.title("📄 Invoice Extraction AI")
st.write("Upload a PDF invoice to automatically extract vendor details, totals, and dates.")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Show a button to trigger extraction
    if st.button("Analyze Invoice"):
        with st.spinner("⏳ Sending to AI... (This uses Llama-3.2)"):
            try:
                # Prepare the file for the API request
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                
                # Call YOUR FastAPI Backend
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Extraction Complete!")
                    
                    # 1. Show Key Metrics (The "Business" View)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Vendor", data.get("vendor_name") or "Unknown")
                    col2.metric("Total", f"{data.get('total_gross')} {data.get('currency')}")
                    col3.metric("Date", data.get("invoice_date") or "Unknown")

                    # 2. Show Structured Data (The "Database" View)
                    st.subheader("Structured Data")
                    st.json(data)
                    
                    # 3. Show Database ID
                    st.caption(f"✅ Saved to PostgreSQL Database with ID: {data.get('id')}")
                    
                else:
                    st.error(f"Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to Backend. Is 'uvicorn' running?")
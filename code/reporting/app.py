import streamlit as st
import os
import json
import pandas as pd
import tempfile
from common.config import SYNTHETIC_DATA_DIR, OUTPUT_DIR
from common.schemas import PlaybookClause
from comparison.pipeline import run_pipeline
from ingestion.pdf_parser import extract_text
from reporting.report_builder import build_tabular_report
from reporting.csv_report import write_csv_report
from reporting.pdf_report import write_pdf_report

st.set_page_config(page_title="Contract Playbook Comparison", layout="wide")

st.title("Contract Playbook Comparison System (Stage 1 PoC)")

@st.cache_data
def load_playbook():
    with open(os.path.join(SYNTHETIC_DATA_DIR, "playbook.json"), "r") as f:
        playbook_data = json.load(f)
        return [PlaybookClause(**c) for c in playbook_data]

playbook = load_playbook()

# Sidebar for contract selection
st.sidebar.header("Select Contract")
upload_file = st.sidebar.file_uploader("Upload a Contract (TXT or PDF)", type=["txt", "pdf"])

if upload_file is not None:
    # Save uploaded file to a temporary file to extract text
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{upload_file.name.split('.')[-1]}") as tmp:
        tmp.write(upload_file.getvalue())
        tmp_path = tmp.name
    
    contract_text = extract_text(tmp_path)
    contract_id = upload_file.name.split('.')[0]
    os.remove(tmp_path)
    st.sidebar.success(f"Loaded {contract_id}")
else:
    # Use synthetic contracts
    contracts_dir = os.path.join(SYNTHETIC_DATA_DIR, "contracts")
    contract_files = [f for f in os.listdir(contracts_dir) if f.endswith(".txt")]
    selected_file = st.sidebar.selectbox("Or choose a synthetic contract", contract_files)
    
    with open(os.path.join(contracts_dir, selected_file), "r", encoding="utf-8") as f:
        contract_text = f.read()
    contract_id = selected_file.replace(".txt", "")

st.header(f"Report for: {contract_id}")

use_llm = st.sidebar.checkbox("Use LLM (Requires API Key)", value=False)

if st.button("Run Comparison"):
    with st.spinner("Running pipeline..."):
        try:
            report = run_pipeline(contract_text, contract_id, playbook, use_llm=use_llm)
            
            # Display Report
            st.subheader("Comparison Results")
            rows = build_tabular_report(report)
            df = pd.DataFrame(rows)
            
            # Color code dataframe based on status
            def color_status(val):
                if val == 'MATCH':
                    color = 'green'
                elif val == 'DEVIATION':
                    color = 'orange'
                elif val == 'MISSING':
                    color = 'red'
                else:
                    color = 'black'
                return f'color: {color}'
            
            st.dataframe(df.style.map(color_status, subset=['Status']), use_container_width=True)
            
            # Download buttons
            csv_path = os.path.join(OUTPUT_DIR, f"{contract_id}_report.csv")
            pdf_path = os.path.join(OUTPUT_DIR, f"{contract_id}_report.pdf")
            
            write_csv_report(report, csv_path)
            write_pdf_report(report, pdf_path)
            
            col1, col2 = st.columns(2)
            with col1:
                with open(csv_path, "rb") as f:
                    st.download_button("Download CSV Report", f, file_name=f"{contract_id}_report.csv", mime="text/csv")
            with col2:
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF Report", f, file_name=f"{contract_id}_report.pdf", mime="application/pdf")
                    
        except Exception as e:
            st.error(f"Error running pipeline: {e}")

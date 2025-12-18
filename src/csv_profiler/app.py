import csv
import json
import streamlit as st
from io import StringIO
from pathlib import Path
from profiling import profile_rows
from render import render_markdown 
st.set_page_config(page_title="CSV Profiler", layout="wide")

st.title("CSV Profiler")
st.caption("Upload CSV → profile → export JSON + Markdown")


st.sidebar.header("Inputs")
show_preview = st.sidebar.checkbox("Show preview", value=True)
report_name = st.sidebar.text_input("Report name", value="report") 


uploaded = st.file_uploader("Upload a CSV", type=["csv"])
rows = None
report = st.session_state.get("report")

if uploaded is not None: 
        text = uploaded.getvalue().decode("utf-8-sig")
        rows = list(csv.DictReader(StringIO(text)))
        
        if len(rows) == 0:
            st.error("CSV has no data. Upload a CSV with at least 1 row.")
            st.stop() 
            
        if len(rows[0]) == 0:
            st.warning("CSV has no headers (no columns detected).") 
        

        if show_preview:
            st.subheader("Preview")
            st.write(rows[:5])
   

        if rows is not None and len(rows) > 0:
         if st.button("Generate report"):
            st.session_state["report"] = profile_rows(rows)
            
        if report is not None:
         st.divider()
        
        cols = st.columns(2)
        cols[0].metric("Rows", report.get("n_rows", 0))
        cols[1].metric("Columns", report["n_cols"])
        
        st.subheader("Columns")
        st.write(report["columns"])

        st.divider()
        st.subheader("Export Report")
        
        json_file = report_name + ".json" 
        json_text = json.dumps(report, indent=2, ensure_ascii=False) 
        
        md_file = report_name + ".md" 
        md_text = render_markdown(report) 
        c1, c2 = st.columns(2)
        c1.download_button("Download JSON", data=json_text, file_name=json_file) 
        c2.download_button("Download Markdown", data=md_text, file_name=md_file) 
        

        if st.button("Save to outputs/"): 
            out_dir = Path("outputs") 
            out_dir.mkdir(parents=True, exist_ok=True) 
        
            (out_dir / json_file).write_text(json_text, encoding="utf-8") 
            (out_dir / md_file).write_text(md_text, encoding="utf-8") 
            
            st.success(f"Saved outputs/{json_file} and outputs/{md_file}") 

        with st.expander("Markdown preview"):
            st.markdown(md_text)
else:
        st.info("Upload a CSV to begin.")
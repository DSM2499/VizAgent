import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import urllib.parse
from agents.ingestion_agent import ingest_csv
from agents.cleaning_agent import clean_data, load_cleaning_rules
from agents.planning_agent import suggest_dashboard_plan
from agents.tableau_export_agent import export_hyper, export_chart_plan_json
from agents.workbook_generator import create_twb_from_plan

import subprocess

def run_eda_subprocess(csv_path: str, output_dir: str):
    command = [
        "eda_env/bin/python",
        "eda_agent_subprocess.py",
        csv_path,
        output_dir,
    ]
    result = subprocess.run(command, capture_output = True, text = True)
    return result

st.title("📊 VizAgent - Web Analytics Agentic System")

st.sidebar.header("Step 1: Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    st.success("✅ File uploaded. Processing...")

    df, metadata = ingest_csv(uploaded_file)

    if df is not None:
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(10))

        st.subheader("Ingestion Metadata")
        st.json(metadata)
    else:
        st.error(f"❌ Ingestion Failed: {metadata.get('error', 'Unknown error')}")

st.subheader("Step 2: Data Cleaning")

if st.button("Run Cleaning Agent"):
    with st.spinner("Cleaning data..."):
        rules = load_cleaning_rules()
        cleaned_df, cleaning_log = clean_data(df.copy(), rules)
        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["cleaning_log"] = cleaning_log

        st.success("✅ Data cleaned")
        st.subheader("Cleaned Data Preview")
        st.dataframe(cleaned_df.head(10))

        st.subheader("Cleaning Log")
        st.code(cleaning_log, language='text')

if st.button("Save Cleaned CSV for EDA"):
    output_path = "outputs/eda_input.csv"
    st.session_state["eda_csv_path"] = output_path
    st.session_state["eda_output_dir"] = "outputs/generated_dashboards/"
    st.session_state["eda_ready"] = True

    st.session_state["cleaned_df"].to_csv(output_path, index=False)
    st.success(f"✅ CSV saved for EDA: `{output_path}`")


st.subheader("Step 3: Exploratory Data Analysis")

if "eda_ready" in st.session_state and st.session_state["eda_ready"]:
    if st.button("Run EDA Agent in Subprocess"):
        with st.spinner("Running EDA subprocess..."):
            result = run_eda_subprocess(
                st.session_state["eda_csv_path"],
                st.session_state["eda_output_dir"]
            )

            if result.returncode == 0:
                    st.success("EDA reports generated!")
                    st.subheader("📥 Download EDA Reports")
                    ydata_path = "outputs/generated_dashboards/ydata_profile.html"
                    if os.path.exists(ydata_path):
                        with open(ydata_path, "rb") as f:
                            ydata_bytes = f.read()
                            st.download_button(
                                label="📊 Download YData Profile Report",
                                data = ydata_bytes,
                                file_name = "ydata_profile.html",
                                mime = "text/html",

                            )
                
                    sweetviz_path = "outputs/generated_dashboards/sweetviz_report.html"
                    if os.path.exists(sweetviz_path):
                        with open(sweetviz_path, "rb") as f:
                            sweetviz_bytes = f.read()
                            st.download_button(
                                label = "📈 Download Sweetviz Report",
                                data = sweetviz_bytes,
                                file_name = "sweetviz_report.html",
                                mime = "text/html",
                            )

            else:
                st.error("❌ EDA subprocess failed.")
                st.code(result.stderr)
else:
    st.info("Please run Cleaning Agent and Save CSV for EDA first.")

st.subheader("Step 4: Visualization Planning")

if "cleaned_df" in st.session_state:
    if st.button("Generate Dashboard Plan"):
        with st.spinner("Calling LLM to suggest dashboard layout..."):
            plan_text = suggest_dashboard_plan(st.session_state["cleaned_df"])
            st.session_state["viz_plan"] = plan_text

        st.success("✅ Dashboard Plan Ready")
        st.subheader("Suggested Charts")
        st.markdown(st.session_state["viz_plan"], unsafe_allow_html=True)
else:
    st.warning("⚠️ Please run data cleaning first.")

st.subheader("Step 5: Export to Tableau")

if "cleaned_df" in st.session_state and "viz_plan" in st.session_state:
    if st.button("Export .hyper and Chart Plan"):
        with st.spinner("Exporting..."):
            hyper_path = export_hyper(st.session_state["cleaned_df"])
            plan_path = export_chart_plan_json(st.session_state["viz_plan"])
            st.session_state["hyper_path"] = hyper_path
            st.session_state["plan_path"] = plan_path

        st.success("✅ Export Complete")

        # Download buttons
        with open(hyper_path, "rb") as f:
            st.download_button("📥 Download Tableau .hyper file", data=f, file_name="vizagent_output.hyper", mime="application/octet-stream")

        with open(plan_path, "rb") as f:
            st.download_button("📄 Download Dashboard Plan JSON", data=f, file_name="dashboard_plan.json", mime="application/json")

else:
    st.warning("⚠️ Please run data cleaning and chart planning first.")

st.subheader("📘 Optional: Generate Tableau Workbook (.twb)")

if "hyper_path" in st.session_state and "plan_path" in st.session_state:
    if st.button("📘 Generate .twb Workbook"):
        workbook_path = create_twb_from_plan(
            hyper_file_name=os.path.basename(st.session_state["hyper_path"]),
            dashboard_json_path=st.session_state["plan_path"]
        )

        with open(workbook_path, "rb") as f:
            st.download_button(
                label="📥 Download Tableau Workbook (.twb)",
                data=f,
                file_name="vizagent_dashboard.twb",
                mime="application/xml"
            )
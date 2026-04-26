import streamlit as st
import requests

st.set_page_config(page_title="OmniAgent Dashboard", layout="wide")
st.title("OmniAgent – Personal AI Operations Center")

api_base = st.sidebar.text_input("API Base URL", value="http://localhost:8000")
goal = st.text_area("Task", placeholder="Research RAG 2.0 and remind me in two weeks")

if st.button("Run Task", type="primary"):
    with st.spinner("Running OmniAgent..."):
        resp = requests.post(f"{api_base}/tasks/run", json={"user_goal": goal}, timeout=30)
        if resp.ok:
            data = resp.json()
            st.subheader("Final Report")
            st.markdown(data["result"].get("final_report", "No report generated."))
            st.subheader("Metrics")
            st.json(data["metrics"])
            st.subheader("Tool Results")
            st.json(data["result"].get("tool_results", []))
        else:
            st.error(f"Request failed: {resp.status_code} {resp.text}")

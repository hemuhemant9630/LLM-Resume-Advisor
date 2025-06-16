import streamlit as st
import requests

st.title("LLM Resume Career Advisor")
file = st.file_uploader("Upload Resume", type="pdf")

if file:
    with st.spinner("Analyzing with GPT..."):
        res = requests.post("http://localhost:8000/analyze-resume/", files={"file": file})
        if res.ok:
            result = res.json()
            st.subheader("Career Suggestions")
            st.markdown(result["gpt_analysis"])
        else:
            st.error("Failed to process resume")

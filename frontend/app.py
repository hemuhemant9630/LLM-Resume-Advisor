# import streamlit as st
# import requests
# from typing import Dict, Any

# def display_candidate_summary(summary: Dict[str, str]):
#     st.header("📋 Candidate Summary")
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("Education")
#         st.write(summary["education"])
#         st.subheader("Experience")
#         st.write(summary["experience"])
    
#     with col2:
#         st.subheader("Core Competencies")
#         st.write(summary["core_competencies"])
#         st.subheader("Career Level")
#         st.write(summary["career_level"])

# def display_job_roles(roles: list):
#     st.header("💼 Recommended Job Roles")
#     for role in roles:
#         with st.expander(f"{role['title']} (Suitability: {role['suitability_score']}%)"):
#             st.write("**Why this role?**")
#             st.write(role["justification"])

# def display_skill_gaps(gaps: Dict[str, list]):
#     st.header("🎯 Skill Gaps Analysis")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.subheader("Critical Skills")
#         for skill in gaps["critical_skills"]:
#             st.write(f"• {skill}")
    
#     with col2:
#         st.subheader("Recommended")
#         for skill in gaps["recommended_skills"]:
#             st.write(f"• {skill}")
    
#     with col3:
#         st.subheader("Nice to Have")
#         for skill in gaps["nice_to_have"]:
#             st.write(f"• {skill}")

# def display_learning_advice(advice: Dict[str, list]):
#     st.header("📚 Learning & Development Path")
    
#     st.subheader("Recommended Courses")
#     for course in advice["courses"]:
#         st.write(f"• {course}")
    
#     st.subheader("Professional Development Tips")
#     for tip in advice["development_tips"]:
#         st.write(f"• {tip}")
    
#     st.subheader("Resume Improvement Suggestions")
#     for suggestion in advice["resume_improvements"]:
#         st.write(f"• {suggestion}")

# def main():
#     st.set_page_config(
#         page_title="LLM Resume Career Advisor",
#         page_icon="📝",
#         layout="wide"
#     )

#     st.title("📝 LLM Resume Career Advisor")
#     st.write("""
#     Upload your resume (PDF, DOCX, or TXT) to get personalized career insights:
#     - Career level assessment
#     - Suitable job role recommendations
#     - Skill gap analysis
#     - Learning and development advice
#     """)

#     file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

#     if file:
#         with st.spinner("🔍 Analyzing your resume with AI..."):
#             try:
#                 res = requests.post(
#                     "http://localhost:8000/analyze-resume/",
#                     files={"file": file}
#                 )
#                 res.raise_for_status()
#                 analysis = res.json()
                
#                 # Display the analysis sections
#                 display_candidate_summary(analysis["candidate_summary"])
#                 display_job_roles(analysis["recommended_roles"])
#                 display_skill_gaps(analysis["skill_gaps"])
#                 display_learning_advice(analysis["learning_advice"])
                
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Failed to process resume: {str(e)}")
#                 if hasattr(e.response, 'text'):
#                     st.error(f"Server response: {e.response.text}")

# if __name__ == "__main__":
#     main()



import streamlit as st
import requests
import json
from typing import Dict, Any

def display_error_message(error_msg: str):
    st.error("Error Processing Resume")
    
    if "No internet connection" in error_msg or "Failed to resolve" in error_msg:
        st.error("⚠️ Internet Connection Error: Please check your internet connection and try again.")
    elif "API key" in error_msg:
        st.error("⚠️ API Configuration Error: Please check if the API key is properly set.")
    else:
        st.error(f"⚠️ {error_msg}")
    
    st.info("If the problem persists, please try:")
    st.markdown("""
    1. Check your internet connection
    2. Ensure the backend server is running
    3. Verify that the API key is properly set in the `.env` file
    4. Try uploading the resume again
    """)

def display_candidate_summary(summary: Dict[str, str]):
    st.header("📋 Candidate Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Education")
        st.write(summary["education"])
        st.subheader("Experience")
        st.write(summary["experience"])
    
    with col2:
        st.subheader("Core Competencies")
        st.write(summary["core_competencies"])
        st.subheader("Career Level")
        st.write(summary["career_level"])

def display_job_roles(roles: list):
    st.header("💼 Recommended Job Roles")
    for role in roles:
        with st.expander(f"{role['title']} (Suitability: {role['suitability_score']}%)"):
            st.write("**Why this role?**")
            st.write(role["justification"])

def display_skill_gaps(gaps: Dict[str, list]):
    st.header("🎯 Skill Gaps Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Critical Skills")
        for skill in gaps["critical_skills"]:
            st.write(f"• {skill}")
    
    with col2:
        st.subheader("Recommended")
        for skill in gaps["recommended_skills"]:
            st.write(f"• {skill}")
    
    with col3:
        st.subheader("Nice to Have")
        for skill in gaps["nice_to_have"]:
            st.write(f"• {skill}")

def display_learning_advice(advice: Dict[str, list]):
    st.header("📚 Learning & Development Path")
    
    st.subheader("Recommended Courses")
    for course in advice["courses"]:
        st.write(f"• {course}")
    
    st.subheader("Professional Development Tips")
    for tip in advice["development_tips"]:
        st.write(f"• {tip}")
    
    st.subheader("Resume Improvement Suggestions")
    for suggestion in advice["resume_improvements"]:
        st.write(f"• {suggestion}")

def main():
    st.set_page_config(
        page_title="LLM Resume Career Advisor",
        page_icon="📝",
        layout="wide"
    )

    st.title("📝 LLM Resume Career Advisor")
    st.write("""
    Upload your resume (PDF, DOCX, or TXT) to get personalized career insights:
    - Career level assessment
    - Suitable job role recommendations
    - Skill gap analysis
    - Learning and development advice
    """)

    file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if file:
        with st.spinner("🔍 Analyzing your resume with AI..."):
            try:
                # Check if backend is available
                try:
                    response = requests.get("http://localhost:8000/")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend server. Please make sure it's running.")
                    st.info("To start the backend server, run:\n```\ncd backend\nuvicorn main:app --reload\n```")
                    return

                # Send resume for analysis
                res = requests.post(
                    "http://localhost:8000/analyze-resume/",
                    files={"file": file},
                    timeout=60
                )
                
                if res.ok:
                    analysis = res.json()
                    display_candidate_summary(analysis["candidate_summary"])
                    display_job_roles(analysis["recommended_roles"])
                    display_skill_gaps(analysis["skill_gaps"])
                    display_learning_advice(analysis["learning_advice"])
                else:
                    try:
                        error_detail = res.json().get("detail", str(res.text))
                        display_error_message(error_detail)
                    except json.JSONDecodeError:
                        display_error_message(f"Server Error: {res.status_code}")
                        
            except requests.exceptions.Timeout:
                display_error_message("Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                display_error_message(str(e))
            except Exception as e:
                display_error_message(str(e))

if __name__ == "__main__":
    main()
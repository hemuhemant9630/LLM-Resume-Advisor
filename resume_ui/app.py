import streamlit as st
import requests

st.set_page_config(page_title="Resume Career Analyzer", layout="wide")
st.title("📄 LLM Resume Career Advisor")

uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("🔍 Analyzing your resume..."):
        try:
            response = requests.post(
                "http://localhost:8000/analyze-resume/",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
            )
            if response.ok:
                data = response.json()
                st.success("✅ Analysis Complete!")

                st.subheader("📌 Candidate Summary")
                st.json(data.get("candidate_summary", {}))

                st.subheader("💼 Recommended Roles")
                for role in data.get("recommended_roles", []):
                    st.write(f"**{role['title']}** — Suitability: {role['suitability_score']}%")
                    st.caption(role["justification"])

                st.subheader("🧠 Skill Gaps")
                st.json(data.get("skill_gaps", {}))

                st.subheader("📚 Learning Advice")
                st.markdown("**Courses:**")
                for c in data["learning_advice"].get("courses", []):
                    st.write(f"- {c}")
                st.markdown("**Tips:**")
                for t in data["learning_advice"].get("development_tips", []):
                    st.write(f"- {t}")
                st.markdown("**Resume Improvements:**")
                for r in data["learning_advice"].get("resume_improvements", []):
                    st.write(f"- {r}")

            else:
                st.error("❌ Failed to analyze resume.")
                st.text(response.text)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

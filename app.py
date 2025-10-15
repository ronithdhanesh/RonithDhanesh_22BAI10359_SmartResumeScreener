import os
import streamlit as st
from backend.parsing_utils import structured_data, parse_job_description
from backend.match_job import match_job


st.set_page_config(page_title="Smart Resume Screener By Legend Ronith Dhanesh", layout="wide", page_icon="🤖")

st.title("🤖 Smart Resume Screener")
st.caption("AI-powered ATS that matches resumes with job descriptions")


uploaded_file = st.file_uploader("📄 Upload a Resume (PDF)", type=["pdf"])
jd_text = st.text_area("🧾 Paste Job Description", height=200)


if uploaded_file and jd_text:
    if st.button("🔍 Analyze Match"):
        with st.spinner("Extracting and analyzing... ⏳"):
            temp_path = os.path.join("temp_resume.pdf")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            resume_data = structured_data(temp_path)
            jd_data = parse_job_description(jd_text)

            result = match_job(resume_data, jd_data)


        st.subheader("📊 Match Results")
        st.metric("Match Score", f"{result['match_score']}%")
        st.progress(result['match_score'] / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("✅ **Matched Skills**")
            for skill in result.get("matched_skills", []):
                st.markdown(f"- {skill}")

        with col2:
            st.markdown("⚠️ **Missing Skills**")
            for skill in result.get("missing_skills", []):
                st.markdown(f"- {skill}")

        st.markdown("### 🧠 Summary of Fit")
        st.write(result["summary_of_fit"])

        st.markdown("### 🎓 Education Relevance")
        st.write(result["education_relevance"])

        st.markdown("### 💼 Experience Relevance")
        st.write(result["experience_relevance"])

        st.markdown("### 🏁 Recommendation")
        st.success(result["recommendation"])

else:
    st.info("Upload a resume and paste a job description to begin.")

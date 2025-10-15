import os
import streamlit as st
from backend.parsing_utils import structured_data, parse_job_description
from backend.match_job import match_job
from backend.database import SessionLocal, Resume, JobDescription, Match  # ✅ NEW IMPORTS


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

            try:
                session = SessionLocal()

                resume = Resume(
                    name=resume_data.get("Name"),
                    email=resume_data.get("Email"),
                    phone=resume_data.get("Phone"),
                    skills=resume_data.get("Skills"),
                    education=resume_data.get("Education"),
                    projects=resume_data.get("Projects"),
                    parsed_data=resume_data,
                )
                session.add(resume)
                session.commit()

                job = JobDescription(
                    title=jd_data.get("role"),
                    company=jd_data.get("company"),
                    required_skills=jd_data.get("required_skills"),
                    jd_data=jd_data,
                )
                session.add(job)
                session.commit()

                match_entry = Match(
                    resume_id=resume.id,
                    job_id=job.id,
                    match_score=result.get("match_score"),
                    summary_of_fit=result.get("summary_of_fit"),
                    matched_skills=result.get("matched_skills"),
                    missing_skills=result.get("missing_skills"),
                )
                session.add(match_entry)
                session.commit()

            except Exception as e:
                st.error(f"⚠️ Error saving to database: {e}")
            finally:
                session.close()


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

        st.sidebar.markdown("[📊 Open Recruiter Dashboard →](http://localhost:8502)")

else:
    st.info("Upload a resume and paste a job description to begin.")

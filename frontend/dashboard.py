import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from backend.database import SessionLocal, Resume, JobDescription, Match
from datetime import datetime

st.set_page_config(page_title="Recruiter Dashboard", layout="wide", page_icon="📊")

st.title("📊 Smart Resume Screener — Recruiter Dashboard")
st.caption("View resumes, job descriptions, and match results in one place.")

session = SessionLocal()

page = st.sidebar.radio(
    "Navigate",
    ["📄 Resumes", "🧾 Job Descriptions", "📈 Match Results"]
)


if page == "📄 Resumes":
    st.header("📄 Candidate Resumes")

    resumes = session.query(Resume).all()
    if not resumes:
        st.info("No resumes found yet.")
    else:
        df = pd.DataFrame([
            {
                "ID": r.id,
                "Name": r.name,
                "Email": r.email,
                "Phone": r.phone,
                "Skills Count": len(r.skills or []),
                "Created": r.created_at.strftime("%Y-%m-%d"),
            }
            for r in resumes
        ])
        st.dataframe(df, use_container_width=True)

        selected_id = st.selectbox("Select Resume ID to view details:", df["ID"])
        selected_resume = next(r for r in resumes if r.id == selected_id)
        st.subheader(f"📋 Resume Details — {selected_resume.name}")
        st.json(selected_resume.parsed_data)


elif page == "🧾 Job Descriptions":
    st.header("🧾 Job Descriptions")

    jobs = session.query(JobDescription).all()
    if not jobs:
        st.info("No job descriptions available.")
    else:
        df = pd.DataFrame([
            {
                "ID": j.id,
                "Title": j.title,
                "Company": j.company or "N/A",
                "Skill Count": len(j.required_skills or []),
                "Created": j.created_at.strftime("%Y-%m-%d"),
            }
            for j in jobs
        ])
        st.dataframe(df, use_container_width=True)

        selected_id = st.selectbox("Select Job ID to view details:", df["ID"])
        selected_job = next(j for j in jobs if j.id == selected_id)
        st.subheader(f"🏢 Job Details — {selected_job.title}")
        st.json(selected_job.jd_data)


elif page == "📈 Match Results":
    st.header("📈 Match Analysis")

    matches = session.query(Match).all()
    if not matches:
        st.info("No match results available.")
    else:
        df = pd.DataFrame([
            {
                "Match ID": m.id,
                "Resume ID": m.resume_id,
                "Job ID": m.job_id,
                "Match Score": m.match_score,
                "Date": m.created_at.strftime("%Y-%m-%d"),
            }
            for m in matches
        ])
        st.dataframe(df, use_container_width=True)

        
        top_matches = df.sort_values(by="Match Score", ascending=False).head(5)
        st.subheader("🏆 Top 5 Matches")
        st.bar_chart(top_matches.set_index("Match ID")["Match Score"])

        selected_id = st.selectbox("Select Match ID to view details:", df["Match ID"])
        selected_match = next(m for m in matches if m.id == selected_id)

        st.subheader("📊 Match Details")
        st.metric("Match Score", f"{selected_match.match_score}%")
        st.markdown("### ✅ Matched Skills")
        st.write(selected_match.matched_skills)
        st.markdown("### ⚠️ Missing Skills")
        st.write(selected_match.missing_skills)
        st.markdown("### 🧠 Summary of Fit")
        st.write(selected_match.summary_of_fit)

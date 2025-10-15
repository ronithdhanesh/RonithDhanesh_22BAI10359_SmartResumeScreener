# 🤖 Smart Resume Screener  
### *AI-powered ATS for Recruiters — Built by Legend Ronith Dhanesh*

---

## 🧭 Overview

**Smart Resume Screener** is an intelligent Applicant Tracking System (ATS) that leverages **LLMs**, **LangChain**, and **LlamaParse** to automatically analyze resumes, extract structured information, and match candidates to job descriptions based on skills, education, and project relevance.

Recruiters can:
- Upload any **resume (PDF)**  
- Paste any **job description**  
- Get an instant **match score**, **fit summary**, and **skill gap analysis**  
- View results in an interactive **Streamlit dashboard**

---

## 🏗️ System Architecture

```
                ┌──────────────────────────┐
                │        User (HR)         │
                │ Upload Resume + JD Input │
                └────────────┬─────────────┘
                             │
                             ▼
                 ┌──────────────────────────┐
                 │      Streamlit UI        │
                 │   (app.py interface)     │
                 └────────────┬─────────────┘
                             │
                             ▼
        ┌──────────────────────────────────────────────┐
        │                Backend Layer                 │
        │----------------------------------------------│
        │ 1. Resume Parser (LlamaParse + Gemini)       │
        │ 2. JD Parser (LangChain + Gemini)            │
        │ 3. Match Engine (LLM-based Scoring)          │
        │ 4. Database ORM (SQLAlchemy - SQLite/Postgres)│
        └───────────────────┬──────────────────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │  Database (SQLAlchemy)   │
                │  - Resumes               │
                │  - Job Descriptions      │
                │  - Match Results         │
                └──────────────────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │ Streamlit Dashboard      │
                │ (dashboard.py)           │
                │ Recruiter analytics view │
                └──────────────────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit |
| **Backend / LLM Framework** | LangChain |
| **LLM Provider** | Google Gemini (via `langchain-google-genai`) |
| **Document Parsing** | LlamaParse |
| **Database** | SQLAlchemy (SQLite / PostgreSQL) |
| **Environment Management** | python-dotenv |

---

## 🧠 LLM Prompt Design

### 1️⃣ Resume Extraction Prompt
```text
You are an expert resume parser.
Read the following resume text and extract structured details.

Required fields:
- name
- email
- phone
- linkedin
- github
- education (degree, institution, years)
- skills (grouped if possible)
- experience (company, role, duration, description)
- projects (title, description, technologies)
- certifications
- languages

Resume text:
```
→ Used in `structured_data()` (Resume Parser with LlamaParse + Gemini)

---

### 2️⃣ Job Description Extraction Prompt
```text
You are an expert HR analyst.
Extract key structured information from the following job description text.

Required JSON fields:
- role
- company (if available)
- experience_required
- education_required
- key_responsibilities (list)
- required_skills (list)
- preferred_skills (list)
- location
- employment_type
- salary_range

Job Description:
```
→ Used in `parse_job_description()` (LangChain + Gemini)

---

### 3️⃣ Resume vs Job Matching Prompt
```text
You are an experienced Technical Recruiter.

Compare the structured resume data and job description data.
Provide:
1. A match score (0–100)
2. A short summary of overall fit
3. Lists of matched skills and missing skills
4. Comments on education and experience relevance
5. A one-line recommendation (e.g., "Strong fit", "Moderate fit", "Not a fit")

Output strictly in JSON.
```
→ Used in `match_job()` chain.

---

## 🧩 Database Schema

**1️⃣ Resumes Table**
| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| name | Text | Candidate name |
| email | Text | Candidate email |
| phone | Text | Contact info |
| skills | JSON | Parsed skills |
| education | JSON | Parsed education |
| projects | JSON | Parsed projects |
| parsed_data | JSON | Full structured resume |
| created_at | DateTime | Timestamp |

**2️⃣ Job Descriptions Table**
| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| title | Text | Role title |
| company | Text | Company |
| required_skills | JSON | Parsed skills |
| jd_data | JSON | Full JD data |
| created_at | DateTime | Timestamp |

**3️⃣ Matches Table**
| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| resume_id | FK | Resumes.id |
| job_id | FK | JobDescriptions.id |
| match_score | Integer | Fit score |
| summary_of_fit | Text | LLM summary |
| matched_skills | JSON | Overlaps |
| missing_skills | JSON | Gaps |
| created_at | DateTime | Timestamp |

---

## 💻 Local Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/smart-resume-screener.git
cd smart-resume-screener
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # on macOS/Linux
.venv\Scripts\activate      # on Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your API Key
Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///smart_screener.db
```

### 5️⃣ Initialize the Database
```bash
python
>>> from backend.database import init_db
>>> init_db()
```

### 6️⃣ Run the Streamlit Apps
**Main Screener:**
```bash
streamlit run app.py --server.port 8501
```

**Recruiter Dashboard:**
```bash
streamlit run dashboard.py --server.port 8502
```

---

## 📊 Dashboard Features

- View all parsed resumes and job postings  
- Inspect structured JSON outputs  
- See match results, filter by score  
- View top candidate matches by job  
- Export or analyze data for reports  

---

## 🔮 Future Improvements
- Semantic candidate search using vector embeddings (LangChain + Chroma)  
- Auto email shortlist notifications to recruiters  
- Integration with HR platforms (Greenhouse, Lever, etc.)  
- Fine-tuned LLM for domain-specific job categories  

---

## 👑 Author
**Legend Ronith Dhanesh**  
*Developer, AI Engineer, and Creator of Smart Resume Screener*

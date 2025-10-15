import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()


def match_job(job_desc : dict, resume : dict):
    prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and HR analyst.
Compare the following candidate resume data with the given job description data.

You must analyze:
- Skill match and gaps
- Education relevance
- Experience relevance
- Project and domain alignment

Then, provide a structured JSON output with the following fields:
- match_score (0–100)
- summary_of_fit (2–3 sentences)
- matched_skills (list)
- missing_skills (list)
- education_relevance
- experience_relevance
- recommendation ("Strong Fit", "Moderate Fit", or "Not a Fit")

Resume Data:
{resume_data}

Job Description Data:
{jd_data}

Return ONLY valid JSON.""")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    parser = JsonOutputParser()

    chain = prompt | llm | parser 

    analysis = chain.invoke({"resume_data" : resume, "jd_data" : job_desc})

    return analysis





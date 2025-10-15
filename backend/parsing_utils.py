import os 
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def structured_data(file_path : str):
    parser = LlamaParse(result_type="markdown")
    results = parser.load_data(file_path)
    resume_text = "\n".join(doc.text for doc in results)


    prompt = ChatPromptTemplate.from_template("""
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
    {resume_text}
    ```

    Return ONLY valid JSON.""")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    json_parser = JsonOutputParser()

    chain = prompt | llm | json_parser

    structured_data = chain.invoke({"resume_text" : resume_text})
    return structured_data


def parse_job_description(jd_text: str):
    prompt = ChatPromptTemplate.from_template("""
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
    - location (if mentioned)
    - employment_type (Full-time / Contract / Internship)
    - salary_range (if mentioned)

    Job Description:
    {jd_text}

    Return JSON only.
    """)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    chain = prompt | llm | JsonOutputParser()
    parsed_jd = chain.invoke({"jd_text" : jd_text})
    return parsed_jd


if __name__ == "__main__":
    # file_path = r"C:\Users\USER\Desktop\Projects\local_rag\Ronith Dhanesh.pdf"
    # structured_info = structured_data(file_path)
    # print(structured_info)
    pass

    

    
from backend.parsing_utils import structured_data, parse_job_description
from backend.match_job import match_job

if __name__ == "__main__":
    jd = """AI Intern 
Mumbai, Maharashtra, India · 4 weeks ago · Over 100 applicants
Promoted by hirer · Actively reviewing applicants


 On-site
Matches your job preferences, workplace type is On-site.

 Internship
Matches your job preferences, job type is Internship.

Easy Apply

Save
Save AI Intern  at Avendus
AI Intern
Avendus · Mumbai, Maharashtra, India (On-site)

Easy Apply

Save
Save AI Intern  at Avendus
Show more options
How your profile and resume fit this job
Get AI-powered advice on this job and more exclusive features with Premium. Try Premium for ₹0




Tailor my resume to this job

Am I a good fit for this job?

How can I best position myself for this job?

People you can reach out to
Kartavya profile photo
Kartavya profile photo
Kartavya Asthana 
Kartavya Asthana is verified 
· 3rd
Avendus Capital • IIM Calcutta Co'25
School alum from Vellore Institute of Technology

Message
About the job
Duration: 6 months starting Aug'25 first week (non-negotiable)
Working Model: Full-time onsite (candidate need to arrange required NOC from the college)
Location: BKC, Mumbai


About Us

Avendus is a leading global financial services firm. With a robust track record of delivering exceptional results, Avendus offers strategic advisory services, capital raising solutions, institutional broking, funds and comprehensive wealth management to a diverse clientele. The firm leverages deep industry knowledge, a vast network, and innovative approaches to drive growth and value for its clients through technology. Avendus is committed to excellence, integrity, and building lasting partnerships in the financial landscape.


Role Overview

As an AI Intern, you will play a key role in developing and optimizing knowledge graph algorithms and exploring applications of generative AI. Your responsibilities will include solving complex problems at the intersection of these technologies.


Key Responsibilities

Knowledge Graph Algorithms: Work on developing and optimizing algorithms related to knowledge graphs.
Generative AI: Apply generative AI techniques to solve complex problems and enhance existing solutions.
Frontend Development: Build and maintain frontend applications to facilitate the consumption of developed solutions.
Vendor Collaboration: Running MVPs and collaborating with different vendors.
Project Involvement: Contribute to various other projects as needed, providing support and insight into different areas.


Requirements



Technical Skills

Extensive programming experience with a track record of completing technical projects.
Proficiency in Python.
Experience with machine learning techniques and tools.
Knowledge and Experience:

Understanding of knowledge graph algorithms and their applications.
Familiarity with generative AI and its practical uses.
Experience with frontend development frameworks and tools.
Education:

Pursuing or completed a degree in Computer Science, Data Science, Engineering, or a related field.
Additional Skills:

Strong problem-solving abilities and analytical skills.
Excellent communication and teamwork skills.
Ability to manage multiple tasks and projects effectively.


What We Offer

Learning Experience: Gain hands-on experience in cutting-edge technologies and real-world applications.
Mentorship: Work closely with experienced professionals and receive guidance on career development.
Dynamic Environment: Be part of a forward-thinking team and work on innovative projects."""

parsed_jd = parse_job_description(jd)
file_path = r"C:\Users\USER\Desktop\Projects\local_rag\Ronith Dhanesh.pdf"
parsed_resume = structured_data(file_path)

analysis = match_job(parsed_jd, parsed_resume)
print(analysis)


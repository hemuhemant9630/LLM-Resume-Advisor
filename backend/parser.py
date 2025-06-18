# import re
# from typing import Dict

# def parse_resume_sections(text: str) -> Dict[str, str]:
#     sections = {
#         "education": "",
#         "experience": "",
#         "skills": "",
#         "projects": "",
#         "certifications": ""
#     }

#     text = text.lower()
    
#     patterns = {
#         "education": r"(education|academic background)(.*?)(experience|skills|projects|certifications|$)",
#         "experience": r"(experience|work history)(.*?)(education|skills|projects|certifications|$)",
#         "skills": r"(skills|technologies)(.*?)(experience|education|projects|certifications|$)",
#         "projects": r"(projects)(.*?)(experience|education|skills|certifications|$)",
#         "certifications": r"(certifications|courses)(.*?)(experience|education|skills|projects|$)"
#     }

#     for key, pattern in patterns.items():
#         match = re.search(pattern, text, re.DOTALL)
#         if match:
#             sections[key] = match.group(2).strip()

#     return sections


# import re

# def parse_resume_sections(text: str) -> dict:
#     """
#     Extract key sections from the resume based on common headings.
#     """
#     sections = {
#         "education": "",
#         "skills": "",
#         "projects": "",
#         "experience": "",
#         "certifications": ""
#     }

#     current_section = None
#     lines = text.split("\n")
#     buffer = []

#     for line in lines:
#         l = line.lower()

#         if "education" in l:
#             if current_section and buffer:
#                 sections[current_section] = "\n".join(buffer).strip()
#                 buffer = []
#             current_section = "education"

#         elif "skill" in l:
#             if current_section and buffer:
#                 sections[current_section] = "\n".join(buffer).strip()
#                 buffer = []
#             current_section = "skills"

#         elif "project" in l:
#             if current_section and buffer:
#                 sections[current_section] = "\n".join(buffer).strip()
#                 buffer = []
#             current_section = "projects"

#         elif "experience" in l or "work history" in l:
#             if current_section and buffer:
#                 sections[current_section] = "\n".join(buffer).strip()
#                 buffer = []
#             current_section = "experience"

#         elif "certification" in l or "courses" in l:
#             if current_section and buffer:
#                 sections[current_section] = "\n".join(buffer).strip()
#                 buffer = []
#             current_section = "certifications"

#         elif current_section:
#             buffer.append(line)

#     # Save last buffer
#     if current_section and buffer:
#         sections[current_section] = "\n".join(buffer).strip()

#     return sections
def parse_resume_sections(text: str) -> dict:
    sections = {
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "certifications": ""
    }
    current_section = None
    buffer = []

    for line in text.split("\n"):
        l = line.lower().strip()
        
        # Check if this line is a section header
        new_section = None
        if "education" in l: new_section = "education"
        elif "skill" in l: new_section = "skills"
        elif "project" in l: new_section = "projects"
        elif "experience" in l or "work history" in l: new_section = "experience"
        elif "certification" in l or "course" in l: new_section = "certifications"

        # If we found a new section, save the current buffer and start a new one
        if new_section:
            if current_section and buffer:
                sections[current_section] = '\n'.join(buffer).strip()
            current_section = new_section
            buffer = []
        # If we're in a section, add the line to the buffer
        elif current_section and line.strip():
            buffer.append(line)

    # Don't forget to save the last section
    if current_section and buffer:
        sections[current_section] = '\n'.join(buffer).strip()

    return sections
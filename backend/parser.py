def parse_resume_sections(text: str) -> dict:
    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "certifications": ""
    }

    current_section = None
    lines = text.splitlines()

    for line in lines:
        line_lower = line.lower().strip()

        if "education" in line_lower:
            current_section = "education"
        elif "experience" in line_lower:
            current_section = "experience"
        elif "project" in line_lower:
            current_section = "projects"
        elif "skill" in line_lower:
            current_section = "skills"
        elif "certification" in line_lower:
            current_section = "certifications"
        elif current_section:
            sections[current_section] += line + "\n"

    return sections

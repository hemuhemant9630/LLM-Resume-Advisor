# import re

# def clean_text(text: str) -> str:
#     """
#     Cleans the raw resume text by removing extra whitespace, special characters, and non-informative lines.
#     """
#     # Remove non-ASCII characters
#     text = text.encode("ascii", errors="ignore").decode()
    
#     # Replace multiple newlines and spaces
#     text = re.sub(r'\n+', '\n', text)
#     text = re.sub(r'\s{2,}', ' ', text)

#     # Remove long empty whitespace and known garbage lines
#     lines = text.split('\n')
#     cleaned_lines = []
#     for line in lines:
#         line = line.strip()
#         if len(line) < 2:
#             continue
#         if re.match(r'^[-_=]{3,}$', line):  # lines with just ---- or ====
#             continue
#         cleaned_lines.append(line)

#     cleaned_text = '\n'.join(cleaned_lines).strip()
#     return cleaned_text


import re

def clean_text(text: str) -> str:
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 2 and not re.match(r'^[-_=]{3,}$', line)]
    return '\n'.join(cleaned_lines)


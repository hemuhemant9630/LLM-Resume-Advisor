import re

def clean_text(text: str) -> str:
    # Remove extra whitespace, non-ASCII, etc.
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

import re
from typing import List, Dict

HEADING_PATTERN = re.compile(
    r"^(?:[A-Z][A-Za-z0-9’'(),:&\- ]{3,})$"  
)

def split_into_sections(raw_text: str) -> List[Dict]:
    """
    Split page text into sections by:
      1) Detecting lines that match HEADING_PATTERN
      2) Treating those as titles; everything until the next title is that section's body.
    Fallback: if no headings found, single section with text.
    """
    lines = raw_text.splitlines()
    sections: List[Dict] = []
    current_title = None
    buffer: List[str] = []

    def flush():
        if current_title or buffer:
            sections.append({
                "section_title": current_title or "Untitled Section",
                "text": "\n".join(buffer).strip()
            })

    for line in lines:
        stripped = line.strip()
        if HEADING_PATTERN.match(stripped):
            flush()
            buffer = []
            current_title = stripped
        else:
            buffer.append(line)
    flush()
    return sections

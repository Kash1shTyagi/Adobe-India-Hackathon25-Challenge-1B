import json
from datetime import datetime
from typing import List, Dict, Any

def write_output(
    input_docs: List[str],
    persona: str,
    job_to_be_done: str,
    sections: List[Dict[str, Any]],
    subsections: List[Dict[str, Any]],
    output_path: str
) -> None:
    metadata = {
        "input_documents": input_docs,
        "persona": persona,
        "job_to_be_done": job_to_be_done,
        "processing_timestamp": datetime.now().isoformat()
    }

    payload = {
        "metadata": metadata,
        "extracted_sections": sections,
        "subsection_analysis": subsections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

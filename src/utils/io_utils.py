import json
from pathlib import Path
from typing import Tuple, List, Any

def load_input_config(input_path: Path) -> Tuple[str, str, List[Path]]:
    """
    Reads challenge1b_input.json and returns:
      (persona_text, job_to_be_done, list_of_pdf_paths)

    - If persona/job is a dict, combines its key fields into a single string.
    - Supports document entries as strings or dicts.
    """
    data = json.loads(input_path.read_text(encoding="utf-8"))
    
    raw_persona = data.get("persona") or data.get("role")
    if isinstance(raw_persona, dict):
        parts: List[str] = []
        for key in ("role", "expertise", "focus_areas"):
            if key in raw_persona:
                val = raw_persona[key]
                parts.append(", ".join(val) if isinstance(val, list) else str(val))
        persona = " | ".join(parts)
    else:
        persona = str(raw_persona or "")

    raw_job = data.get("job_to_be_done") or data.get("job")
    if isinstance(raw_job, dict):
        parts: List[str] = []
        for key in ("job_to_be_done", "task", "description"):
            if key in raw_job:
                val = raw_job[key]
                parts.append(str(val))
        job = " | ".join(parts)
    else:
        job = str(raw_job or "")

    raw_docs = data.get("documents") or data.get("input_documents") or []
    docs: List[Path] = []
    for entry in raw_docs:
        if isinstance(entry, str):
            docs.append(Path(entry))
        elif isinstance(entry, dict):
            for key in ("document", "filename", "name", "path"):
                if key in entry:
                    docs.append(Path(entry[key]))
                    break
            else:
                raise ValueError(f"Cannot parse document entry: {entry!r}")
        else:
            raise TypeError(f"Invalid document entry type: {type(entry)}")

    return persona, job, docs


import pdfplumber
import logging
from pathlib import Path
from typing import List, Dict

from .utils.text_utils import split_into_sections

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_dir: Path, input_docs: List[Path]):
        self.pdf_dir = pdf_dir
        self.input_docs = input_docs

    def extract_sections(self) -> List[Dict]:
        """
        Read each PDF, extract text per page, split into sections,
        and return list of dicts:
          {
            "document": str,
            "page_number": int,
            "section_title": str,
            "text": str
          }
        """
        all_sections: List[Dict] = []

        for path in self.input_docs:
            file_path = self.pdf_dir / path.name
            logger.info(f"Opening PDF {file_path}")
            with pdfplumber.open(file_path) as pdf:
                for page_idx, page in enumerate(pdf.pages, start=1):
                    raw_text = page.extract_text() or ""
                    sections = split_into_sections(raw_text)
                    for sec in sections:
                        sec.update({
                            "document": path.name,
                            "page_number": page_idx
                        })
                        all_sections.append(sec)
                logger.info(f" → extracted {len(all_sections)} sections so far")
        return all_sections

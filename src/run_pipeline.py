import argparse
import logging
from pathlib import Path

from .pdf_processor import PDFProcessor
from .embedder import Embedder
from .ranking import Ranker
from .json_writer import write_output
from .utils.io_utils import load_input_config

def parse_args():
    parser = argparse.ArgumentParser(description="Persona‑Driven Document Intelligence")
    parser.add_argument("--input",      type=Path, required=True, help="Path to challenge1b_input.json")
    parser.add_argument("--pdf-dir",    type=Path, required=True, help="Directory containing PDFs")
    parser.add_argument("--output",     type=Path, required=True, help="Where to write output JSON")
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s │ %(message)s",
    )

def main():
    setup_logging()
    args = parse_args()
    logging.info("Loading input config")
    persona, job, input_docs = load_input_config(args.input)

    logging.info("Processing PDFs into sections")
    processor = PDFProcessor(args.pdf_dir, input_docs)
    sections = processor.extract_sections()

    logging.info("Computing embeddings")
    embedder = Embedder(model_name="all-MiniLM-L6-v2")
    sections = embedder.embed_sections(sections, persona, job)

    logging.info("Ranking sections and subsections")
    ranker = Ranker(top_k_sections=10, top_k_subsections=5)
    ranked_sections, ranked_subsections = ranker.rank(sections)

    logging.info("Writing final JSON output")
    write_output(
        input_docs=[p.name for p in input_docs],
        persona=persona,
        job_to_be_done=job,
        sections=ranked_sections,
        subsections=ranked_subsections,
        output_path=str(args.output),
    )

if __name__ == "__main__":
    main()

from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, model_name: str):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name, device="cpu")

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    def embed_sections(
        self,
        sections: List[Dict],
        persona: str,
        job: str
    ) -> List[Dict]:
        query = persona.strip() + " " + job.strip()
        query_emb = self.embed_texts([query])[0]
        
        texts = [sec["text"] for sec in sections]
        sec_embs = self.embed_texts(texts)
        
        for sec, emb in zip(sections, sec_embs):
            sec["embedding"] = emb
            sec["query_embedding"] = query_emb
        return sections

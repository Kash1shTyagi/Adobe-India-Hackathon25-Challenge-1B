import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class Ranker:
    def __init__(self, top_k_sections: int = 10, top_k_subsections: int = 5):
        self.top_k_sections = top_k_sections
        self.top_k_subsections = top_k_subsections

    def rank(
        self,
        sections: List[Dict]
    ) -> Tuple[List[Dict], List[Dict]]:
        embs = np.stack([sec["embedding"] for sec in sections])
        qemb = np.stack([sec["query_embedding"] for sec in sections])[0]
        sims = cosine_similarity(embs, qemb.reshape(1, -1)).flatten()

        for sec, score in zip(sections, sims):
            sec["score"] = float(score)

        sections_sorted = sorted(sections, key=lambda x: x["score"], reverse=True)

        top_sections = []
        for rank, sec in enumerate(sections_sorted[:self.top_k_sections], start=1):
            top_sections.append({
                "document": sec["document"],
                "page_number": sec["page_number"],
                "section_title": sec.get("section_title", ""),
                "importance_rank": rank
            })

        subsections = []
        for sec_rank, sec in enumerate(sections_sorted[:self.top_k_sections], start=1):
            sentences = [s.strip() for s in sec["text"].split(". ") if s.strip()]
            if not sentences:
                continue
            emb_sents = self.model_encode(sentences)
            sim_sents = cosine_similarity(emb_sents, sec["query_embedding"].reshape(1, -1)).flatten()
            top_idx = np.argsort(sim_sents)[-self.top_k_subsections:]
            for sub_rank, idx in enumerate(reversed(top_idx), start=1):
                subsections.append({
                    "document": sec["document"],
                    "page_number": sec["page_number"],
                    "refined_text": sentences[idx],
                    "importance_rank": sub_rank,
                    "parent_rank": sec_rank
                })

        return top_sections, subsections

    def model_encode(self, texts: List[str]) -> np.ndarray:
        from .embedder import Embedder
        model = Embedder("all-MiniLM-L6-v2").model
        return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
import os
from indexer import Indexer
from sentence_transformers import CrossEncoder

load_dotenv()

class Retriever:
    def __init__(self, indexer: Indexer, config: Dict):
        self.indexer = indexer
        self.reranker = CrossEncoder(config['retrieval']['reranker_model'])  # Load cross-encoder
        self.vector_top_k = config['retrieval']['vector_top_k']
        self.bm25_top_k = config['retrieval']['bm25_top_k']
        self.rerank_top_k = config['retrieval']['rerank_top_k']
    
    def retrieve(self, query: str) -> str:
        query_embed = self.indexer.model.encode([query], convert_to_numpy=True)[0]
        query_embed = np.array([query_embed], dtype=np.float32)
        _, vec_indices = self.indexer.index.search(query_embed, self.vector_top_k)
        
        bm25_scores = self.indexer.bm25.get_scores(query.split())
        bm25_indices = np.argsort(bm25_scores)[::-1][:self.bm25_top_k]
        
        candidates = set(list(vec_indices[0]) + list(bm25_indices))
        candidate_chunks = [self.indexer.chunks[i] for i in candidates]
        
        # Rerank using cross-encoder
        documents = [c['text'] for c in candidate_chunks]
        pairs = [[query, doc] for doc in documents]
        rerank_scores = self.reranker.predict(pairs)
        rerank_indices = np.argsort(rerank_scores)[::-1][:self.rerank_top_k]
        
        # Sort by relevance scores
        sorted_candidates = [(rerank_scores[i], candidate_chunks[i]) for i in rerank_indices]
        context = '\n\n'.join([f"Page {c['page_num']}: {c['text']}" for _, c in sorted_candidates])
        return context
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from rank_bm25 import BM25Okapi
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()
model = SentenceTransformer('BAAI/bge-base-en-v1.5')  # Load free embedding model

class Indexer:
    def __init__(self, config: Dict):
        self.model = model  # Use pre-loaded model
        self.index = None
        self.bm25 = None
        self.chunks = []
    
    def build_indexes(self, chunks: List[Dict], faiss_path: str, chunks_path: str):
        self.chunks = chunks
        texts = [c['text'] for c in chunks]
        
        embeds = self.model.encode(texts, convert_to_numpy=True)
        embeds = np.array(embeds, dtype=np.float32)
        
        dim = embeds.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeds)
        faiss.write_index(self.index, faiss_path)
        
        tokenized_texts = [t.split() for t in texts]
        self.bm25 = BM25Okapi(tokenized_texts)
        
        with open(chunks_path, 'w') as f:
            json.dump(chunks, f)
    
    def load_indexes(self, faiss_path: str, chunks_path: str):
        self.index = faiss.read_index(faiss_path)
        with open(chunks_path, 'r') as f:
            self.chunks = json.load(f)
        texts = [c['text'] for c in self.chunks]
        self.bm25 = BM25Okapi([t.split() for t in texts])
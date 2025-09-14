from sentence_transformers import SentenceTransformer
import spacy
import yaml
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()
model = SentenceTransformer('BAAI/bge-base-en-v1.5')  # Load free embedding model
nlp = spacy.load("en_core_web_sm")

def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def chunk_page(page: Dict, config: Dict) -> List[Dict]:
    max_chunk_size = config['chunking']['max_chunk_size']
    overlap = config['chunking']['overlap']
    
    doc = nlp(page['text'])
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    if not sentences:
        return []
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for i, sent in enumerate(sentences):
        words = sent.split()
        word_count = len(words)
        
        if current_word_count + word_count > max_chunk_size and current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'page_num': page['page_num'],
                'metadata': {'chunk_id': len(chunks)}
            })
            overlap_sents = current_chunk[-int(len(current_chunk) * overlap):]
            current_chunk = overlap_sents + [sent]
            current_word_count = sum(len(s.split()) for s in current_chunk)
        else:
            current_chunk.append(sent)
            current_word_count += word_count
    
    if current_chunk:
        chunks.append({
            'text': ' '.join(current_chunk),
            'page_num': page['page_num'],
            'metadata': {'chunk_id': len(chunks)}
        })
    
    for i in range(len(chunks)):
        chunks[i]['metadata']['prev_chunk_id'] = chunks[i-1]['metadata']['chunk_id'] if i > 0 else None
        chunks[i]['metadata']['next_chunk_id'] = chunks[i+1]['metadata']['chunk_id'] if i < len(chunks)-1 else None
    
    return chunks
from flask import Flask, request, jsonify
from flask_cors import CORS   # 👈 add this
import yaml
from pdf_processor import extract_and_clean
from chunker import chunk_page, load_config
from indexer import Indexer
from retriever import Retriever
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 👈 allow all origins (or restrict to your frontend URL)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/query', methods=['POST'])
def query_manual():
    try:
        data = request.get_json()
        if not data or 'query' not in data or not data['query']:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        query = data['query']
        config = load_config("config.yaml")
        indexer = Indexer(config)
        
        faiss_path = "indexes/faiss_index.bin"
        chunks_path = "indexes/chunks.json"
        if not (os.path.exists(faiss_path) and os.path.exists(chunks_path)):
            pages = extract_and_clean("data/manual.pdf")
            chunks = []
            for page in pages:
                chunks.extend(chunk_page(page, config))
            indexer.build_indexes(chunks, faiss_path, chunks_path)
        else:
            indexer.load_indexes(faiss_path, chunks_path)
        
        retriever = Retriever(indexer, config)
        context = retriever.retrieve(query)
        
        # Prepare prompt for Gemini 2.5 Pro
        prompt = f"Answer based only on this context: {context}\n\nQuestion: {query}. \n Output: Provide a concise, accurate answer based *only* on the following context, avoiding speculation and don't say Based only on the provided context, the requirements only give answer."
        model = genai.GenerativeModel('gemini-2.5-pro')  # Use Gemini 2.5 Pro
        response = model.generate_content(prompt)
        answer = response.text if response else "Error generating response"
        
        return jsonify({'answer': answer, 'context': context})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

# RAG Q&A Bot for PDF Manual

## Overview

A RAG Q&A bot for a 500-page PDF manual using voyage-3-large embeddings and rerank-2.5 for high accuracy, built with Flask.

## Setup

1. Clone the repository:

```bash
git clone <repo_url>
cd rag_qa_bot
```
2. create virtual envirnoment:
   ```bash
   python -m venv venv
   ```
   Activate Virtual Environment:
   ```bash
   .\venv\Scripts\Activate
   ```

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. Set gemini API key in `.env`:

   ```bash
   echo "Gemini_API_Key=your_key_here" > .env
   ```

3. Place your PDF manual in `data/manual.pdf`.

4. Run the server:

   ```bash
   python app.py
   ```

   For production, use Gunicorn:

   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## Usage

Query via HTTP:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "How to troubleshoot error X?"}' http://localhost:8000/query
```
or 
By using postman:

HTTP method : POST

url : http://localhost:8000/query

Headers:

Key: Content-Type

Value: application/json

body :

raw : json

{

  "query": "What are the changes from OASIS-E to OASIS-E1?"

}

example response:

{
  
  "answer": "The changes from OASIS-E to OASIS-E1 include: One new item (O0350) was added, two items (M0110, M2200) were removed, and three items (M1028, M1060, M1800) were revised for clarity. Additionally, for Medicare patients, an Occupational Therapist (OT) may now complete the comprehensive assessment when ordered with another qualifying rehabilitation therapy service (Speech-Language Pathology or Physical Therapy), a change noted in Chapter 1. The phrase 'usual status' was retired, replaced with reporting what is true greater than 50% of the time unless specified otherwise.", "context": "Page 269: Appendix D Description of Changes from OASIS-E to OASIS-E1 Edit # Chapter,Section,Page OASIS-E OASIS-E1 Description of Change • For Medicare patients, the OT may complete the comprehensive assessment... 5 Chapter 1... This section will be updated... 6 Chapter 1 General OASIS Item Convention #3 If the patient’s ability or status varies... Retired phrase 'usual status'..."

}

## Backend Integration with Flask

This project includes a chat system that integrates with a Flask backend for RAG (Retrieval-Augmented Generation) functionality. The frontend communicates with the Flask backend through a Supabase Edge Function that acts as a proxy.

### Local Development with ngrok

To run the Flask backend locally and connect it to your deployed Lovable app, you'll need to use ngrok to create a secure tunnel to your local development server.

#### Prerequisites

1. **Flask Backend Setup**: Ensure you have your Flask backend running locally
   - Your Flask backend should have an endpoint at `/query` that accepts POST requests
   - The request format should match: `{"query": "user input"}`
   - The response format should be: `{"answer": "response", "context": "context"}` or `{"error": "error message"}`

2. **Install ngrok**: Download and install ngrok from [ngrok.com](https://ngrok.com/)
   ```bash
   # On macOS with Homebrew
   brew install ngrok
   
   # On Windows with Chocolatey
   choco install ngrok
   
   # Or download directly from https://ngrok.com/download
   ```

3. **ngrok Account** (Optional but recommended): Sign up for a free ngrok account to get an auth token for stable URLs

#### Step-by-Step Setup

1. **Start your Flask backend locally**:
   ```bash
   # Example: Start your Flask app on port 8000
   python app.py
   # or
   flask run --port=8000
   ```

2. **Create ngrok tunnel**:
   ```bash
   # Create a tunnel to your local Flask backend
   ngrok http 8000
   ```

3. **Copy the ngrok URL**: ngrok will display a forwarding URL like:
   ```
   Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
   ```

#### Development Workflow

1. Start your Flask backend locally
2. Start ngrok tunnel (`ngrok http 8000`)
3. Update `FLASK_BACKEND_URL` in Supabase with the new ngrok URL
4. Test your chat functionality in the Lovable app
5. Make changes to your Flask backend and test in real-time

#### Troubleshooting

**Common Issues:**

- **"ngrok not found"**: Make sure ngrok is installed and in your PATH
- **Connection refused**: Ensure your Flask backend is running on the correct port
- **CORS errors**: Make sure your Flask backend includes proper CORS headers
- **502 Bad Gateway**: Check that the ngrok URL in `FLASK_BACKEND_URL` is correct and active

**Debug Tips:**

- Check the [Edge Function logs](https://supabase.com/dashboard/project/tqeindrtbjvbiqskogwk/functions/chat-query/logs) for connection errors
- Verify your Flask backend is responding at `http://localhost:8000/query`
- Test the ngrok URL directly in your browser or with curl

#### Production Deployment

For production, replace the ngrok URL with your deployed Flask backend URL in the `FLASK_BACKEND_URL` environment variable.


## Notes
- Indexes are rebuilt in indexes/ if missing (~100-200s).
- Latency ~600-800ms per query; tune rerank_top_k in config.yaml if needed.
- Enable CORS for frontend integration.
- Flask’s debug mode is enabled; disable in production (debug=False)

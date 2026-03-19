Complete Project Guide: PD Screening with RAG
🎯 Project Overview
This is a complete, production-ready AI system for text-based Parkinson's Disease screening using:

RAG (Retrieval-Augmented Generation) for evidence-based reasoning
Multiple LLM Support (GPT-4o, Claude, Mistral)
Medical Knowledge Base with PD research and clinical guidelines
Structured JSON Outputs with risk scores and recommendations
📦 What's Included
Core Components
Text Preprocessing - Cleans, normalizes, and extracts linguistic features
RAG Pipeline - Vector storage (ChromaDB/FAISS) and context retrieval
LLM Inference - Multi-provider support with structured prompts
Response Parser - Validates and formats JSON outputs
User Interfaces
CLI - Command-line interface for quick screenings
Streamlit Web App - User-friendly web interface
Flask REST API - HTTP endpoints for integration
Additional Features
Medical knowledge base builder
Comprehensive test suite
Sample transcripts for testing
Configuration management
Logging and monitoring
🚀 Quick Start (5 Minutes)
Option 1: Automated Setup
bash
# 1. Make setup script executable
chmod +x setup.sh

# 2. Run setup
./setup.sh

# 3. Add API key to .env
echo "OPENAI_API_KEY=your-key-here" >> .env

# 4. Run interactive CLI
source venv/bin/activate
python src/main.py --interactive
Option 2: Manual Setup
bash
# 1. Create environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 4. Configure
cp .env.example .env
# Edit .env and add API keys

# 5. Build knowledge base
cd src/rag && python build_knowledge_base.py && cd ../..

# 6. Run
python src/main.py --interactive
📊 Usage Examples
Example 1: CLI Screening
bash
python src/main.py --transcript "My handwriting has become smaller and my voice is softer."
Example 2: Python API
python
from main import PDScreeningSystem

system = PDScreeningSystem()
results = system.screen_transcript(
    "I have a resting tremor and slow movements."
)

print(f"Risk: {results['screening_response']['risk_score']}")
print(f"Recommendation: {results['screening_response']['recommendation']}")
Example 3: Web Interface
bash
streamlit run ui/streamlit_app.py
# Open http://localhost:8501
Example 4: REST API
bash
# Start server
python ui/flask_api.py

# Make request
curl -X POST http://localhost:5000/api/v1/screen \
  -H "Content-Type: application/json" \
  -d '{"transcript": "My speech is quiet and slow."}'
🔧 Configuration Guide
Basic Configuration (config.yaml)
yaml
llm:
  provider: "openai"  # openai, anthropic, mistral
  model: "gpt-4o"
  temperature: 0.1
  
rag:
  vector_store: "chromadb"
  top_k: 3
  similarity_threshold: 0.7
  
preprocessing:
  min_word_count: 5
Environment Variables (.env)
bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=...
📋 System Architecture
User Input (Transcript)
         ↓
   Preprocessing
   - Clean text
   - Tokenize
   - Extract linguistic features
         ↓
   RAG Retrieval
   - Embed query
   - Search vector store
   - Retrieve top-K passages
         ↓
   LLM Inference
   - Combine transcript + context
   - Generate screening assessment
   - Return structured JSON
         ↓
   Response Parser
   - Validate JSON structure
   - Check consistency
   - Format output
         ↓
   Structured Output
   {risk_score, confidence, rationale, recommendation}

# Parkinson's Disease Text-Based Screening with RAG

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete AI-powered system for text-based screening of Parkinson's Disease using Retrieval-Augmented Generation (RAG) and Large Language Models.

## ⚠️ Medical Disclaimer

**This tool is for screening purposes only and does NOT provide medical diagnoses.** It uses artificial intelligence to assess potential risk indicators based on text patterns and medical literature. Always consult qualified healthcare professionals for proper medical evaluation and diagnosis.

## 🎯 Project Overview

This system analyzes text transcripts (typed or from speech recognition) to identify linguistic and speech patterns potentially associated with Parkinson's Disease, using:

- **RAG Pipeline**: Retrieves relevant medical context from a curated knowledge base
- **Multiple LLM Support**: GPT-4o, Claude, Mistral, or local models
- **Evidence-Based**: Grounded in MDS-UPDRS guidelines and PD research
- **Structured Output**: Returns JSON with risk scores, confidence, and recommendations

## 🚀 Features

- ✅ Text preprocessing with linguistic feature extraction
- ✅ Vector storage with ChromaDB/FAISS
- ✅ Medical knowledge base with PD research
- ✅ Multi-LLM inference (OpenAI, Anthropic, Mistral)
- ✅ Structured JSON responses
- ✅ Streamlit web interface
- ✅ Flask REST API
- ✅ Comprehensive test suite
- ✅ Modular, extensible architecture

## 📁 Project Structure

```
parkinsons-screening-rag/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── config.yaml                    # Configuration settings
├── .env.example                   # Environment variables template
│
├── src/                           # Source code
│   ├── main.py                    # Main orchestrator
│   ├── preprocessing.py           # Text preprocessing
│   │
│   ├── rag/                       # RAG components
│   │   ├── vector_store.py        # Vector storage (ChromaDB/FAISS)
│   │   ├── retriever.py           # Context retrieval
│   │   └── build_knowledge_base.py # KB builder
│   │
│   └── llm/                       # LLM components
│       ├── inference.py           # Multi-LLM inference
│       ├── prompts.py             # Prompt templates
│       └── response_parser.py     # JSON validation
│
├── data/                          # Data directory
│   ├── knowledge_base/            # Medical documents
│   ├── chroma_db/                 # ChromaDB storage
│   └── sample_transcripts.txt    # Example inputs
│
├── tests/                         # Test suite
│   ├── test_preprocessing.py
│   ├── test_rag.py
│   ├── test_llm.py
│   └── test_end_to_end.py
│
└── ui/                            # User interfaces
    ├── streamlit_app.py           # Web UI
    └── flask_api.py               # REST API
```

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- API keys for LLM providers (OpenAI, Anthropic, or Mistral)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd parkinsons-screening-rag
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Example `.env`:
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
MISTRAL_API_KEY=your_mistral_key_here
```

6. **Build knowledge base**
```bash
cd src/rag
python build_knowledge_base.py --config ../../config.yaml
```

## 📖 Usage

### Command Line Interface

```bash
# Single transcript screening
python src/main.py --transcript "My speech has become softer and my handwriting smaller."

# Interactive mode
python src/main.py --interactive

# System statistics
python src/main.py --stats
```

### Streamlit Web Interface

```bash
streamlit run ui/streamlit_app.py
```

Then open http://localhost:8501 in your browser.

### Flask REST API

```bash
python ui/flask_api.py --host 0.0.0.0 --port 5000
```

API endpoints:
- `GET /health` - Health check
- `GET /api/v1/stats` - System statistics
- `POST /api/v1/screen` - Screen single transcript
- `POST /api/v1/batch-screen` - Batch screening
- `POST /api/v1/validate` - Validate transcript
- `GET /api/v1/docs` - API documentation

Example API call:
```bash
curl -X POST http://localhost:5000/api/v1/screen \
  -H "Content-Type: application/json" \
  -d '{"transcript": "I notice trembling in my right hand when resting.", "include_details": true}'
```

### Python API

```python
from main import PDScreeningSystem

# Initialize system
system = PDScreeningSystem(config_path='config.yaml')

# Screen transcript
transcript = "My voice has become quieter and I have trouble with balance."
results = system.screen_transcript(transcript, include_details=True)

# Print formatted results
system.screen_and_display(transcript)
```

## 📊 Output Format

The system returns structured JSON:

```json
{
  "success": true,
  "screening_response": {
    "risk_score": 0.65,
    "confidence": "medium",
    "rationale": [
      "Hypophonia (reduced vocal volume) is a recognized speech change in PD",
      "Balance difficulties align with postural instability symptoms",
      "Multiple motor symptoms warrant further evaluation"
    ],
    "recommendation": "refer for evaluation"
  },
  "metadata": {
    "preprocessing": {
      "is_valid": true,
      "features": {
        "word_count": 15,
        "sentence_count": 1,
        "lexical_diversity": 0.933
      }
    },
    "retrieval": {
      "num_passages": 3
    },
    "llm": {
      "provider": "openai",
      "model": "gpt-4o"
    }
  }
}
```

### Risk Score Interpretation

- **0.0 - 0.3**: Low risk - minimal linguistic indicators
- **0.4 - 0.6**: Moderate risk - some concerning patterns
- **0.7 - 1.0**: Higher risk - multiple indicators present

### Recommendations

- **insufficient data**: Transcript too short or unclear
- **monitor**: Low to moderate risk, continue monitoring
- **refer for evaluation**: Higher risk, professional evaluation recommended

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
llm:
  provider: "openai"  # openai, anthropic, mistral
  model: "gpt-4o"
  temperature: 0.1

rag:
  vector_store: "chromadb"  # chromadb, faiss
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  top_k: 3
  similarity_threshold: 0.7

preprocessing:
  lowercase: true
  min_word_count: 5
```

## 🧪 Testing

Run the test suite:

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_preprocessing.py -v

# With coverage
pytest --cov=src tests/
```

Individual module tests:
```bash
python src/preprocessing.py
python src/rag/vector_store.py
python src/rag/retriever.py
python src/llm/prompts.py
python src/llm/response_parser.py
```

## 📚 Knowledge Base

The system includes curated medical knowledge covering:

- MDS-UPDRS clinical guidelines
- Parkinson's speech and language research
- NIH and Parkinson's Foundation summaries
- Motor and non-motor symptoms
- Linguistic features in PD
- Early warning signs

### Adding Custom Documents

1. Place `.txt` files in `data/knowledge_base/`
2. Run the knowledge base builder:
```bash
python src/rag/build_knowledge_base.py --load-dir --clear
```

## 🔧 Advanced Usage

### Using Different LLM Providers

**OpenAI (GPT-4o)**:
```yaml
llm:
  provider: "openai"
  model: "gpt-4o"
```

**Anthropic (Claude)**:
```yaml
llm:
  provider: "anthropic"
  model: "claude-sonnet-4-20250514"
```

**Mistral**:
```yaml
llm:
  provider: "mistral"
  model: "mistral-large"
```

### Custom Prompts

Modify `src/llm/prompts.py` to customize the system and user prompts.

### Batch Processing

```python
from main import PDScreeningSystem

system = PDScreeningSystem()

transcripts = [
    "Transcript 1 text...",
    "Transcript 2 text...",
    "Transcript 3 text..."
]

for i, transcript in enumerate(transcripts):
    print(f"\nProcessing transcript {i+1}...")
    results = system.screen_transcript(transcript)
    print(f"Risk Score: {results['screening_response']['risk_score']}")
```

## 🔍 Future Enhancements

- [ ] Support for audio file input with ASR integration
- [ ] Integration with mPower, UCI, and PPMI datasets
- [ ] Multi-language support
- [ ] Advanced acoustic feature analysis
- [ ] Longitudinal tracking and trend analysis
- [ ] Clinical validation studies
- [ ] HIPAA-compliant deployment options

## 📊 Performance Considerations

### Optimization Tips

1. **Use smaller embedding models** for faster processing:
```yaml
rag:
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"  # Fast & efficient
```

2. **Adjust retrieval parameters**:
```yaml
rag:
  top_k: 2  # Fewer passages = faster
  similarity_threshold: 0.75  # Higher threshold = more selective
```

3. **Enable caching**:
```yaml
features:
  enable_caching: true
```

## 🐛 Troubleshooting

### Common Issues

**1. ChromaDB initialization fails**
```bash
# Clear existing database
rm -rf data/chroma_db/*
python src/rag/build_knowledge_base.py --clear
```

**2. API key errors**
- Verify `.env` file exists and contains valid keys
- Check environment variables: `echo $OPENAI_API_KEY`

**3. NLTK data missing**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

**4. Import errors**
```bash
# Ensure you're in the correct directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**5. Memory issues with large knowledge bases**
- Use FAISS instead of ChromaDB for large-scale deployments
- Reduce chunk_size in config.yaml
- Limit top_k retrieval count

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **MDS-UPDRS**: Movement Disorder Society Unified Parkinson's Disease Rating Scale
- **NIH**: National Institute of Health Parkinson's Disease Information
- **Parkinson's Foundation**: Educational resources and clinical guidelines
- Research community for PD speech and language studies

## 📧 Contact & Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## 🔐 Privacy & Security

- **No data storage**: Transcripts are processed in-memory only
- **API keys**: Stored securely in environment variables
- **HIPAA compliance**: For clinical use, additional security measures required
- **Audit logging**: Available through loguru configuration

## 📖 References

1. Movement Disorder Society UPDRS
2. Speech characteristics in Parkinson's disease (Multiple research papers)
3. NIH Parkinson's Disease Information Page
4. Parkinson's Foundation Clinical Resources
5. mPower Study (Sage Bionetworks)
6. UCI ML Repository - Parkinson's datasets
7. PPMI (Parkinson's Progression Markers Initiative)

## 🎓 Research & Citations

If you use this system in research, please cite:

```bibtex
@software{pd_screening_rag,
  title={Text-Based Parkinson's Disease Screening with RAG},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/parkinsons-screening-rag}
}
```

---

## Quick Start Example

```python
from main import PDScreeningSystem

# 1. Initialize
system = PDScreeningSystem()

# 2. Screen a transcript
transcript = """
I've noticed my handwriting has gotten much smaller over the past 
few months. My voice seems softer and people ask me to speak up. 
I also have a slight tremor in my right hand when it's at rest.
"""

# 3. Get results
results = system.screen_transcript(transcript)

# 4. Display
print(f"Risk Score: {results['screening_response']['risk_score']}")
print(f"Recommendation: {results['screening_response']['recommendation']}")
for point in results['screening_response']['rationale']:
    print(f"  - {point}")
```

**Output:**
```
Risk Score: 0.72
Recommendation: refer for evaluation
  - Micrographia (small handwriting) is a common early motor symptom
  - Hypophonia (soft voice) is a recognized speech change in PD
  - Resting tremor is a cardinal motor symptom of Parkinson's disease
  - Multiple symptoms suggest need for professional evaluation
```

---

**Built with ❤️ for the Parkinson's research community**
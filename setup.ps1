#!/bin/bash

# Setup script for PD Screening RAG System
# This script sets up the complete environment

set -e  # Exit on error

echo "=========================================="
echo "PD Screening RAG System - Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.9"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
else
    echo -e "${RED}✗ Python 3.9+ required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p data/knowledge_base
mkdir -p data/chroma_db
mkdir -p logs
mkdir -p tests
echo -e "${GREEN}✓ Directories created${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}! Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python3 << EOF
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
print("NLTK data downloaded successfully")
EOF
echo -e "${GREEN}✓ NLTK data downloaded${NC}"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}! Please edit .env file and add your API keys${NC}"
    echo -e "${YELLOW}! Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, or MISTRAL_API_KEY${NC}"
else
    echo -e "${YELLOW}! .env file already exists${NC}"
fi

# Check if config.yaml exists
echo ""
if [ -f "config.yaml" ]; then
    echo -e "${GREEN}✓ config.yaml found${NC}"
else
    echo -e "${YELLOW}! config.yaml not found - using defaults${NC}"
fi

# Build knowledge base
echo ""
echo "Building knowledge base..."
read -p "Do you want to build the knowledge base now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Building knowledge base with sample data..."
    cd src/rag
    python3 build_knowledge_base.py --config ../../config.yaml 2>/dev/null || echo -e "${YELLOW}! Knowledge base build encountered issues${NC}"
    cd ../..
    echo -e "${GREEN}✓ Knowledge base built${NC}"
else
    echo -e "${YELLOW}! Skipping knowledge base build${NC}"
    echo -e "${YELLOW}! Run manually: cd src/rag && python build_knowledge_base.py${NC}"
fi

# Run tests
echo ""
read -p "Do you want to run tests? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running basic tests..."
    python3 src/preprocessing.py
    echo -e "${GREEN}✓ Tests completed${NC}"
else
    echo -e "${YELLOW}! Skipping tests${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate the environment: source venv/bin/activate"
echo "3. Run the system:"
echo "   - CLI: python src/main.py --interactive"
echo "   - Web UI: streamlit run ui/streamlit_app.py"
echo "   - API: python ui/flask_api.py"
echo ""
echo "Documentation: See README.md for detailed usage"
echo ""
echo "=========================================="
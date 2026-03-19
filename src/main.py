"""
Main Orchestrator for PD Screening System
Coordinates preprocessing, RAG, and LLM inference
"""
from llm.confidence_scorer import ConfidenceScorer
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()  # automatically looks for ".env" in current directory


import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

from preprocessing import TextPreprocessor
from rag.vector_store import VectorStore
from rag.retriever import ContextRetriever
from llm.inference import LLMInference
from llm.response_parser import ResponseParser


class PDScreeningSystem:
    """Complete PD screening system orchestrator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the complete screening system
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        logger.info("Initializing PD Screening System")
        
        self.preprocessor = TextPreprocessor(self.config)
        self.vector_store = VectorStore(self.config)
        self.retriever = ContextRetriever(self.vector_store, self.config)
        self.llm = LLMInference(self.config)
        self.parser = ResponseParser(self.config)
        self.confidence_scorer = ConfidenceScorer()
        logger.info("System initialization complete")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        if not os.path.exists(config_path):
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'llm': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.1,
                'max_tokens': 1000
            },
            'rag': {
                'vector_store': 'chromadb',
                'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
                'top_k': 3,
                'similarity_threshold': 0.7
            },
            'preprocessing': {
                'lowercase': True,
                'remove_punctuation': False,
                'remove_stopwords': False,
                'min_word_count': 5
            },
            'paths': {
                'chroma_persist': './data/chroma_db',
                'knowledge_base': './data/knowledge_base'
            },
            'logging': {
                'level': 'INFO'
            },
            'features': {
                'strict_json_validation': True
            }
        }
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        level = log_config.get('level', 'INFO')
        
        # Configure loguru
        logger.remove()  # Remove default handler
        logger.add(
            lambda msg: print(msg, end=""),
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
        )
        
        # Add file logging if specified
        log_file = log_config.get('file')
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            logger.add(log_file, rotation="10 MB", level=level)
    
    def screen_transcript(
        self, 
        transcript: str,
        include_details: bool = True
    ) -> Dict[str, Any]:
        """
        Complete screening pipeline for a transcript
        
        Args:
            transcript: User's text transcript
            include_details: Include detailed processing info
            
        Returns:
            Screening results dictionary
        """
        logger.info("=" * 60)
        logger.info("Starting screening pipeline")
        logger.info("=" * 60)
        
        results = {
            'success': False,
            'screening_response': {},
            'metadata': {}
        }
        
        try:
            # Step 1: Preprocess transcript
            # Step 1: Preprocess transcript
            logger.info("Step 1: Preprocessing transcript")
            preprocessed = self.preprocessor.preprocess(transcript)

            if not preprocessed['is_valid']:
                logger.warning("Transcript validation failed")
                results['screening_response'] = self.parser.create_fallback_response(
                    preprocessed['validation']['reason']
                 )
                results['metadata']['preprocessing'] = preprocessed
                return results

# ADD THIS SECTION HERE ↓↓↓
# Score transcript quality for confidence assessment
            quality_score = self.confidence_scorer.score_transcript_quality(
                preprocessed['cleaned_text'],
                preprocessed['features']
            )
            logger.info(f"Transcript quality score: {quality_score['total_score']:.2f}")
# ADD THIS SECTION HERE ↑↑↑

# Step 2: Retrieve relevant context
            logger.info("Step 2: Retrieving medical context")
            retrieval_result = self.retriever.retrieve_and_format(
                preprocessed['cleaned_text']
            )
            
            if include_details:
                results['metadata']['retrieval'] = {
                    'num_passages': retrieval_result['num_passages'],
                    'passages': retrieval_result['passages']
                }
            
            # Step 3: Generate LLM response
            logger.info("Step 3: Generating screening assessment")
            screening_response = self.llm.generate_with_fallback(
                transcript=preprocessed['cleaned_text'],
                context=retrieval_result['formatted_context'],
                linguistic_features=preprocessed['features']
            )
            
            results['screening_response'] = screening_response
            results['success'] = True
            
            # Add metadata
            if include_details:
                results['metadata']['preprocessing'] = {
                    'is_valid': preprocessed['is_valid'],
                    'features': preprocessed['features']
                }
                results['metadata']['llm'] = {
                    'provider': self.llm.provider,
                    'model': self.llm.model
                }
            
            logger.info("Screening pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Screening pipeline failed: {e}")
            results['screening_response'] = self.parser.create_fallback_response(str(e))
            results['error'] = str(e)
        
        return results
    
    def screen_and_display(self, transcript: str):
        """
        Screen transcript and display formatted results
        
        Args:
            transcript: User's transcript
        """
        results = self.screen_transcript(transcript)
        
        # Display formatted output
        formatted = self.parser.format_output(results['screening_response'])
        print("\n" + formatted)
        
        return results
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get system statistics
        
        Returns:
            Dictionary with system stats
        """
        return {
            'vector_store': self.vector_store.get_collection_stats(),
            'llm': {
                'provider': self.llm.provider,
                'model': self.llm.model
            },
            'config': {
                'preprocessing': self.config.get('preprocessing', {}),
                'rag': self.config.get('rag', {})
            }
        }


def main():
    """Main entry point for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PD Screening System - Text-based Parkinson's Disease Screening"
    )
    parser.add_argument(
        '--transcript',
        type=str,
        help='Transcript text to screen'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display system statistics'
    )
    
    args = parser.parse_args()
    
    # Initialize system
    system = PDScreeningSystem(config_path=args.config)
    
    # Display stats if requested
    if args.stats:
        stats = system.get_system_stats()
        print("\n=== SYSTEM STATISTICS ===")
        print(json.dumps(stats, indent=2))
        return
    
    # Interactive mode
    if args.interactive:
        print("\n" + "=" * 60)
        print("PD SCREENING SYSTEM - Interactive Mode")
        print("=" * 60)
        print("Enter transcript (or 'quit' to exit):\n")
        
        while True:
            try:
                transcript = input("> ")
                if transcript.lower() in ['quit', 'exit', 'q']:
                    break
                
                if transcript.strip():
                    system.screen_and_display(transcript)
                    print()
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    # Single transcript mode
    elif args.transcript:
        system.screen_and_display(args.transcript)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
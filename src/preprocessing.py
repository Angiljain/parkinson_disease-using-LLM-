"""
Text Preprocessing Module for PD Screening
Cleans, normalizes, and tokenizes user transcripts
"""

import re
import string
from typing import Dict, List, Optional
from unidecode import unidecode
import nltk
from loguru import logger

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


class TextPreprocessor:
    """Handles all text preprocessing for PD screening transcripts"""
    
    def __init__(self, config: Dict):
        """
        Initialize preprocessor with configuration
        
        Args:
            config: Dictionary with preprocessing settings
        """
        self.config = config.get('preprocessing', {})
        self.min_word_count = self.config.get('min_word_count', 5)
        self.language = self.config.get('language', 'en')
        
        # Load stopwords if needed
        self.stopwords = set(stopwords.words(self.language)) if self.config.get('remove_stopwords') else set()
        
        logger.info("TextPreprocessor initialized")
    
    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text string
        """
        if not text or not isinstance(text, str):
            logger.warning("Invalid input text received")
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        
        # Normalize unicode characters
        text = unidecode(text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text according to configuration
        
        Args:
            text: Cleaned text
            
        Returns:
            Normalized text
        """
        # Lowercase if configured
        if self.config.get('lowercase', True):
            text = text.lower()
        
        # Remove punctuation if configured
        if self.config.get('remove_punctuation', False):
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Normalized text
            
        Returns:
            List of tokens
        """
        tokens = word_tokenize(text)
        
        # Remove stopwords if configured
        if self.config.get('remove_stopwords', False):
            tokens = [t for t in tokens if t.lower() not in self.stopwords]
        
        return tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        return sent_tokenize(text)
    
    def validate_transcript(self, text: str) -> Dict[str, any]:
        """
        Validate if transcript meets minimum requirements
        
        Args:
            text: Input transcript
            
        Returns:
            Dictionary with validation results
        """
        tokens = self.tokenize(text)
        word_count = len([t for t in tokens if t.isalpha()])
        
        is_valid = word_count >= self.min_word_count
        
        return {
            'is_valid': is_valid,
            'word_count': word_count,
            'sentence_count': len(self.extract_sentences(text)),
            'char_count': len(text),
            'reason': None if is_valid else f"Insufficient words (min: {self.min_word_count})"
        }
    
    def extract_linguistic_features(self, text: str) -> Dict[str, any]:
        """
        Extract linguistic features relevant for PD screening
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary of linguistic features
        """
        sentences = self.extract_sentences(text)
        tokens = self.tokenize(text)
        words = [t for t in tokens if t.isalpha()]
        
        # Calculate metrics
        avg_sentence_length = sum(len(word_tokenize(s)) for s in sentences) / max(len(sentences), 1)
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        
        # Repetition analysis (simple)
        unique_words = len(set(w.lower() for w in words))
        lexical_diversity = unique_words / max(len(words), 1)
        
        return {
            'sentence_count': len(sentences),
            'word_count': len(words),
            'unique_words': unique_words,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_word_length': round(avg_word_length, 2),
            'lexical_diversity': round(lexical_diversity, 3),
            'total_characters': len(text)
        }
    
    def preprocess(self, text: str) -> Dict[str, any]:
        """
        Complete preprocessing pipeline
        
        Args:
            text: Raw input text
            
        Returns:
            Dictionary with processed text and metadata
        """
        logger.info("Starting text preprocessing")
        
        # Step 1: Clean
        cleaned_text = self.clean_text(text)
        
        # Step 2: Validate
        validation = self.validate_transcript(cleaned_text)
        
        if not validation['is_valid']:
            logger.warning(f"Transcript validation failed: {validation['reason']}")
            return {
                'original_text': text,
                'cleaned_text': cleaned_text,
                'normalized_text': '',
                'tokens': [],
                'validation': validation,
                'features': {},
                'is_valid': False
            }
        
        # Step 3: Normalize
        normalized_text = self.normalize_text(cleaned_text)
        
        # Step 4: Tokenize
        tokens = self.tokenize(normalized_text)
        
        # Step 5: Extract features
        features = self.extract_linguistic_features(cleaned_text)
        
        logger.info(f"Preprocessing complete: {features['word_count']} words, {features['sentence_count']} sentences")
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'normalized_text': normalized_text,
            'tokens': tokens,
            'validation': validation,
            'features': features,
            'is_valid': True
        }


def test_preprocessor():
    """Test function for preprocessing module"""
    config = {
        'preprocessing': {
            'lowercase': True,
            'remove_punctuation': False,
            'remove_stopwords': False,
            'min_word_count': 5,
            'language': 'en'
        }
    }
    
    preprocessor = TextPreprocessor(config)
    
    # Test case 1: Valid transcript
    text1 = "I have been experiencing some difficulty with my balance lately. My handwriting has become smaller too."
    result1 = preprocessor.preprocess(text1)
    print("Test 1 - Valid transcript:")
    print(f"  Valid: {result1['is_valid']}")
    print(f"  Features: {result1['features']}")
    
    # Test case 2: Too short
    text2 = "I feel fine."
    result2 = preprocessor.preprocess(text2)
    print("\nTest 2 - Short transcript:")
    print(f"  Valid: {result2['is_valid']}")
    print(f"  Reason: {result2['validation']['reason']}")


if __name__ == "__main__":
    test_preprocessor()
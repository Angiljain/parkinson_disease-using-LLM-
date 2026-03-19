"""
End-to-End Integration Tests
Tests complete screening pipeline from input to output
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import pytest
from main import PDScreeningSystem


class TestEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.fixture(scope="class")
    def system(self):
        """Initialize system once for all tests"""
        config = {
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
                'similarity_threshold': 0.5
            },
            'preprocessing': {
                'lowercase': True,
                'remove_punctuation': False,
                'remove_stopwords': False,
                'min_word_count': 5
            },
            'paths': {
                'chroma_persist': './test_data/chroma_db',
                'knowledge_base': './test_data/knowledge_base'
            },
            'logging': {'level': 'INFO'},
            'features': {'strict_json_validation': True}
        }
        
        # Write config temporarily
        import yaml
        config_path = './test_config.yaml'
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        system = PDScreeningSystem(config_path)
        
        # Build minimal knowledge base
        from rag.build_knowledge_base import KnowledgeBaseBuilder
        builder = KnowledgeBaseBuilder(system.config)
        builder.build_knowledge_base(use_sample_data=True, clear_existing=True)
        
        yield system
        
        # Cleanup
        import os
        if os.path.exists(config_path):
            os.remove(config_path)
    
    def test_valid_transcript_high_risk(self, system):
        """Test screening with high-risk transcript"""
        transcript = """
        I've been experiencing a resting tremor in my right hand for several months.
        My movements have become slower, and I notice my handwriting is much smaller.
        People tell me I don't show expressions on my face anymore, and my voice is softer.
        """
        
        results = system.screen_transcript(transcript)
        
        assert results['success'] is True
        assert 'screening_response' in results
        
        response = results['screening_response']
        assert 'risk_score' in response
        assert 'confidence' in response
        assert 'rationale' in response
        assert 'recommendation' in response
        
        # Should be higher risk given multiple symptoms
        assert response['risk_score'] >= 0.5
        assert response['confidence'] in ['low', 'medium', 'high']
        assert isinstance(response['rationale'], list)
        assert len(response['rationale']) > 0
    
    def test_valid_transcript_low_risk(self, system):
        """Test screening with low-risk transcript"""
        transcript = "I feel healthy and active. I exercise regularly and have no health concerns."
        
        results = system.screen_transcript(transcript)
        
        assert results['success'] is True
        response = results['screening_response']
        
        # Should be low risk
        assert response['risk_score'] <= 0.4
        assert response['recommendation'] in ['monitor', 'insufficient data']
    
    def test_short_transcript(self, system):
        """Test screening with insufficient transcript"""
        transcript = "I'm fine."
        
        results = system.screen_transcript(transcript)
        
        # Should handle gracefully
        assert 'screening_response' in results
        response = results['screening_response']
        
        # Should indicate insufficient data
        assert response['confidence'] == 'low'
        assert response['recommendation'] == 'insufficient data'
    
    def test_metadata_included(self, system):
        """Test that metadata is included when requested"""
        transcript = "My speech has become quieter and I have balance issues."
        
        results = system.screen_transcript(transcript, include_details=True)
        
        assert 'metadata' in results
        assert 'preprocessing' in results['metadata']
        assert 'retrieval' in results['metadata']
        assert 'llm' in results['metadata']
    
    def test_response_structure(self, system):
        """Test that response has correct structure"""
        transcript = "I notice trembling in my hand and slower movements."
        
        results = system.screen_transcript(transcript)
        response = results['screening_response']
        
        # Validate structure
        assert isinstance(response['risk_score'], (int, float))
        assert 0.0 <= response['risk_score'] <= 1.0
        assert response['confidence'] in ['low', 'medium', 'high']
        assert isinstance(response['rationale'], list)
        assert all(isinstance(r, str) for r in response['rationale'])
        assert response['recommendation'] in ['monitor', 'refer for evaluation', 'insufficient data']
    
    def test_system_stats(self, system):
        """Test system statistics retrieval"""
        stats = system.get_system_stats()
        
        assert 'vector_store' in stats
        assert 'llm' in stats
        assert 'config' in stats
        
        assert stats['vector_store']['document_count'] > 0
        assert stats['llm']['provider'] == 'openai'
    
    def test_multiple_screenings(self, system):
        """Test multiple consecutive screenings"""
        transcripts = [
            "I have a slight tremor in my right hand when resting.",
            "My balance has been good and I feel healthy.",
            "I notice my handwriting getting smaller over time."
        ]
        
        for transcript in transcripts:
            results = system.screen_transcript(transcript)
            assert results['success'] is True
            assert 'screening_response' in results
    
    def test_linguistic_features_extraction(self, system):
        """Test that linguistic features are extracted"""
        transcript = "This is a longer transcript with multiple sentences. It should extract various features."
        
        results = system.screen_transcript(transcript, include_details=True)
        
        features = results['metadata']['preprocessing']['features']
        assert 'word_count' in features
        assert 'sentence_count' in features
        assert 'lexical_diversity' in features
        assert features['word_count'] > 0
        assert features['sentence_count'] >= 1
    
    def test_rag_retrieval(self, system):
        """Test that RAG retrieval works"""
        transcript = "What are the speech symptoms of Parkinson's disease?"
        
        results = system.screen_transcript(transcript, include_details=True)
        
        retrieval = results['metadata']['retrieval']
        assert 'num_passages' in retrieval
        assert retrieval['num_passages'] > 0
        
        if 'passages' in retrieval:
            assert isinstance(retrieval['passages'], list)


def test_cli_interface():
    """Test command-line interface functionality"""
    # Test that main.py can be imported and run
    from main import main
    
    # This would normally be tested with subprocess or click.testing
    # For now, just verify the function exists
    assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
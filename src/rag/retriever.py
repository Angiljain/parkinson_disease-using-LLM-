"""
Context Retrieval Module for RAG Pipeline
Retrieves and formats relevant medical context for LLM
"""

from typing import List, Dict, Optional
from loguru import logger
from .vector_store import VectorStore


class ContextRetriever:
    """Retrieves relevant medical context for PD screening"""
    
    def __init__(self, vector_store: VectorStore, config: Dict):
        """
        Initialize retriever
        
        Args:
            vector_store: Initialized VectorStore instance
            config: Configuration dictionary
        """
        self.vector_store = vector_store
        self.config = config
        self.rag_config = config.get('rag', {})
        self.top_k = self.rag_config.get('top_k', 3)
        self.similarity_threshold = self.rag_config.get('similarity_threshold', 0.7)
        
        logger.info("ContextRetriever initialized")
    
    def retrieve(
        self, 
        query: str, 
        top_k: Optional[int] = None,
        include_metadata: bool = True
    ) -> List[Dict]:
        """
        Retrieve relevant context passages
        
        Args:
            query: Query text (preprocessed transcript)
            top_k: Number of passages to retrieve
            include_metadata: Whether to include metadata
            
        Returns:
            List of retrieved passages with metadata
        """
        if top_k is None:
            top_k = self.top_k
        
        logger.info(f"Retrieving top-{top_k} passages for query")
        
        # Search vector store
        results = self.vector_store.search(query, top_k=top_k)
        
        # Filter by similarity threshold
        filtered_results = [
            r for r in results 
            if (1 - r['distance']) >= self.similarity_threshold
        ]
        
        if len(filtered_results) < len(results):
            logger.info(
                f"Filtered {len(results) - len(filtered_results)} results "
                f"below similarity threshold {self.similarity_threshold}"
            )
        
        # Format results
        formatted = []
        for i, result in enumerate(filtered_results):
            passage = {
                'text': result['document'],
                'similarity': round(1 - result['distance'], 4),
                'rank': i + 1
            }
            
            if include_metadata:
                passage['metadata'] = result['metadata']
                passage['id'] = result['id']
            
            formatted.append(passage)
        
        logger.info(f"Retrieved {len(formatted)} relevant passages")
        return formatted
    
    def format_context_for_llm(self, passages: List[Dict]) -> str:
        """
        Format retrieved passages for LLM consumption
        
        Args:
            passages: List of retrieved passage dictionaries
            
        Returns:
            Formatted context string
        """
        if not passages:
            return "No relevant medical context found in knowledge base."
        
        formatted_parts = []
        
        for passage in passages:
            # Create passage header
            rank = passage['rank']
            similarity = passage['similarity']
            
            header = f"[Passage {rank} - Relevance: {similarity:.2%}]"
            text = passage['text']
            
            # Add metadata if available
            metadata = passage.get('metadata', {})
            if metadata:
                source = metadata.get('source', 'Unknown')
                category = metadata.get('category', 'General')
                header += f"\nSource: {source} | Category: {category}"
            
            formatted_parts.append(f"{header}\n{text}")
        
        # Join all passages
        context = "\n\n---\n\n".join(formatted_parts)
        
        return context
    
    def retrieve_and_format(
        self, 
        query: str, 
        top_k: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Complete retrieval pipeline: retrieve and format context
        
        Args:
            query: Query text
            top_k: Number of passages to retrieve
            
        Returns:
            Dictionary with passages and formatted context
        """
        # Retrieve passages
        passages = self.retrieve(query, top_k=top_k)
        
        # Format for LLM
        formatted_context = self.format_context_for_llm(passages)
        
        return {
            'passages': passages,
            'formatted_context': formatted_context,
            'num_passages': len(passages),
            'query': query
        }
    
    def get_retrieval_stats(self, passages: List[Dict]) -> Dict:
        """
        Calculate statistics about retrieved passages
        
        Args:
            passages: List of retrieved passages
            
        Returns:
            Statistics dictionary
        """
        if not passages:
            return {
                'num_passages': 0,
                'avg_similarity': 0.0,
                'min_similarity': 0.0,
                'max_similarity': 0.0
            }
        
        similarities = [p['similarity'] for p in passages]
        
        return {
            'num_passages': len(passages),
            'avg_similarity': round(sum(similarities) / len(similarities), 4),
            'min_similarity': round(min(similarities), 4),
            'max_similarity': round(max(similarities), 4),
            'total_chars': sum(len(p['text']) for p in passages)
        }


def test_retriever():
    """Test function for retriever"""
    from .vector_store import VectorStore
    
    config = {
        'rag': {
            'vector_store': 'chromadb',
            'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
            'top_k': 3,
            'similarity_threshold': 0.0
        },
        'paths': {
            'chroma_persist': './test_chroma_db'
        }
    }
    
    # Initialize components
    vector_store = VectorStore(config)
    
    # Add sample medical documents
    docs = [
        "Parkinson's disease affects dopamine-producing neurons in the substantia nigra. Motor symptoms include tremor, bradykinesia, rigidity, and postural instability.",
        "Speech difficulties in Parkinson's disease include hypophonia (reduced volume), monotone speech, imprecise articulation, and reduced prosody.",
        "Non-motor symptoms of PD include cognitive changes, depression, sleep disorders, and autonomic dysfunction.",
        "The MDS-UPDRS Part III evaluates motor symptoms including speech, facial expression, rigidity, finger tapping, and gait.",
        "Linguistic features in PD speech may show reduced lexical diversity, shorter utterances, and increased pauses."
    ]
    
    metadatas = [
        {"source": "NIH", "category": "pathophysiology"},
        {"source": "Speech Research", "category": "speech"},
        {"source": "Clinical Guide", "category": "symptoms"},
        {"source": "MDS-UPDRS", "category": "assessment"},
        {"source": "Research Paper", "category": "linguistic"}
    ]
    
    vector_store.clear()
    vector_store.add_documents(docs, metadatas)
    
    # Initialize retriever
    retriever = ContextRetriever(vector_store, config)
    
    # Test retrieval
    query = "My speech has been soft and monotone. I also have trouble with balance."
    result = retriever.retrieve_and_format(query, top_k=3)
    
    print("\n=== Retrieved Context ===")
    print(result['formatted_context'])
    
    print("\n=== Retrieval Statistics ===")
    stats = retriever.get_retrieval_stats(result['passages'])
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    test_retriever()
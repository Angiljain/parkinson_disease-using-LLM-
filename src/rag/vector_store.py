"""
Vector Store Management for RAG Pipeline
Supports ChromaDB and FAISS for efficient similarity search
"""

import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import chromadb
from chromadb.config import Settings
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer


class VectorStore:
    """Manages vector storage and retrieval for medical knowledge base"""
    
    def __init__(self, config: Dict):
        """
        Initialize vector store
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.rag_config = config.get('rag', {})
        self.store_type = self.rag_config.get('vector_store', 'chromadb')
        
        # Initialize embedding model
        embedding_model_name = self.rag_config.get(
            'embedding_model', 
            'sentence-transformers/all-MiniLM-L6-v2'
        )
        logger.info(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Initialize appropriate vector store
        if self.store_type == 'chromadb':
            self._init_chromadb()
        elif self.store_type == 'faiss':
            self._init_faiss()
        else:
            raise ValueError(f"Unsupported vector store: {self.store_type}")
        
        logger.info(f"VectorStore initialized with {self.store_type}")
    
    def _init_chromadb(self):
        """Initialize ChromaDB client and collection"""
        persist_dir = self.config['paths'].get('chroma_persist', './data/chroma_db')
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create or get collection
        try:
            self.collection = self.client.get_or_create_collection(
                name="parkinsons_knowledge",
                metadata={"description": "Medical knowledge for PD screening"}
            )
            logger.info(f"ChromaDB collection ready with {self.collection.count()} documents")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB collection: {e}")
            raise
    
    def _init_faiss(self):
        """Initialize FAISS index (placeholder for future implementation)"""
        logger.warning("FAISS support is experimental")
        self.faiss_index = None
        self.document_store = []
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as list
        """
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Add documents to vector store
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents
            
        Returns:
            Success status
        """
        try:
            if not documents:
                logger.warning("No documents to add")
                return False
            
            # Generate IDs if not provided
            if ids is None:
                existing_count = self.collection.count()
                ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(documents)} documents")
            embeddings = self.embed_texts(documents)
            
            # Prepare metadata
            if metadatas is None:
                metadatas = [{"source": "knowledge_base"} for _ in documents]
            
            # Add to ChromaDB
            if self.store_type == 'chromadb':
                self.collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully added {len(documents)} documents to ChromaDB")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def search(
        self, 
        query: str, 
        top_k: Optional[int] = None,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of search results with documents and scores
        """
        if top_k is None:
            top_k = self.rag_config.get('top_k', 3)
        
        try:
            if self.store_type == 'chromadb':
                # Generate query embedding
                query_embedding = self.embed_text(query)
                
                # Search in ChromaDB
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter_dict
                )
                
                # Format results
                formatted_results = []
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        formatted_results.append({
                            'document': doc,
                            'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                            'distance': results['distances'][0][i] if results['distances'] else 0,
                            'id': results['ids'][0][i] if results['ids'] else None
                        })
                
                logger.info(f"Retrieved {len(formatted_results)} documents for query")
                return formatted_results
            
            return []
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with collection statistics
        """
        if self.store_type == 'chromadb':
            count = self.collection.count()
            return {
                'store_type': self.store_type,
                'document_count': count,
                'embedding_model': self.rag_config.get('embedding_model'),
                'collection_name': self.collection.name
            }
        return {'store_type': self.store_type, 'document_count': 0}
    
    def clear(self) -> bool:
        """
        Clear all documents from vector store
        
        Returns:
            Success status
        """
        try:
            if self.store_type == 'chromadb':
                # Get all IDs and delete
                all_docs = self.collection.get()
                if all_docs['ids']:
                    self.collection.delete(ids=all_docs['ids'])
                logger.info("Vector store cleared")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear vector store: {e}")
            return False


def test_vector_store():
    """Test function for vector store"""
    config = {
        'rag': {
            'vector_store': 'chromadb',
            'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
            'top_k': 3
        },
        'paths': {
            'chroma_persist': './test_chroma_db'
        }
    }
    
    # Initialize
    store = VectorStore(config)
    
    # Clear existing data
    store.clear()
    
    # Add sample documents
    docs = [
        "Parkinson's disease is a progressive neurological disorder affecting movement.",
        "Common symptoms include tremor, rigidity, bradykinesia, and postural instability.",
        "Speech changes in PD may include reduced volume, monotone, and imprecise articulation."
    ]
    
    metadatas = [
        {"source": "definition", "category": "general"},
        {"source": "symptoms", "category": "clinical"},
        {"source": "speech", "category": "linguistic"}
    ]
    
    store.add_documents(docs, metadatas)
    
    # Test search
    query = "What are speech problems in Parkinson's?"
    results = store.search(query, top_k=2)
    
    print("\nSearch Results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['document'][:100]}...")
        print(f"   Distance: {result['distance']:.4f}")
        print(f"   Category: {result['metadata'].get('category', 'N/A')}")
    
    # Stats
    stats = store.get_collection_stats()
    print(f"\nCollection Stats: {stats}")


if __name__ == "__main__":
    test_vector_store()
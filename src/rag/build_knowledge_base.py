"""
Knowledge Base Builder
Builds medical knowledge base from documents and research papers
"""


from .enhanced_knowledge import get_enhanced_medical_knowledge
import os
from pathlib import Path
from typing import List, Dict, Optional
import yaml
from loguru import logger

from .vector_store import VectorStore


class KnowledgeBaseBuilder:
    """Builds and manages medical knowledge base for PD screening"""
    
    def __init__(self, config: Dict):
        """
        Initialize knowledge base builder
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.vector_store = VectorStore(config)
        self.kb_path = Path(config['paths'].get('knowledge_base', './data/knowledge_base'))
        
        logger.info("KnowledgeBaseBuilder initialized")
    
    def get_sample_medical_knowledge(self) -> List[Dict[str, str]]:
        """
        Get sample medical knowledge documents for PD screening
        
        Returns:
            List of document dictionaries with text and metadata
        """
        documents = [
            {
                'text': "Parkinson's disease (PD) is a progressive neurodegenerative disorder primarily affecting dopamine-producing neurons in the substantia nigra. The cardinal motor symptoms include resting tremor, bradykinesia (slowness of movement), rigidity, and postural instability. These symptoms typically manifest asymmetrically and progress gradually over time.",
                'metadata': {'source': 'NIH_Overview', 'category': 'pathophysiology', 'type': 'definition'}
            },
            {
                'text': "Speech and voice changes in Parkinson's disease include hypophonia (reduced vocal volume), monotone or monopitch speech, reduced prosody, imprecise articulation, breathy or hoarse voice quality, and rapid or variable speech rate. These changes are collectively known as hypokinetic dysarthria.",
                'metadata': {'source': 'Speech_Research', 'category': 'speech', 'type': 'symptoms'}
            },
            {
                'text': "The MDS-UPDRS (Movement Disorder Society-Unified Parkinson's Disease Rating Scale) Part III assesses motor examination including speech, facial expression, rigidity of neck and limbs, finger tapping, hand movements, pronation-supination movements, toe tapping, leg agility, arising from chair, gait, freezing of gait, and postural stability.",
                'metadata': {'source': 'MDS-UPDRS', 'category': 'assessment', 'type': 'clinical_tool'}
            },
            {
                'text': "Linguistic features that may indicate PD include reduced lexical diversity, shorter utterance length, increased pause frequency and duration, simplified syntactic structures, word-finding difficulties, and repetition of words or phrases. These changes reflect both motor and cognitive aspects of the disease.",
                'metadata': {'source': 'Linguistic_Research', 'category': 'linguistic', 'type': 'research'}
            },
            {
                'text': "Early signs of Parkinson's disease may include subtle changes in handwriting (micrographia), loss of smell (anosmia), sleep disturbances including REM sleep behavior disorder, constipation, soft or low voice, masked facies (reduced facial expression), and stooped posture.",
                'metadata': {'source': 'PD_Foundation', 'category': 'early_signs', 'type': 'symptoms'}
            },
            {
                'text': "Non-motor symptoms of PD are common and include cognitive changes (executive dysfunction, memory problems), mood disorders (depression, anxiety, apathy), sleep disorders (insomnia, REM sleep behavior disorder, excessive daytime sleepiness), autonomic dysfunction (orthostatic hypotension, urinary problems, constipation), and sensory symptoms (pain, paresthesias).",
                'metadata': {'source': 'NIH_Symptoms', 'category': 'non-motor', 'type': 'symptoms'}
            },
            {
                'text': "Resting tremor in PD typically presents as a pill-rolling movement of the thumb and fingers at 4-6 Hz. The tremor is most prominent at rest, decreases with voluntary movement, and may be exacerbated by stress or fatigue. It usually begins unilaterally and may spread to the contralateral side.",
                'metadata': {'source': 'Clinical_Guide', 'category': 'tremor', 'type': 'symptoms'}
            },
            {
                'text': "Bradykinesia manifests as slowness of movement, reduced amplitude of movements, difficulty initiating movements, and progressive decrease in speed and amplitude with repetitive movements (sequence effect). It affects activities of daily living including walking, turning in bed, buttoning clothes, and cutting food.",
                'metadata': {'source': 'Clinical_Guide', 'category': 'bradykinesia', 'type': 'symptoms'}
            },
            {
                'text': "Postural instability in PD results from impaired postural reflexes. Patients may have difficulty maintaining balance, particularly when turning or changing position. The pull test (posterior displacement) can assess postural stability, though this typically occurs in later stages of the disease.",
                'metadata': {'source': 'Clinical_Examination', 'category': 'balance', 'type': 'assessment'}
            },
            {
                'text': "Rigidity in PD is characterized by increased muscle tone throughout the range of passive movement, often with cogwheeling (ratchet-like resistance). It can affect both flexor and extensor muscles and contributes to stooped posture, reduced arm swing while walking, and complaints of stiffness or aching.",
                'metadata': {'source': 'Motor_Symptoms', 'category': 'rigidity', 'type': 'symptoms'}
            },
            {
                'text': "Freezing of gait (FOG) is a common symptom in PD characterized by brief episodes where patients feel their feet are glued to the floor. It most commonly occurs when initiating gait, turning, approaching doorways or obstacles, or in crowded spaces. FOG increases fall risk and impacts quality of life.",
                'metadata': {'source': 'Gait_Disorders', 'category': 'gait', 'type': 'symptoms'}
            },
            {
                'text': "Cognitive impairment in PD ranges from mild cognitive impairment (PD-MCI) to Parkinson's disease dementia (PDD). Executive dysfunction is often the earliest cognitive change, affecting planning, organization, and problem-solving. Visual-spatial difficulties, attention deficits, and memory problems may also occur.",
                'metadata': {'source': 'Cognitive_Research', 'category': 'cognition', 'type': 'symptoms'}
            },
            {
                'text': "Masked facies or hypomimia refers to reduced facial expressiveness in PD. This results from rigidity and bradykinesia affecting facial muscles, leading to decreased spontaneous facial movements, reduced blinking, and a fixed stare. Family members often report that the patient looks sad or disinterested.",
                'metadata': {'source': 'Facial_Expression', 'category': 'facies', 'type': 'symptoms'}
            },
            {
                'text': "Micrographia, or small handwriting, is a common early sign of PD. Writing becomes progressively smaller as the task continues, with letters becoming illegible. This reflects bradykinesia and is often one of the first symptoms patients or family members notice.",
                'metadata': {'source': 'Writing_Changes', 'category': 'micrographia', 'type': 'symptoms'}
            },
            {
                'text': "Screening for PD should lead to referral to a movement disorder specialist or neurologist for comprehensive evaluation. Diagnosis is clinical, based on history and examination. Dopamine transporter (DaT) scans may support diagnosis in unclear cases. Early diagnosis allows for timely treatment initiation and care planning.",
                'metadata': {'source': 'Clinical_Guidelines', 'category': 'diagnosis', 'type': 'clinical_practice'}
            }
        ]
        
        return documents
    
    def chunk_document(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """
        Split document into overlapping chunks
        
        Args:
            text: Document text
            chunk_size: Maximum chunk size in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for period followed by space
                last_period = text[start:end].rfind('. ')
                if last_period > chunk_size // 2:  # Don't create too small chunks
                    end = start + last_period + 1
            
            chunks.append(text[start:end].strip())
            start = end - overlap
        
        return chunks
    
    def load_documents_from_directory(self, directory: Path) -> List[Dict]:
        """
        Load documents from directory
        
        Args:
            directory: Path to documents directory
            
        Returns:
            List of document dictionaries
        """
        documents = []
        
        if not directory.exists():
            logger.warning(f"Directory {directory} does not exist")
            return documents
        
        for file_path in directory.glob('**/*.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                documents.append({
                    'text': text,
                    'metadata': {
                        'source': file_path.stem,
                        'file_path': str(file_path),
                        'type': 'document'
                    }
                })
                
                logger.info(f"Loaded document: {file_path.name}")
                
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
        
        return documents
    
    def build_knowledge_base(
        self,
        use_sample_data: bool = True,
        load_from_directory: bool = False,
        clear_existing: bool = False
    ) -> Dict[str, any]:
        """
        Build complete knowledge base
        
        Args:
            use_sample_data: Use built-in sample medical knowledge
            load_from_directory: Load documents from knowledge_base directory
            clear_existing: Clear existing data before building
            
        Returns:
            Build statistics
        """
        logger.info("Building knowledge base")
        
        if clear_existing:
            logger.info("Clearing existing knowledge base")
            self.vector_store.clear()
        
        all_documents = []
        
        # Add sample data
       # Add sample data
        if use_sample_data:
            logger.info("Adding sample medical knowledge")
            sample_docs = self.get_sample_medical_knowledge()
            all_documents.extend(sample_docs)
    
    # Add enhanced knowledge
        try:
            
            enhanced_docs = get_enhanced_medical_knowledge()
            all_documents.extend(enhanced_docs)
            logger.info(f"Added {len(enhanced_docs)} enhanced medical documents")
        except ImportError:
               logger.warning("Enhanced knowledge module not found, using basic knowledge only")
        
        # Load from directory
        if load_from_directory:
            logger.info(f"Loading documents from {self.kb_path}")
            dir_docs = self.load_documents_from_directory(self.kb_path)
            all_documents.extend(dir_docs)
        
        if not all_documents:
            logger.warning("No documents to add to knowledge base")
            return {'success': False, 'num_documents': 0}
        
        # Process and add documents
        logger.info(f"Processing {len(all_documents)} documents")
        
        texts = [doc['text'] for doc in all_documents]
        metadatas = [doc['metadata'] for doc in all_documents]
        
        success = self.vector_store.add_documents(texts, metadatas)
        
        stats = self.vector_store.get_collection_stats()
        
        logger.info(f"Knowledge base built: {stats['document_count']} documents")
        
        return {
            'success': success,
            'num_documents': len(all_documents),
            'stats': stats
        }


def main():
    """Build knowledge base from command line"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build PD Screening Knowledge Base")
    parser.add_argument('--config', default='../../config.yaml', help='Config file path')
    parser.add_argument('--clear', action='store_true', help='Clear existing data')
    parser.add_argument('--no-sample', action='store_true', help='Skip sample data')
    parser.add_argument('--load-dir', action='store_true', help='Load from directory')
    
    args = parser.parse_args()
    
    # Load config
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'rag': {
                'vector_store': 'chromadb',
                'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2'
            },
            'paths': {
                'chroma_persist': './data/chroma_db',
                'knowledge_base': './data/knowledge_base'
            }
        }
    
    # Build knowledge base
    builder = KnowledgeBaseBuilder(config)
    result = builder.build_knowledge_base(
        use_sample_data=not args.no_sample,
        load_from_directory=args.load_dir,
        clear_existing=args.clear
    )
    
    print("\n=== Knowledge Base Build Results ===")
    print(f"Success: {result['success']}")
    print(f"Documents processed: {result['num_documents']}")
    if 'stats' in result:
        print(f"Total documents in store: {result['stats']['document_count']}")


if __name__ == "__main__":
    main()
"""
Confidence Scoring Module
Analyzes transcript quality and adjusts confidence levels
"""

from typing import Dict, List
import re

class ConfidenceScorer:
    """Scores transcript quality for confidence assessment"""
    
    # High-value medical terms
    CARDINAL_TERMS = [
        'tremor', 'rigidity', 'bradykinesia', 'stiffness', 'slow movement',
        'postural instability', 'balance', 'falls'
    ]
    
    SPEECH_TERMS = [
        'voice', 'speech', 'quiet', 'soft', 'loud', 'monotone', 'mumble',
        'articulation', 'slurred', 'hypophonia'
    ]
    
    WRITING_TERMS = [
        'handwriting', 'writing', 'small', 'micrographia', 'signature',
        'illegible', 'cramped'
    ]
    
    TIMELINE_INDICATORS = [
        'month', 'year', 'week', 'ago', 'started', 'began', 'since',
        'progressive', 'worsening', 'getting worse', 'gradual'
    ]
    
    SPECIFIC_INDICATORS = [
        'right hand', 'left hand', 'right arm', 'left arm', 'one side',
        'pill-rolling', 'resting', 'at rest', 'when sitting'
    ]
    
    FAMILY_INDICATORS = [
        'wife', 'husband', 'family', 'spouse', 'children', 'friends',
        'people say', 'others notice', 'told me', 'asked me'
    ]
    
    def __init__(self):
        pass
    
    def score_transcript_quality(self, transcript: str, features: Dict) -> Dict:
        """
        Score transcript quality for confidence assessment
        
        Args:
            transcript: The input transcript
            features: Linguistic features dict
            
        Returns:
            Quality score dict with components
        """
        text_lower = transcript.lower()
        
        # Component scores (0-1)
        length_score = self._score_length(features.get('word_count', 0))
        specificity_score = self._score_specificity(text_lower)
        timeline_score = self._score_timeline(text_lower)
        medical_terminology_score = self._score_medical_terms(text_lower)
        family_observation_score = self._score_family_observations(text_lower)
        detail_score = self._score_detail_level(transcript, features)
        
        # Weighted average
        weights = {
            'length': 0.15,
            'specificity': 0.25,
            'timeline': 0.15,
            'medical_terms': 0.20,
            'family_observations': 0.10,
            'detail_level': 0.15
        }
        
        total_score = (
            length_score * weights['length'] +
            specificity_score * weights['specificity'] +
            timeline_score * weights['timeline'] +
            medical_terminology_score * weights['medical_terms'] +
            family_observation_score * weights['family_observations'] +
            detail_score * weights['detail_level']
        )
        
        return {
            'total_score': round(total_score, 3),
            'components': {
                'length': round(length_score, 3),
                'specificity': round(specificity_score, 3),
                'timeline': round(timeline_score, 3),
                'medical_terminology': round(medical_terminology_score, 3),
                'family_observations': round(family_observation_score, 3),
                'detail_level': round(detail_score, 3)
            },
            'suggested_confidence': self._map_to_confidence(total_score)
        }
    
    def _score_length(self, word_count: int) -> float:
        """Score based on word count"""
        if word_count < 10:
            return 0.2
        elif word_count < 20:
            return 0.5
        elif word_count < 40:
            return 0.7
        elif word_count < 60:
            return 0.9
        else:
            return 1.0
    
    def _score_specificity(self, text: str) -> float:
        """Score based on specific details mentioned"""
        score = 0.0
        
        # Check for specific body parts
        if any(term in text for term in self.SPECIFIC_INDICATORS):
            score += 0.4
        
        # Check for cardinal symptoms
        cardinal_count = sum(1 for term in self.CARDINAL_TERMS if term in text)
        score += min(cardinal_count * 0.15, 0.4)
        
        # Check for multiple domains
        domains = 0
        if any(term in text for term in self.SPEECH_TERMS):
            domains += 1
        if any(term in text for term in self.WRITING_TERMS):
            domains += 1
        if 'tremor' in text:
            domains += 1
        
        score += min(domains * 0.1, 0.2)
        
        return min(score, 1.0)
    
    def _score_timeline(self, text: str) -> float:
        """Score based on timeline information"""
        timeline_count = sum(1 for term in self.TIMELINE_INDICATORS if term in text)
        
        if timeline_count == 0:
            return 0.3
        elif timeline_count == 1:
            return 0.6
        else:
            return 1.0
    
    def _score_medical_terms(self, text: str) -> float:
        """Score based on medical terminology usage"""
        all_medical_terms = (
            self.CARDINAL_TERMS + 
            self.SPEECH_TERMS + 
            self.WRITING_TERMS
        )
        
        term_count = sum(1 for term in all_medical_terms if term in text)
        
        if term_count == 0:
            return 0.2
        elif term_count <= 2:
            return 0.5
        elif term_count <= 4:
            return 0.8
        else:
            return 1.0
    
    def _score_family_observations(self, text: str) -> float:
        """Score based on family member observations"""
        if any(indicator in text for indicator in self.FAMILY_INDICATORS):
            return 1.0
        return 0.5
    
    def _score_detail_level(self, transcript: str, features: Dict) -> float:
        """Score based on overall detail level"""
        # Check sentence count
        sentence_count = features.get('sentence_count', 1)
        
        # Check for examples
        example_indicators = ['like', 'such as', 'example', 'for instance', 'including']
        has_examples = any(ind in transcript.lower() for ind in example_indicators)
        
        # Check for comparisons (before/after)
        comparison_indicators = ['than before', 'used to', 'previously', 'now', 'currently', 'was', 'has become']
        has_comparisons = any(ind in transcript.lower() for ind in comparison_indicators)
        
        score = 0.3  # Base score
        
        if sentence_count >= 2:
            score += 0.2
        if sentence_count >= 3:
            score += 0.2
        
        if has_examples:
            score += 0.15
        
        if has_comparisons:
            score += 0.15
        
        return min(score, 1.0)
    
    def _map_to_confidence(self, score: float) -> str:
        """Map quality score to confidence level"""
        if score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"


# Test function
if __name__ == "__main__":
    scorer = ConfidenceScorer()
    
    # Test case 1: High quality
    test1 = "Over the past year, my right hand has developed a resting tremor with a pill-rolling quality. My wife has noticed that my voice has become much quieter, and my handwriting has gotten progressively smaller."
    features1 = {'word_count': 38, 'sentence_count': 2}
    result1 = scorer.score_transcript_quality(test1, features1)
    print("Test 1 (High Quality):")
    print(f"  Total Score: {result1['total_score']}")
    print(f"  Suggested Confidence: {result1['suggested_confidence']}")
    print(f"  Components: {result1['components']}")
    
    # Test case 2: Low quality
    test2 = "I don't feel good."
    features2 = {'word_count': 4, 'sentence_count': 1}
    result2 = scorer.score_transcript_quality(test2, features2)
    print("\nTest 2 (Low Quality):")
    print(f"  Total Score: {result2['total_score']}")
    print(f"  Suggested Confidence: {result2['suggested_confidence']}")
    print(f"  Components: {result2['components']}")
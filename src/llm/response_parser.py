"""
Response Parser and Validator
Parses and validates JSON responses from LLM
"""

import json
import re
from typing import Dict, Any, List, Tuple
from loguru import logger


class ResponseParser:
    """Parses and validates LLM screening responses"""
    
    REQUIRED_FIELDS = ['risk_score', 'confidence', 'rationale', 'recommendation']
    VALID_CONFIDENCE = ['low', 'medium', 'high']
    VALID_RECOMMENDATION = ['monitor', 'refer for evaluation', 'insufficient data']
    
    def __init__(self, config: Dict):
        """
        Initialize parser
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.strict_validation = config.get('features', {}).get('strict_json_validation', True)
        logger.info("ResponseParser initialized")
    
    def extract_json_from_text(self, text: str) -> str:
        """
        Extract JSON from text that may contain additional content
        
        Args:
            text: Raw LLM response
            
        Returns:
            Extracted JSON string
        """
        # Try to find JSON object in text
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            # Return the most complete JSON match
            return max(matches, key=len)
        
        # If no match, return original text
        return text.strip()
    
    def parse_json(self, response_text: str) -> Tuple[Dict, List[str]]:
        """
        Parse JSON from response text
        
        Args:
            response_text: Raw response text
            
        Returns:
            Tuple of (parsed_dict, errors_list)
        """
        errors = []
        
        try:
            # Extract JSON if embedded in text
            json_text = self.extract_json_from_text(response_text)
            
            # Parse JSON
            parsed = json.loads(json_text)
            
            return parsed, errors
            
        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error: {str(e)}")
            logger.error(f"Failed to parse JSON: {e}")
            return {}, errors
    
    def validate_structure(self, response: Dict) -> List[str]:
        """
        Validate response structure and fields
        
        Args:
            response: Parsed response dictionary
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in response:
                errors.append(f"Missing required field: {field}")
        
        # Validate risk_score
        if 'risk_score' in response:
            risk = response['risk_score']
            if not isinstance(risk, (int, float)):
                errors.append(f"risk_score must be numeric, got {type(risk)}")
            elif not (0.0 <= risk <= 1.0):
                errors.append(f"risk_score must be between 0.0 and 1.0, got {risk}")
        
        # Validate confidence
        if 'confidence' in response:
            conf = response['confidence']
            if not isinstance(conf, str):
                errors.append(f"confidence must be string, got {type(conf)}")
            elif conf not in self.VALID_CONFIDENCE:
                errors.append(f"confidence must be one of {self.VALID_CONFIDENCE}, got '{conf}'")
        
        # Validate rationale
        if 'rationale' in response:
            rationale = response['rationale']
            if not isinstance(rationale, list):
                errors.append(f"rationale must be list, got {type(rationale)}")
            elif len(rationale) == 0:
                errors.append("rationale list cannot be empty")
            elif not all(isinstance(item, str) for item in rationale):
                errors.append("All rationale items must be strings")
        
        # Validate recommendation
        if 'recommendation' in response:
            rec = response['recommendation']
            if not isinstance(rec, str):
                errors.append(f"recommendation must be string, got {type(rec)}")
            elif rec not in self.VALID_RECOMMENDATION:
                errors.append(f"recommendation must be one of {self.VALID_RECOMMENDATION}, got '{rec}'")
        
        return errors
    
    def validate_consistency(self, response: Dict) -> List[str]:
        """
        Validate internal consistency of response
        
        Args:
            response: Parsed response dictionary
            
        Returns:
            List of consistency warnings
        """
        warnings = []
        
        if 'risk_score' not in response or 'recommendation' not in response:
            return warnings
        
        risk = response['risk_score']
        rec = response['recommendation']
        
        # Check if recommendation matches risk level
        if risk >= 0.7 and rec not in ['refer for evaluation']:
            warnings.append(f"High risk score ({risk}) but recommendation is '{rec}'")
        
        if risk <= 0.3 and rec == 'refer for evaluation':
            warnings.append(f"Low risk score ({risk}) but recommendation is 'refer for evaluation'")
        
        if rec == 'insufficient data' and risk > 0.5:
            warnings.append(f"Insufficient data recommendation but risk score is {risk}")
        
        return warnings
    
    def parse_and_validate(self, response_text: str) -> Dict[str, Any]:
        """
        Complete parsing and validation pipeline
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Dictionary with validation results
        """
        logger.info("Parsing and validating LLM response")
        
        # Parse JSON
        parsed, parse_errors = self.parse_json(response_text)
        
        if parse_errors:
            return {
                'is_valid': False,
                'response': {},
                'errors': parse_errors,
                'warnings': [],
                'raw_text': response_text
            }
        
        # Validate structure
        structure_errors = self.validate_structure(parsed)
        
        # Check consistency
        consistency_warnings = self.validate_consistency(parsed)
        
        # Determine if valid
        is_valid = len(structure_errors) == 0
        
        if not is_valid:
            logger.warning(f"Response validation failed: {structure_errors}")
        elif consistency_warnings:
            logger.info(f"Response valid with warnings: {consistency_warnings}")
        else:
            logger.info("Response validation successful")
        
        return {
            'is_valid': is_valid,
            'response': parsed,
            'errors': structure_errors,
            'warnings': consistency_warnings,
            'raw_text': response_text
        }
    
    def create_fallback_response(self, error_message: str) -> Dict[str, Any]:
        """
        Create fallback response when LLM fails
        
        Args:
            error_message: Error description
            
        Returns:
            Safe fallback screening response
        """
        logger.warning(f"Creating fallback response due to: {error_message}")
        
        return {
            'risk_score': 0.0,
            'confidence': 'low',
            'rationale': [
                'Unable to complete screening due to technical error',
                f'Error: {error_message}',
                'Please try again or consult a healthcare professional directly'
            ],
            'recommendation': 'insufficient data',
            'error': error_message,
            'is_fallback': True
        }
    
    def format_output(self, response: Dict) -> str:
        """
        Format response for human-readable output
        
        Args:
            response: Validated response dictionary
            
        Returns:
            Formatted string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("PARKINSON'S DISEASE SCREENING RESULTS")
        lines.append("=" * 60)
        
        # Risk score
        risk = response.get('risk_score', 0.0)
        risk_level = 'LOW' if risk < 0.4 else ('MODERATE' if risk < 0.7 else 'HIGHER')
        lines.append(f"\nRisk Score: {risk:.2f} ({risk_level})")
        
        # Confidence
        confidence = response.get('confidence', 'low').upper()
        lines.append(f"Confidence: {confidence}")
        
        # Rationale
        lines.append("\nRationale:")
        for i, point in enumerate(response.get('rationale', []), 1):
            lines.append(f"  {i}. {point}")
        
        # Recommendation
        rec = response.get('recommendation', 'insufficient data')
        lines.append(f"\nRecommendation: {rec.upper()}")
        
        # Disclaimer
        lines.append("\n" + "-" * 60)
        lines.append("IMPORTANT DISCLAIMER:")
        lines.append("This is a screening tool only, NOT a medical diagnosis.")
        lines.append("Please consult a healthcare professional for proper evaluation.")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def test_parser():
    """Test response parser"""
    config = {
        'features': {
            'strict_json_validation': True
        }
    }
    
    parser = ResponseParser(config)
    
    # Test case 1: Valid response
    valid_response = '''
    {
      "risk_score": 0.65,
      "confidence": "medium",
      "rationale": [
        "Hypophonia mentioned indicating speech difficulties",
        "Self-reported progressive changes",
        "Multiple symptoms align with PD indicators"
      ],
      "recommendation": "refer for evaluation"
    }
    '''
    
    result1 = parser.parse_and_validate(valid_response)
    print("Test 1 - Valid Response:")
    print(f"  Valid: {result1['is_valid']}")
    print(f"  Errors: {result1['errors']}")
    print(f"  Warnings: {result1['warnings']}")
    
    # Test case 2: Invalid response
    invalid_response = '''
    {
      "risk_score": 1.5,
      "confidence": "very_high",
      "recommendation": "see doctor"
    }
    '''
    
    result2 = parser.parse_and_validate(invalid_response)
    print("\nTest 2 - Invalid Response:")
    print(f"  Valid: {result2['is_valid']}")
    print(f"  Errors: {result2['errors']}")
    
    # Test case 3: Format output
    print("\n" + parser.format_output(result1['response']))
    
    # Test case 4: Fallback
    fallback = parser.create_fallback_response("API timeout")
    print("\nTest 4 - Fallback Response:")
    print(json.dumps(fallback, indent=2))


if __name__ == "__main__":
    import json
    test_parser()
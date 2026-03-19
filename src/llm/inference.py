"""
LLM Inference Module
Handles inference with multiple LLM providers (OpenAI, Anthropic, Mistral, Groq, etc.)
"""

import os
import json
from typing import Dict, Optional, Any
from loguru import logger
import openai
from anthropic import Anthropic
from groq import Groq  # ADD THIS LINE
from dotenv import load_dotenv  # ✅ ADD THIS
load_dotenv()  # ✅ AND THIS
from .prompts import PromptTemplate




class LLMInference:
    """Manages LLM inference for PD screening"""
    
    def __init__(self, config: Dict):
        """
        Initialize LLM inference
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.llm_config = config.get('llm', {})
        
        self.provider = self.llm_config.get('provider', 'openai')
        self.model = self.llm_config.get('model', 'gpt-4o')
        self.temperature = self.llm_config.get('temperature', 0.1)
        self.max_tokens = self.llm_config.get('max_tokens', 1000)
        self.timeout = self.llm_config.get('timeout', 30)
        
        # Initialize API clients
        self._init_clients()
        
        # Initialize prompt template
        self.prompt_template = PromptTemplate()
        
        logger.info(f"LLMInference initialized with {self.provider}/{self.model}")
    
    def _init_clients(self):
        """Initialize API clients based on provider"""
        if self.provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.warning("OPENAI_API_KEY not found in environment")
            self.openai_client = openai.OpenAI(api_key=api_key)
        
        elif self.provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY not found in environment")
            self.anthropic_client = Anthropic(api_key=api_key)
        
        elif self.provider == 'groq':
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                logger.warning("GROQ_API_KEY not found in environment")
                raise ValueError("GROQ_API_KEY is required for Groq provider")
            self.groq_client = Groq(api_key=api_key)
            logger.info("Groq client initialized successfully")
        
        elif self.provider == 'mistral':
            api_key = os.getenv('MISTRAL_API_KEY')
            if not api_key:
                logger.warning("MISTRAL_API_KEY not found in environment")
            self.mistral_client = None
        
        else:
            logger.warning(f"Unknown provider: {self.provider}")
    
    def _call_groq(self, messages: list, response_format: Optional[Dict] = None) -> str:
        """
        Call Groq API
        
        Args:
            messages: List of message dictionaries
            response_format: Optional response format (Groq supports JSON mode)
            
        Returns:
            LLM response text
        """
        try:
            kwargs = {
                'model': self.model,
                'messages': messages,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
            }
            
            # Groq supports JSON mode
            if response_format and response_format.get('type') == 'json_object':
                kwargs['response_format'] = {"type": "json_object"}
            
            response = self.groq_client.chat.completions.create(**kwargs)
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    def _call_openai(
        self, 
        messages: list,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Call OpenAI API
        
        Args:
            messages: List of message dictionaries
            response_format: Optional response format specification
            
        Returns:
            LLM response text
        """
        try:
            kwargs = {
                'model': self.model,
                'messages': messages,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'timeout': self.timeout
            }
            
            # Add response format for JSON mode (GPT-4 and later)
            if response_format:
                kwargs['response_format'] = response_format
            
            response = self.openai_client.chat.completions.create(**kwargs)
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _call_anthropic(self, system: str, user: str) -> str:
        """
        Call Anthropic Claude API
        
        Args:
            system: System prompt
            user: User prompt
            
        Returns:
            LLM response text
        """
        try:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system,
                messages=[{"role": "user", "content": user}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def _call_mistral(self, messages: list) -> str:
        """
        Call Mistral AI API (placeholder)
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            LLM response text
        """
        logger.warning("Mistral API not fully implemented")
        raise NotImplementedError("Mistral provider not yet implemented")
    
    def generate_screening_response(
        self,
        transcript: str,
        context: str,
        linguistic_features: Optional[Dict] = None
    ) -> str:
        """
        Generate screening response from LLM
        
        Args:
            transcript: User's transcript
            context: Retrieved medical context
            linguistic_features: Optional linguistic features
            
        Returns:
            Raw LLM response (should be JSON)
        """
        logger.info(f"Generating screening response using {self.provider}")
        
        try:
            if self.provider == 'openai':
                messages = self.prompt_template.create_chat_messages(
                    transcript, context, linguistic_features
                )
                
                response_format = None
                if 'gpt-4' in self.model.lower() or 'gpt-3.5' in self.model.lower():
                    response_format = {"type": "json_object"}
                
                response = self._call_openai(messages, response_format)
            
            elif self.provider == 'groq':
                messages = self.prompt_template.create_chat_messages(
                    transcript, context, linguistic_features
                )
                
                # Groq supports JSON mode
                response_format = {"type": "json_object"}
                response = self._call_groq(messages, response_format)
                
            elif self.provider == 'anthropic':
                system = self.prompt_template.SYSTEM_PROMPT
                user = self.prompt_template.create_user_prompt(
                    transcript, context, linguistic_features
                )
                response = self._call_anthropic(system, user)
            
            elif self.provider == 'mistral':
                messages = self.prompt_template.create_chat_messages(
                    transcript, context, linguistic_features
                )
                response = self._call_mistral(messages)
            
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            logger.info("Successfully generated LLM response")
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise
    
    def generate_with_fallback(
        self,
        transcript: str,
        context: str,
        linguistic_features: Optional[Dict] = None,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Generate response with retry logic and fallback
        
        Args:
            transcript: User's transcript
            context: Retrieved medical context
            linguistic_features: Optional linguistic features
            max_retries: Maximum number of retries
            
        Returns:
            Parsed screening response dictionary
        """
        from .response_parser import ResponseParser
        
        parser = ResponseParser(self.config)
        
        for attempt in range(max_retries + 1):
            try:
                # Generate response
                raw_response = self.generate_screening_response(
                    transcript, context, linguistic_features
                )
                
                # Parse and validate
                parsed = parser.parse_and_validate(raw_response)
                
                if parsed['is_valid']:
                    logger.info(f"Valid response generated on attempt {attempt + 1}")
                    return parsed['response']
                else:
                    logger.warning(f"Invalid response on attempt {attempt + 1}: {parsed['errors']}")
                    if attempt < max_retries:
                        continue
                    else:
                        # Return fallback on final attempt
                        return parser.create_fallback_response(
                            "Failed to generate valid response after retries"
                        )
                        
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries:
                    continue
                else:
                    return parser.create_fallback_response(str(e))
        
        # Should not reach here
        return parser.create_fallback_response("Unknown error")


def test_inference():
    """Test LLM inference"""
    config = {
        'llm': {
            'provider': 'groq',
            'model': 'llama-3.1-8b-instant',
            'temperature': 0.1,
            'max_tokens': 1000,
            'timeout': 30
        }
    }
    
    inference = LLMInference(config)
    
    # Test case
    transcript = "My speech has become quieter and people ask me to repeat myself. I also notice my hands shake when resting."
    context = """[Passage 1]
Speech difficulties in Parkinson's disease include hypophonia (reduced volume) and monotone speech.
[Passage 2]
Resting tremor is a cardinal motor symptom of Parkinson's disease."""
    
    features = {
        "word_count": 20,
        "sentence_count": 2,
        "avg_word_length": 5.1
    }
    
    print("Generating screening response...")
    try:
        response = inference.generate_with_fallback(transcript, context, features)
        print("\n=== Screening Response ===")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_inference()
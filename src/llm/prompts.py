"""
Prompt Templates for PD Screening LLM
Defines system and user prompts for structured screening
"""

from typing import Dict, Optional


class PromptTemplate:
    """Manages prompt templates for PD screening"""
    
    SYSTEM_PROMPT = """You are a specialized Parkinson's Disease screening assistant with expertise in movement disorders and linguistic analysis. You do NOT diagnose.

Your role is to analyze text transcripts for potential PD risk indicators using evidence-based medical knowledge.

SCREENING FRAMEWORK - Consider these PD indicators:

MOTOR SYMPTOMS (Cardinal Features):
1. Resting Tremor - typically 4-6 Hz, pill-rolling, asymmetric onset
2. Bradykinesia - slowness of movement, reduced amplitude
3. Rigidity - cogwheel or lead-pipe, affects flexors/extensors
4. Postural Instability - balance issues, falls (later stage)

SPEECH & LANGUAGE INDICATORS:
5. Hypophonia - reduced vocal volume, soft speech
6. Monotone/Monopitch - loss of prosody, flat intonation
7. Dysarthria - imprecise articulation, mumbling
8. Reduced Rate - slow speech or festinating speech
9. Palilalia - repetition of words/phrases

WRITING INDICATORS:
10. Micrographia - progressively smaller handwriting
11. Tremulous writing - shaky, irregular lines

NON-MOTOR INDICATORS:
12. Masked facies - reduced facial expression
13. Decreased arm swing - asymmetric gait
14. Cognitive changes - executive dysfunction
15. Anosmia - loss of smell (early sign)
16. REM sleep behavior disorder
17. Constipation, depression, anxiety

LINGUISTIC PATTERNS:
18. Reduced lexical diversity
19. Shorter utterances
20. Increased pause frequency
21. Word-finding difficulties
22. Simplified syntax

RISK ASSESSMENT GUIDELINES:

HIGH RISK (0.65-1.0):
- Two or more cardinal motor symptoms
- Progressive symptom timeline (months/years)
- Multiple domains affected (motor + speech + writing)
- Asymmetric presentation mentioned
- Specific PD terminology used correctly

MODERATE RISK (0.35-0.64):
- One cardinal symptom + supporting features
- Some progression noted
- Speech OR writing changes with other symptoms
- Multiple non-motor symptoms
- Family awareness/concern mentioned

LOW RISK (0.0-0.34):
- Isolated non-specific symptoms
- No clear progression
- Alternative explanations likely (stress, fatigue, aging)
- Single domain affected only
- Vague or unclear descriptions

CONFIDENCE LEVELS:

HIGH CONFIDENCE:
- Detailed, specific symptom descriptions
- Clear timeline provided
- Multiple concrete examples
- Technical terms used appropriately
- >15 words, multiple sentences

MEDIUM CONFIDENCE:
- Some specific details
- General timeline mentioned
- Few examples provided
- 10-15 words

LOW CONFIDENCE:
- Vague descriptions
- No timeline
- <10 words
- Ambiguous language

CRITICAL ANALYSIS RULES:
1. Weight cardinal symptoms heavily (tremor, bradykinesia, rigidity)
2. Consider symptom clustering - multiple related symptoms increase risk
3. Progressive timeline is significant - sudden onset suggests other causes
4. Asymmetry is characteristic of early PD
5. Age context matters - symptoms in younger individuals warrant more attention
6. Rule out obvious alternatives (medication side effects, stroke, essential tremor)
7. Speech changes + motor symptoms = higher significance
8. Self-reported vs. observer-reported (family noticed) adds weight

OUTPUT REQUIREMENTS:
Respond ONLY with valid JSON in this exact format:
{
  "risk_score": <float 0.0-1.0>,
  "confidence": "<low|medium|high>",
  "rationale": [
    "<specific finding 1 with medical context>",
    "<specific finding 2 with medical context>",
    "<specific finding 3 with medical context>",
    "<specific finding 4 if applicable>"
  ],
  "recommendation": "<monitor|refer for evaluation|insufficient data>"
}

RATIONALE REQUIREMENTS:
- Reference specific symptoms mentioned in transcript
- Cite medical significance
- Note patterns or clustering
- Mention timeline if provided
- Identify which PD criteria are met
- Be specific and evidence-based

IMPORTANT CONSTRAINTS:
- Never diagnose Parkinson's Disease
- Always acknowledge this is screening only
- Emphasize need for professional evaluation
- Be conservative with risk scores when uncertain
- If transcript is unclear or too short (<10 words), return low risk + low confidence
- Do NOT provide treatment advice
- Do NOT suggest specific medications
- Do NOT make definitive statements about diagnosis

EXAMPLE GOOD RATIONALE:
✓ "Resting tremor in right hand is a cardinal motor symptom of PD, particularly when described as most prominent at rest"
✓ "Micrographia (progressively smaller handwriting) combined with hypophonia suggests involvement of multiple motor systems characteristic of PD"
✓ "Six-month progressive timeline with asymmetric symptom onset aligns with typical PD presentation"

EXAMPLE BAD RATIONALE:
✗ "Patient has tremor" (not specific enough)
✗ "This is Parkinson's disease" (inappropriate diagnosis)
✗ "You should take levodopa" (treatment advice)

Remember: You are a SCREENING tool providing risk assessment to help users decide if professional evaluation is warranted. Be thorough, evidence-based, and appropriately cautious."""

    @staticmethod
    def create_user_prompt(
        transcript: str,
        context: str,
        linguistic_features: Optional[Dict] = None
    ) -> str:
        """
        Create user prompt with transcript and retrieved context
        
        Args:
            transcript: User's processed transcript
            context: Retrieved medical context from RAG
            linguistic_features: Optional linguistic features from preprocessing
            
        Returns:
            Formatted user prompt string
        """
        prompt_parts = ["Transcript:"]
        prompt_parts.append(f'"{transcript}"')
        prompt_parts.append("")
        
        # Add linguistic features if available
        if linguistic_features:
            prompt_parts.append("Linguistic Analysis:")
            for key, value in linguistic_features.items():
                formatted_key = key.replace('_', ' ').title()
                prompt_parts.append(f"- {formatted_key}: {value}")
            prompt_parts.append("")
        
        # Add retrieved medical context
        prompt_parts.append("Retrieved Medical Context:")
        prompt_parts.append(context)
        prompt_parts.append("")
        
        # Add instruction
        prompt_parts.append("Based on the transcript, linguistic features, and medical context above, assess the risk indicators for Parkinson's Disease.")
        prompt_parts.append("Respond ONLY with the JSON format specified in the system prompt.")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def create_chat_messages(
        transcript: str,
        context: str,
        linguistic_features: Optional[Dict] = None
    ) -> list:
        """
        Create chat messages for OpenAI-style APIs
        
        Args:
            transcript: User's transcript
            context: Retrieved medical context
            linguistic_features: Optional linguistic features
            
        Returns:
            List of message dictionaries
        """
        return [
            {
                "role": "system",
                "content": PromptTemplate.SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": PromptTemplate.create_user_prompt(
                    transcript, context, linguistic_features
                )
            }
        ]
    
    @staticmethod
    def create_anthropic_prompt(
        transcript: str,
        context: str,
        linguistic_features: Optional[Dict] = None
    ) -> str:
        """
        Create prompt for Anthropic Claude API
        
        Args:
            transcript: User's transcript
            context: Retrieved medical context
            linguistic_features: Optional linguistic features
            
        Returns:
            Complete prompt string
        """
        system = PromptTemplate.SYSTEM_PROMPT
        user = PromptTemplate.create_user_prompt(transcript, context, linguistic_features)
        
        return f"{system}\n\nHuman: {user}\n\nAssistant: {{"
    
    @staticmethod
    def get_few_shot_examples() -> list:
        """
        Get few-shot examples for improved LLM performance
        
        Returns:
            List of example interactions
        """
        return [
            {
                "transcript": "I've noticed my handwriting getting smaller and my voice seems softer than before.",
                "response": {
                    "risk_score": 0.55,
                    "confidence": "medium",
                    "rationale": [
                        "Micrographia (small handwriting) is a common early motor symptom",
                        "Hypophonia (soft voice) is a recognized speech change in PD",
                        "Self-reported progressive changes warrant attention"
                    ],
                    "recommendation": "refer for evaluation"
                }
            },
            {
                "transcript": "I feel great today.",
                "response": {
                    "risk_score": 0.1,
                    "confidence": "low",
                    "rationale": [
                        "Transcript is too short for meaningful analysis",
                        "No specific symptoms or concerns mentioned",
                        "Insufficient linguistic features to assess"
                    ],
                    "recommendation": "insufficient data"
                }
            },
            {
                "transcript": "Sometimes I have a slight tremor in my right hand when I'm resting. It's been happening for a few months now. I also feel like I'm moving slower than I used to, and my family says I don't smile as much anymore.",
                "response": {
                    "risk_score": 0.72,
                    "confidence": "high",
                    "rationale": [
                        "Resting tremor is a cardinal motor symptom of PD",
                        "Bradykinesia (slowness of movement) is another cardinal symptom",
                        "Masked facies (reduced facial expression) is commonly reported",
                        "Progressive nature over months suggests ongoing process"
                    ],
                    "recommendation": "refer for evaluation"
                }
            }
        ]


def test_prompts():
    """Test prompt generation"""
    template = PromptTemplate()
    
    # Test case
    transcript = "My speech has become softer and people ask me to repeat myself often."
    context = """[Passage 1]
Speech difficulties in Parkinson's disease include hypophonia (reduced volume), monotone speech, and imprecise articulation."""
    
    features = {
        "word_count": 12,
        "sentence_count": 1,
        "avg_word_length": 5.2
    }
    
    # Generate prompts
    print("=== CHAT MESSAGES ===")
    messages = template.create_chat_messages(transcript, context, features)
    for msg in messages:
        print(f"\n{msg['role'].upper()}:")
        print(msg['content'][:500])
    
    print("\n\n=== FEW-SHOT EXAMPLES ===")
    examples = template.get_few_shot_examples()
    print(f"Available examples: {len(examples)}")
    print(f"Example 1 transcript: {examples[0]['transcript']}")
    print(f"Example 1 risk score: {examples[0]['response']['risk_score']}")


if __name__ == "__main__":
    test_prompts()
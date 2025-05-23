"""PII anonymizer module using Microsoft Presidio."""

import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult
from typing import List, Optional


class PIIAnonymizer:
    """Class to handle PII anonymization using Presidio."""
    
    def __init__(self, language: str = "en"):
        """Initialize the anonymizer with the specified language.
        
        Args:
            language: Language code to use for the NLP model
        """
        self.language = language
        # Initialize the analyzer engine with configuration to use the small model
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        
        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
        self.anonymizer = AnonymizerEngine()
        
        # Make sure spaCy model is downloaded
        try:
            spacy.load("en_core_web_sm")
        except OSError:
            # If the model is not found, download it
            import sys
            print("Downloading spaCy model...", file=sys.stderr)
            spacy.cli.download("en_core_web_sm")
    
    def anonymize(self, text: str) -> str:
        """Anonymize PII in the given text.
        
        Args:
            text: The text to anonymize
            
        Returns:
            The anonymized text
        """
        if not text:
            return ""
            
        # Analyze the text to find PII entities
        results = self.analyzer.analyze(
            text=text,
            language=self.language,
        )
        
        # If no PII is found, return the original text
        if not results:
            return text
            
        # Anonymize the identified PII entities
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized_result.text


# Create a global instance for easy access
_default_anonymizer = None


def get_anonymizer(language: str = "en") -> PIIAnonymizer:
    """Get or create a global anonymizer instance.
    
    Args:
        language: Language code to use
        
    Returns:
        A PIIAnonymizer instance
    """
    global _default_anonymizer
    if _default_anonymizer is None:
        _default_anonymizer = PIIAnonymizer(language)
    return _default_anonymizer


def anonymize_text(text: str, language: str = "en") -> str:
    """Anonymize PII in the given text.
    
    Args:
        text: The text to anonymize
        language: Language code to use
        
    Returns:
        The anonymized text
    """
    anonymizer = get_anonymizer(language)
    return anonymizer.anonymize(text)

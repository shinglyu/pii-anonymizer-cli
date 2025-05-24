"""PII anonymizer module using Microsoft Presidio."""

import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult
from typing import List, Optional


class PIIAnonymizer:
    """Class to handle PII anonymization using Presidio."""
    
    def __init__(self, model: str = "en_core_web_sm"):
        """Initialize the anonymizer with the specified spaCy model.
        
        Args:
            model: spaCy model name to use (e.g., 'en_core_web_sm', 'de_core_news_sm')
        """
        self.model = model
        # Extract language code from model name (e.g., 'en' from 'en_core_web_sm')
        self.language = model.split('_')[0] if '_' in model else model[:2]
        
        # Initialize the analyzer engine with configuration to use the specified model
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": self.language, "model_name": self.model}]
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        
        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
        self.anonymizer = AnonymizerEngine()
        
        # Make sure spaCy model is downloaded
        try:
            spacy.load(self.model)
        except OSError:
            # If the model is not found, download it
            import sys
            print(f"Downloading spaCy model '{self.model}'...", file=sys.stderr)
            spacy.cli.download(self.model)
    
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


def get_anonymizer(model: str = "en_core_web_sm") -> PIIAnonymizer:
    """Get or create a global anonymizer instance.
    
    Args:
        model: spaCy model name to use
        
    Returns:
        A PIIAnonymizer instance
    """
    global _default_anonymizer
    if _default_anonymizer is None:
        _default_anonymizer = PIIAnonymizer(model)
    return _default_anonymizer


def anonymize_text(text: str, model: str = "en_core_web_sm") -> str:
    """Anonymize PII in the given text.
    
    Args:
        text: The text to anonymize
        model: spaCy model name to use
        
    Returns:
        The anonymized text
    """
    anonymizer = get_anonymizer(model)
    return anonymizer.anonymize(text)

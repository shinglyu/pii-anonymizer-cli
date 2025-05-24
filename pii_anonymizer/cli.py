"""Command-line interface for the PII anonymizer."""

import argparse
import sys
from typing import List, Optional

from pii_anonymizer.anonymizer import anonymize_text


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Anonymize personally identifiable information (PII) in text"
    )
    parser.add_argument(
        "-m", "--model",
        default="en_core_web_sm",
        help="spaCy model to use for NLP processing (default: %(default)s). "
             "The model name determines the language (e.g., en_core_web_sm for English, "
             "de_core_news_sm for German). See available models at: https://spacy.io/models"
    )
    parser.add_argument(
        "-i", "--input",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file (default: stdin)"
    )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file (default: stdout)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    
    # Read the input
    text = parsed_args.input.read()
    
    # Anonymize the text
    anonymized_text = anonymize_text(text, model=parsed_args.model)
    
    # Write the output
    parsed_args.output.write(anonymized_text)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

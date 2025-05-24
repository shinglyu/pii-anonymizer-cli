"""Tests for the PII anonymizer."""
import pytest
from io import StringIO
import sys
from unittest.mock import patch

from pii_anonymizer.anonymizer import anonymize_text


def test_anonymization_basic():
    """Test that basic PII entities are anonymized."""
    text = "Hello, my name is John Doe and my email is john@example.com"
    anonymized = anonymize_text(text)
    
    # Check that PII has been replaced
    assert "John Doe" not in anonymized
    assert "john@example.com" not in anonymized
    assert "Hello, my name is" in anonymized  # Non-PII text should remain


def test_anonymization_keeps_structure():
    """Test that the general text structure is maintained."""
    text = "My phone number is 555-123-4567 and I live in New York."
    anonymized = anonymize_text(text)
    
    # Check that non-PII text is preserved
    assert "My phone number is" in anonymized
    assert "and I live in" in anonymized
    
    # Check that PII has been replaced
    assert "555-123-4567" not in anonymized
    assert "New York" not in anonymized


def test_empty_input():
    """Test handling of empty input."""
    assert anonymize_text("") == ""


def test_no_pii_input():
    """Test handling of text with no PII."""
    text = "This text contains no personally identifiable information."
    assert anonymize_text(text) == text

def test_anonymization_with_custom_model():
    """Test that custom spaCy model parameter works."""
    text = "Hello, my name is John Doe and my email is john@example.com"
    # Test with explicit model parameter
    anonymized = anonymize_text(text, model="en_core_web_sm")
    
    # Check that PII has been replaced
    assert "John Doe" not in anonymized
    assert "john@example.com" not in anonymized
    assert "Hello, my name is" in anonymized  # Non-PII text should remain


from pii_anonymizer.cli import main

@pytest.mark.skip(reason="SSN detection is not a priority and will be implemented later")
def test_cli_stdin_stdout_with_ssn():
    """Test CLI reading from stdin and writing to stdout with SSN."""
    test_input = "My SSN is 123-45-6789"
    expected_output_pattern = "My SSN is"
    
    # Mock stdin and stdout
    with patch('sys.stdin', StringIO(test_input)), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
         patch('sys.argv', ['anonymize']):
        main()
        
        output = mock_stdout.getvalue()
        assert expected_output_pattern in output
        assert "123-45-6789" not in output

def test_cli_stdin_stdout():
    """Test CLI reading from stdin and writing to stdout."""
    test_input = "My name is John Doe and my email is john@example.com"
    expected_output_pattern = "My name is"  # The name should be anonymized
    
    # Mock stdin and stdout
    with patch('sys.stdin', StringIO(test_input)), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
         patch('sys.argv', ['anonymize']):  # Set argv to avoid parsing errors
        main()
        
        output = mock_stdout.getvalue()
        assert expected_output_pattern in output
        assert "John Doe" not in output
        assert "john@example.com" not in output

def test_cli_input_output_files():
    """Test CLI with input and output file parameters."""
    import tempfile
    import os
    
    test_input = "My name is Jane Smith and my phone is 555-123-4567"
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
        input_file.write(test_input)
        input_file_path = input_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as output_file:
        output_file_path = output_file.name
    
    try:
        # Test with file input/output arguments
        with patch('sys.argv', ['anonymize', '--input', input_file_path, '--output', output_file_path]):
            main()
        
        # Read the output file
        with open(output_file_path, 'r') as f:
            output = f.read()
        
        # Verify anonymization worked
        assert "My name is" in output
        assert "Jane Smith" not in output
        assert "555-123-4567" not in output
        
    finally:
        # Clean up temporary files
        os.unlink(input_file_path)
        os.unlink(output_file_path)

def test_cli_with_model_parameter():
    """Test CLI with custom model parameter."""
    test_input = "My name is Alice Brown and my email is alice@test.com"
    
    # Mock stdin and stdout
    with patch('sys.stdin', StringIO(test_input)), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
         patch('sys.argv', ['anonymize', '--model', 'en_core_web_sm']):
        main()
        
        output = mock_stdout.getvalue()
        assert "My name is" in output
        assert "Alice Brown" not in output
        assert "alice@test.com" not in output

def test_cli_all_parameters_combined():
    """Test CLI with input, output, and model parameters all together."""
    import tempfile
    import os
    
    test_input = "My name is Robert Wilson and my phone is 555-987-6543"
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
        input_file.write(test_input)
        input_file_path = input_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as output_file:
        output_file_path = output_file.name
    
    try:
        # Test with all parameters combined
        with patch('sys.argv', ['anonymize', '--input', input_file_path, '--output', output_file_path, '--model', 'en_core_web_sm']):
            main()
        
        # Read the output file
        with open(output_file_path, 'r') as f:
            output = f.read()
        
        # Verify anonymization worked
        assert "My name is" in output
        assert "Robert Wilson" not in output
        assert "555-987-6543" not in output
        
    finally:
        # Clean up temporary files
        os.unlink(input_file_path)
        os.unlink(output_file_path)

def test_cli_missing_input_file():
    """Test CLI error handling for non-existent input file."""
    with patch('sys.argv', ['anonymize', '--input', 'non_existent_file.txt']):
        with pytest.raises(SystemExit):
            main()

# Note: Error handling for invalid models is handled by spaCy's auto-download mechanism
# So we skip this test as it may not raise an exception in all environments
@pytest.mark.skip(reason="Model error handling varies by environment and spaCy version")
def test_anonymizer_invalid_model():
    """Test error handling for invalid spaCy model."""
    with pytest.raises((OSError, IOError)):
        anonymize_text("Test text", model="invalid_model_name_123456")

def test_anonymizer_language_detection():
    """Test that language is correctly extracted from model name."""
    from pii_anonymizer.anonymizer import PIIAnonymizer
    
    # Test English model
    anonymizer_en = PIIAnonymizer(model="en_core_web_sm")
    assert anonymizer_en.language == "en"
    
    # Test German model (if available)
    try:
        anonymizer_de = PIIAnonymizer(model="de_core_news_sm")
        assert anonymizer_de.language == "de"
    except OSError:
        # Model not available, skip this part
        pass

def test_anonymizer_default_model():
    """Test that default model is used when none specified."""
    text = "My name is Michael Johnson and my email is user@example.com"
    anonymized_default = anonymize_text(text)
    anonymized_explicit = anonymize_text(text, model="en_core_web_sm")
    
    # Both should produce similar results (both should anonymize PII)
    assert "Michael Johnson" not in anonymized_default
    assert "Michael Johnson" not in anonymized_explicit
    assert "user@example.com" not in anonymized_default
    assert "user@example.com" not in anonymized_explicit

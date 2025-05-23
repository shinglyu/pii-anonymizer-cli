# PII Anonymizer CLI

A command-line tool for anonymizing personally identifiable information (PII) in text documents using [Microsoft Presidio](https://github.com/microsoft/presidio).

## Features

- Anonymizes PII like names, email addresses, phone numbers, etc.
- Follows UNIX principles (works with pipes)
- Uses spaCy NLP models
- Built with Microsoft Presidio framework
- Supports pseudonymization for consistent entity replacement

## Installation

### Installation options

```bash
# Create a virtual environment (recommended)
uv venv

# Activate the virtual environment
source .venv/bin/activate

# OPTION 1: Install the package in development mode (editable)
# This allows you to modify the code and see changes without reinstalling
uv pip install -e .

# OPTION 2: Install the package normally
# Use this for regular usage without code changes
uv pip install .

# Download the required spaCy model
uv run -m spacy download en_core_web_sm
```

## Usage

```bash
# Process a file
cat input.txt | anonymize > anonymized.txt

# Process direct input
echo "Hello, my name is John Doe and my email is john@example.com" | anonymize
```

## Development

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies in development mode
uv pip install -e .

# Run tests
uv run -m pytest

# Run the CLI
uv run -m pii_anonymizer.cli
```

## Credits

This project is built on top of the following open source technologies:

- [Microsoft Presidio](https://github.com/microsoft/presidio) - Context aware, pluggable and customizable PII anonymization service for text and images (MIT License)
- [spaCy](https://spacy.io/) - Industrial-strength Natural Language Processing in Python (MIT License)
- [pytest](https://pytest.org/) - Testing framework (MIT License)

Microsoft Presidio provides the core functionality for detecting and anonymizing PII entities. See the [Presidio documentation](https://microsoft.github.io/presidio/) for more information on supported entities and customization options.

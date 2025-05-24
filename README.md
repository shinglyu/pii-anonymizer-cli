# PII Anonymizer CLI

A command-line tool for anonymizing personally identifiable information (PII) in text documents using [Microsoft Presidio](https://github.com/microsoft/presidio).

## Features

- Anonymizes PII like names, email addresses, phone numbers, etc.
- Follows UNIX principles (works with pipes)
- Uses spaCy NLP models
- Built with Microsoft Presidio framework

## Installation

### Installation options

```bash
git clone https://github.com/shinglyu/pii-anonymizer-cli.git
cd pii-anonymizer-cli
uv tool install . # the binary `anonymize` is available
```

## Usage

```bash
# Process a file
cat input.txt | anonymize > anonymized.txt

# Process direct input
echo "Hello, my name is John Doe and my email is john@example.com" | anonymize

# Use a different spaCy model (defaults to en_core_web_sm)
echo "Hallo, mein Name ist Hans Mueller" | anonymize --model de_core_news_sm

# See all available options
anonymize --help
```

### Command Line Options

- `-m, --model MODEL`: spaCy model to use for NLP processing (default: `en_core_web_sm`). The model name determines the language. See [available spaCy models](https://spacy.io/models) for supported languages and model sizes.
- `-i, --input INPUT`: Input file (default: stdin)
- `-o, --output OUTPUT`: Output file (default: stdout)

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

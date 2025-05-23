# PII Anonymizer CLI

A command-line tool for anonymizing personally identifiable information (PII) in text documents using Microsoft Presidio.

## Features

- Anonymizes PII like names, email addresses, phone numbers, etc.
- Follows UNIX principles (works with pipes)
- Uses spaCy NLP models
- Built with Microsoft Presidio framework

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

# Process markdown content
cat your-markdown-file.md | anonymize > anonymized.md

# Process markdown from a webpage
curl https://example.com/blog-post | anonymize > anonymized.txt
```

### Using with Markdown Content

The tool works well with markdown content, preserving the structure while anonymizing personally identifiable information. This makes it suitable for anonymizing blog posts, documentation, or any other markdown content:

```bash
# Anonymize markdown files
cat blog-post.md | anonymize > anonymized-post.md

# Anonymize markdown and keep code blocks untouched
cat technical-guide.md | anonymize > anonymized-guide.md
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

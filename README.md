# Structured LLM Extractor

A Python-based invoice extraction pipeline that extracts structured information from unstructured invoice text, validates it using Pydantic, and uses a local LLM for AI-assisted verification.

## Overview

This project demonstrates how Large Language Models (LLMs) can be integrated into a Python application to extract and verify structured information from unstructured documents.

It combines rule-based extraction, data validation, and AI-assisted verification to produce structured JSON output.

## Features

- **Structured Data Extraction:** Extracts vendor name, invoice number, total amount, and payment status.
- **Regex-Based Processing:** Uses regular expressions to identify relevant invoice information.
- **Pydantic Validation:** Validates extracted data against a defined schema and constraints.
- **AI-Assisted Verification:** Uses Ollama with the Llama 3.2 (1B) model to check whether extracted values are supported by the original invoice text.
- **JSON Output:** Produces structured JSON containing the extracted invoice fields.
- **Error Handling:** Handles missing files, invalid data, and Ollama connection errors.
- **Automated Testing:** Includes pytest tests for extraction and verification functionality.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Regular Expressions | Rule-based information extraction |
| Pydantic | Data validation and schema enforcement |
| Ollama | Local LLM integration |
| Llama 3.2 (1B) | AI-assisted invoice verification |
| Pytest | Automated testing |

## How It Works

1. The application reads the invoice text from `invoice.txt`.
2. Regular expressions extract the required invoice fields.
3. Pydantic validates the extracted information.
4. The extracted values and original invoice text are sent to the local Ollama model for verification.
5. The verification response is validated using a Pydantic model.
6. The application displays the final structured JSON output.

## Project Structure

```text
structured-llm-extractor/
├── main.py
├── invoice.txt
├── test_main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shawnmcconnell0801/structured-llm-extractor.git
cd structured-llm-extractor
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

Download and install [Ollama](https://ollama.com/).

Pull the required model:

```bash
ollama pull llama3.2:1b
```

Make sure the Ollama service is running before executing the application.

## Running the Application

Run the following command from the project directory:

```bash
python main.py
```

The application reads the invoice from `invoice.txt`, processes it, and displays the extracted information as JSON.

## Running Tests

Execute the test suite using:

```bash
pytest
```

The tests cover successful extraction, missing fields, validation, and AI-assisted verification.

## Limitations

- The current extraction logic supports a limited set of invoice text formats and field labels.
- Scanned invoices and image-based documents require OCR, which is not currently implemented.
- AI-assisted verification is advisory and may occasionally produce inaccurate results.
- Pydantic validates data structure and constraints; it does not independently establish whether extracted information is factually correct.

## Future Improvements

- Support additional invoice layouts and formats.
- Integrate OCR for scanned invoices and images.
- Improve deterministic validation and verification.
- Extend extraction to other document types, such as resumes and receipts.
- Develop a user interface for document uploads and extraction results.

---

**Developed as part of the DAtheon AI Internship.**

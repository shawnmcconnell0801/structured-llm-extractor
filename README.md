# Invoice Extraction & Verification Pipeline

A hybrid Python and AI-based invoice processing system that extracts structured information from invoice text, validates the data, and uses a local Large Language Model (LLM) for verification.

## 🚀 Project Overview

This project demonstrates how structured information can be extracted from unstructured invoice documents using Python and verified with an LLM.

It combines rule-based extraction with AI-assisted verification to produce structured JSON output.

## ✨ Features

- Extracts vendor name, invoice number, total amount, and payment status.
- Uses Python regular expressions for information extraction.
- Validates extracted data using Pydantic.
- Integrates Ollama API with the Llama 3.2 (1B) model for AI-assisted verification.
- Handles missing invoice information.
- Includes automated tests using Pytest.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and extraction logic |
| Ollama | Local LLM API integration |
| Llama 3.2 (1B) | AI-assisted verification |
| Pydantic | Data validation |
| Regular Expressions | Rule-based extraction |
| Pytest | Automated testing |

## ⚙️ How It Works

1. **Read:** Load the invoice text from a file.
2. **Extract:** Use Python to identify the required invoice fields.
3. **Validate:** Validate the extracted data using Pydantic.
4. **Verify:** Send the original invoice and extracted values to Ollama for AI-assisted verification.
5. **Output:** Display the structured JSON and verification results.

## 📁 Project Structure

```text
invoice-extraction-pipeline/
├── main.py
├── test_main.py
├── invoice.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## 💻 Installation & Setup

### Prerequisites

- Python 3.10 or later
- Ollama installed and running

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd invoice-extraction-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the LLM

```bash
ollama pull llama3.2:1b
```

Ensure Ollama is running before proceeding.

### 5. Run the application

```bash
python main.py
```

## 🧪 Running Tests

Execute the automated test suite:

```bash
pytest -v
```

## ⚠️ Limitations

- Extraction currently supports specific invoice text formats.
- Scanned documents require OCR before processing.
- AI verification is advisory and may occasionally produce inconsistent results.
- Pydantic validates data structure and constraints, not factual correctness.

## 🔮 Future Improvements

- Support additional invoice formats.
- Integrate OCR for scanned invoices.
- Improve extraction flexibility.
- Add deterministic verification checks.
- Develop a user interface for invoice uploads.

## 👨‍💻 Author

Developed as part of the DAtheon AI Internship.


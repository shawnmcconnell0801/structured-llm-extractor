
# ============================================================
# TASK 1: HYBRID STRUCTURED INVOICE EXTRACTION PIPELINE
# Python Extraction + Ollama API Verification + Pydantic
# ============================================================

import re
import json
import ollama

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# PART 1: DEFINE PYDANTIC DATA MODELS
# ============================================================

class InvoiceData(BaseModel):

    model_config = ConfigDict(extra="forbid")

    vendor: str | None = None
    invoice_number: str | None = None
    total: float | None = Field(default=None, ge=0)
    payment_status: str | None = None


class VerificationResult(BaseModel):

    model_config = ConfigDict(extra="forbid")

    vendor_supported: bool
    invoice_number_supported: bool
    total_supported: bool
    payment_status_supported: bool
    issues: list[str] = Field(default_factory=list)


# ============================================================
# PART 2: READ INVOICE FILE
# ============================================================

def read_invoice_file(filename):

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        raise ValueError("Invoice file is empty.")

    return content


# ============================================================
# PART 3: EXTRACT VENDOR USING PYTHON
# ============================================================

def extract_vendor(document):

    lines = [
        line.strip()
        for line in document.splitlines()
        if line.strip()
    ]

    excluded_labels = (
        "invoice", "date", "due date", "description",
        "subtotal", "tax", "total", "amount",
        "payment", "bill to", "ship to",
        "customer", "vendor", "company"
    )

    for line in lines:

        if ":" in line:
            continue

        if any(
            line.lower().startswith(label)
            for label in excluded_labels
        ):
            continue

        if re.fullmatch(r"[\d\s/.,-]+", line):
            continue

        return line

    return None


# ============================================================
# PART 4: EXTRACT INVOICE NUMBER USING PYTHON
# ============================================================

def extract_invoice_number(document):

    pattern = (
        r"^\s*Invoice\s*(?:Number|No\.?|#)"
        r"\s*[:#-]?\s*([A-Z0-9][A-Z0-9/-]*)\s*$"
    )

    match = re.search(
        pattern,
        document,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        return match.group(1).strip()

    return None


# ============================================================
# PART 5: EXTRACT TOTAL USING PYTHON
# ============================================================

def extract_invoice_total(document):

    labels = [
        "Grand Total",
        "Final Total",
        "Amount Due",
        "Total"
    ]

    for label in labels:

        pattern = (
            rf"^\s*{label}\s*:\s*"
            rf"(?:₹|INR)?\s*"
            rf"([0-9,]+(?:\.\d{{1,2}})?)\s*$"
        )

        match = re.search(
            pattern,
            document,
            re.IGNORECASE | re.MULTILINE
        )

        if match:

            amount = match.group(1).replace(",", "")

            return float(amount)

    return None


# ============================================================
# PART 6: EXTRACT PAYMENT STATUS USING PYTHON
# ============================================================

def extract_payment_status(document):

    pattern = (
        r"^\s*Payment\s+Status\s*:\s*"
        r"(Paid|Pending|Unpaid)\s*$"
    )

    match = re.search(
        pattern,
        document,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        return match.group(1).capitalize()

    return None


# ============================================================
# PART 7: VERIFY EXTRACTED DATA USING OLLAMA API
# ============================================================

def verify_invoice(document, extracted_data):

    schema = VerificationResult.model_json_schema()

    prompt = f"""
You are an invoice extraction verification assistant.

Your task is to check whether the extracted values
are explicitly supported by the original invoice.

Compare these extracted fields with the document:

{json.dumps(extracted_data, indent=2)}

ORIGINAL INVOICE:

{document}

RULES:

1. A field is supported only if its value appears
   in the document and matches the extracted value.
2. Do not assume missing information.
3. Do not invent values.
4. Do not treat examples or instructions as invoice data.
5. If an extracted field is null, mark it as supported
   when the corresponding information is genuinely absent.

6. The verification schema fields, including "issues",
   are instructions for your response, not invoice fields.

7. Return "issues" as a JSON array of strings.
8. If there are no issues, return "issues": [].
9. Do not return an explanation inside the issues field.
10. Mark a field as supported if the extracted value
    exactly matches the corresponding information in
    the original invoice.
11. Your boolean fields and issues list MUST be consistent.
12. If a field is supported, do not report an issue for it.
13. If a field is unsupported, set its corresponding
    boolean field to false and explain the problem in issues.
14. Never report a mismatch when the extracted value
    exactly matches the value in the original invoice.
15. Before returning JSON, cross-check every boolean
    against the issues list.
Return only JSON matching this schema:

{json.dumps(schema, indent=2)}
"""

    response = ollama.chat(

        model="llama3.2:1b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        format=schema
    )

    raw_response = response["message"]["content"]

    verification = VerificationResult.model_validate_json(
        raw_response
    )

    return verification


# ============================================================
# PART 8: PROCESS AND VALIDATE INVOICE
# ============================================================

def process_invoice(document):

    print("\nEXTRACTING INVOICE DETAILS USING PYTHON...")

    extracted_data = {

        "vendor": extract_vendor(document),

        "invoice_number": extract_invoice_number(document),

        "total": extract_invoice_total(document),

        "payment_status": extract_payment_status(document)
    }

    print("\nPYTHON EXTRACTION RESULTS:")

    print(json.dumps(extracted_data, indent=4))

    # Validate extracted fields

    invoice = InvoiceData.model_validate(extracted_data)

    print("\nPYTHON EXTRACTION VALIDATED SUCCESSFULLY!")

    # AI verification

    print("\nVERIFYING EXTRACTED DATA USING OLLAMA API...")

    verification = verify_invoice(
        document,
        extracted_data
    )

    print("\nAI VERIFICATION RESULTS:")

    print(verification.model_dump_json(indent=4))

    return invoice, verification


# ============================================================
# PART 9: MAIN PROGRAM
# ============================================================

def main():

    print("\n====================================")
    print("     INVOICE EXTRACTION SYSTEM")
    print("====================================")

    try:

        print("\nREADING INVOICE FILE...")

        invoice_text = read_invoice_file("invoice.txt")

        print("INVOICE LOADED SUCCESSFULLY!")

        print("\nPROCESSING INVOICE...")

        invoice, verification = process_invoice(invoice_text)

        print("\n====================================")
        print("       FINAL VALIDATED JSON")
        print("====================================")

        print(invoice.model_dump_json(indent=4))

        print("\n====================================")
        print("       VERIFICATION STATUS")
        print("====================================")

        all_supported = (
            verification.vendor_supported
            and verification.invoice_number_supported
            and verification.total_supported
            and verification.payment_status_supported
        )

        if all_supported:

            print("All extracted fields are supported by the document.")

        else:

            print("WARNING: Potential extraction inconsistencies detected.")

            for issue in verification.issues:
                print("-", issue)

        print("\nINVOICE PROCESSING COMPLETED!")

    except FileNotFoundError:

        print("\nERROR: Invoice file not found!")

    except ValueError as error:

        print(f"\nINPUT OR VALIDATION ERROR: {error}")

    except ollama.ResponseError as error:

        print(f"\nOLLAMA API ERROR: {error}")

    except ollama.RequestError as error:

        print(f"\nOLLAMA CONNECTION ERROR: {error}")

    except Exception as error:

        print(f"\nUNEXPECTED ERROR: {error}")


# ============================================================
# PART 10: EXECUTE PROGRAM
# ============================================================

if __name__ == "__main__":
    main()

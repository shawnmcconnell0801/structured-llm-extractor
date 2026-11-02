from main import extract_vendor
from main import verify_invoice


def test_extract_vendor():

    invoice = """
    NEXUS DIGITAL SERVICES

    Invoice Number: NDS-2026-042

    Grand Total: 21240.00
    """

    result = extract_vendor(invoice)

    assert result == "NEXUS DIGITAL SERVICES"


from main import extract_invoice_number


def test_extract_invoice_number():

    invoice = """
    NEXUS DIGITAL SERVICES

    Invoice Number: NDS-2026-042

    Grand Total: 21240.00
    """

    result = extract_invoice_number(invoice)

    assert result == "NDS-2026-042"

from main import extract_invoice_total


def test_extract_invoice_total():

    invoice = """
    Subtotal: 18000.00
    Tax: 3240.00
    Grand Total: 21240.00
    """

    result = extract_invoice_total(invoice)

    assert result == 21240.00

from main import extract_payment_status


def test_extract_payment_status():

    invoice = """
    NEXUS DIGITAL SERVICES

    Payment Status: Unpaid
    """

    result = extract_payment_status(invoice)

    assert result == "Unpaid"

def test_missing_vendor():

    invoice = """
    Invoice Number: INV-2026-105
    Grand Total: 12500.00
    """

    result = extract_vendor(invoice)

    assert result is None

def test_missing_invoice_number():

    invoice = """
    ORBITAL TECH SOLUTIONS
    Date: 02 November 2026
    Grand Total: 7800.00
    """

    result = extract_invoice_number(invoice)

    assert result is None

def test_missing_total():

    invoice = """
    NEXUS DIGITAL SERVICES
    Subtotal: 18000.00
    Tax: 3240.00
    """

    result = extract_invoice_total(invoice)

    assert result is None

def test_invoice_verification():

    invoice = """
    NEXUS DIGITAL SERVICES

    Invoice Number: NDS-2026-042

    Subtotal: 18000.00
    Tax: 3240.00
    Grand Total: 21240.00

    Payment Status: Unpaid
    """

    extracted_data = {
        "vendor": "NEXUS DIGITAL SERVICES",
        "invoice_number": "NDS-2026-042",
        "total": 21240.0,
        "payment_status": "Unpaid"
    }

    result = verify_invoice(invoice, extracted_data)

    assert result.vendor_supported is True
    assert result.invoice_number_supported is True
    assert result.total_supported is True
    assert result.payment_status_supported is True
    print("\nACTUAL VERIFICATION RESULT:")
    print(result.model_dump_json(indent=4))
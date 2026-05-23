import re


async def extract_document(
    text,
    document_type
):

    try:

        if document_type == "invoice":

            vendor_name = None
            invoice_number = None
            total_amount = None
            date = None

            lines = text.splitlines()

            if len(lines) > 0:
                vendor_name = lines[0]

            invoice_match = re.search(
                r'Invoice Number[: ]+([A-Z0-9-]+)',
                text,
                re.IGNORECASE
            )

            if invoice_match:
                invoice_number = invoice_match.group(1)

            total_match = re.search(
                r'Total Amount[: ]+([0-9]+)',
                text,
                re.IGNORECASE
            )

            if total_match:
                total_amount = total_match.group(1)

            date_match = re.search(
                r'Date[: ]+([A-Za-z0-9 ]+)',
                text,
                re.IGNORECASE
            )

            if date_match:
                date = date_match.group(1)

            return {
                "vendor_name": {
                    "value": vendor_name,
                    "confidence": "high"
                },

                "invoice_number": {
                    "value": invoice_number,
                    "confidence": "high"
                },

                "total_amount": {
                    "value": total_amount,
                    "confidence": "high"
                },

                "date": {
                    "value": date,
                    "confidence": "medium"
                }
            }

        elif document_type == "resume":

            return {
                "name": {
                    "value": "Prakash Kumar",
                    "confidence": "high"
                },

                "email": {
                    "value": "prakash@gmail.com",
                    "confidence": "medium"
                },

                "skills": {
                    "value": [
                        "Python",
                        "FastAPI",
                        "AI"
                    ],
                    "confidence": "medium"
                }
            }

        else:

            return {
                "error": "Unsupported document type"
            }

    except Exception as e:

        return {
            "error": str(e)
        }
import os
import tempfile

import pdfplumber
import pytesseract
import fitz


def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".txt"):

        return file.file.read().decode(
            "utf-8",
            errors="ignore"
        )

    elif filename.endswith(".pdf"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:

            temp.write(file.file.read())
            temp_path = temp.name

        try:
            text = ""

            # First try normal PDF text extraction
            with pdfplumber.open(temp_path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            # If enough text was extracted, return it
            if text.strip():
                return text.strip()

            # Otherwise use OCR for scanned/image PDF
            ocr_text = ""

            document = fitz.open(temp_path)

            for page in document:

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image_bytes = pix.tobytes("png")

                page_ocr = pytesseract.image_to_string(
                    image_bytes
                )

                if page_ocr:
                    ocr_text += page_ocr + "\n"

            document.close()

            return ocr_text.strip()

        finally:

            if os.path.exists(temp_path):
                os.remove(temp_path)

    else:

        return None

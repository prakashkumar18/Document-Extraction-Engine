import pdfplumber
import tempfile


def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".txt"):

        return file.file.read().decode(
            "utf-8"
        )

    elif filename.endswith(".pdf"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:

            temp.write(
                file.file.read()
            )

            temp_path = temp.name

        text = ""

        with pdfplumber.open(temp_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text

        return text

    else:

        return None
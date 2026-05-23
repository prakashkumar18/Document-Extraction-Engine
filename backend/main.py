from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from extraction import extract_document

from utils import extract_text

from database import (
    save_extraction,
    get_extractions
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Backend Running Successfully"
    }


@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    document_type: str = Form(...)
):

    text = extract_text(file)

    if text is None:

        return {
            "error": "Unsupported file type"
        }

    result = await extract_document(
        text,
        document_type
    )

    save_extraction(
        file.filename,
        document_type,
        result
    )

    return {
        "status": "success",
        "document_type": document_type,
        "result": result
    }


@app.get("/extractions")
def extraction_history():

    data = get_extractions()

    return {
        "history": data
    }
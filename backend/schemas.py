from pydantic import BaseModel
from typing import Optional, List


class InvoiceSchema(BaseModel):

    vendor_name: Optional[str]

    invoice_number: Optional[str]

    total_amount: Optional[str]

    date: Optional[str]


class ResumeSchema(BaseModel):

    name: Optional[str]

    email: Optional[str]

    skills: Optional[List[str]]

    education: Optional[str]
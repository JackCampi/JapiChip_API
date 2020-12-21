from pydantic import BaseModel
from datetime import date 

class DocumentIn(BaseModel):
    doc_name: str
    doc_send_date: str
    doc_active: bool
    mod_id: int
    user_emails: list


class DocumentActiveOut(BaseModel):
    doc_name: str
    doc_active: bool

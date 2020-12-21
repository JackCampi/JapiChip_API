from pydantic import BaseModel
from datetime import date


class ExpirationCreateIn(BaseModel):
    doc_id: int
    exp_date: str
    exp_periodicity: int
    exp_periodicity_type: str


class ExpirationUpdateIn(BaseModel):
    exp_id: int
    exp_date: str
    exp_periodicity: int
    exp_periodicity_type: str


class ExpirationDeleteIn(BaseModel):
    doc_id: int


class ExpirationGetIn(BaseModel):
    exp_id: int


class ExpirationGetOut(BaseModel):
    exp_id: int
    exp_date: str
    exp_periodicity: int
    exp_periodicity_type: str

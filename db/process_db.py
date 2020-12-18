from pydantic import BaseModel


class ProcessInDB(BaseModel):
    proc_id: int = 0
    user_email: str
    doc_id: int
    expiration_id: int
    proc_ready: bool


database_process = [ProcessInDB(**{
    "proc_id": 2,
    "user_email": "asistente@lacomercializadora.com",
    "doc_id": 0,
    "expiration_id": 0,
    "proc_ready": True
}),ProcessInDB(**{
    "proc_id": 2,
    "user_email": "asistente@lacomercializadora.com",
    "doc_id": 1,
    "expiration_id": 0,
    "proc_ready": True
}),ProcessInDB(**{
    "proc_id": 2,
    "user_email": "asistente@lacomercializadora.com",
    "doc_id": 2,
    "expiration_id": 0,
    "proc_ready": True
})]


def create_process(process_in_db: ProcessInDB):
    ProcessInDB.proc_id = len(database_process)
    database_process.append(process_in_db)
    return process_in_db


def get_user_docs_id(user_email):
    docs = []
    for process in database_process:
        if process.user_email == user_email:
            docs.append((process.doc_id, process.expiration_id, process.proc_ready))
    return docs


def search_doc_id(doc_id: int):
    for process in database_process:
        if process.doc_id == doc_id:
            return process


def put_expiration_id(expiration_id: int, doc_id: int):
    for process in database_process:
        if process.doc_id == doc_id:
            process.expiration_id = expiration_id


def delete_expiration_id(doc_id: int):
    for process in database_process:
        if process.doc_id == doc_id:
            process.expiration_id == 0

from pydantic import BaseModel
from datetime import date 
from typing import Dict

class DocumentInDB(BaseModel):
    doc_id: int = 0
    doc_name: str
    doc_send_date: str
    doc_active: bool
    mod_id: int

database_documents = []

database_documents = [DocumentInDB(**{"doc_id": 0,
                        "doc_name": "RUT",
                        "doc_send_date": "2020-12-11",
                        "doc_active": True,
                        "mod_id": 1}), 
                        DocumentInDB(**{"doc_id": 1,
                        "doc_name": "Camara de comercio",
                        "doc_send_date": "2020-10-12",
                        "doc_active": True,
                        "mod_id": 1}),
                        DocumentInDB(**{"doc_id": 2,
                        "doc_name": "Cédula representante legal",
                        "doc_send_date": "2019-10-12",
                        "doc_active": False,
                        "mod_id": 2}),  
]


def insert_doc(document_in_db: DocumentInDB):
    document_in_db.doc_id = len(database_documents)
    database_documents.append(document_in_db)
    return document_in_db

def get_doc(doc_id : int):
    return database_documents[doc_id]

'''def get_doc_byname(doc_name: str):#nueva
    if doc_name in database_documentsN.keys():
        return database_documentsN[doc_name]
    else:
        return None

def update_doc_active(document_in_db: DocumentInDB):#nueva
    database_documentsN[document_in_db.doc_name]=document_in_db
    return document_in_db'''

def get_doc_by_name(doc_name: str):#nueva
    for document in database_documents:
        if document.doc_name == doc_name:
            return document
    return None

def update_doc_active(document_in_db: DocumentInDB):#nueva
    database_documents[document_in_db.doc_id] = document_in_db
    return document_in_db
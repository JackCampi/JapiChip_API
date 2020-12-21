from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db.user_db import get_user, insert_user

from db.document_db import DocumentInDB
from db.document_db import insert_doc, get_doc, get_doc_by_name, update_doc_active

from db.expiration_db import ExpirationInDB, insert_expiration, search_expiration, update_expiration_db

from db.process_db import ProcessInDB
from db.process_db import create_process, get_user_docs_id, search_doc_id, put_expiration_id, delete_expiration_id

from db.module_db import ModuleInDB
from db.module_db import insert_module2, exist_module

from db.company_db import insert_company

from models.document_model import DocumentIn, DocumentActiveOut
from models.expiration_model import ExpirationCreateIn, ExpirationDeleteIn, ExpirationGetIn, ExpirationGetOut, ExpirationUpdateIn
from models.user_model import UserIn
from models.module_model import ModuleIn
from models.company_model import CompanyIn


api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080","http://localhost:8081","https://japichip-app.herokuapp.com/",
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.post('/docs/upload/')
async def update_file_info(doc_info: DocumentIn):
    document = DocumentInDB(**{
        'doc_name': doc_info.doc_name,
        'doc_send_date' : doc_info.doc_send_date,
        'doc_active' : doc_info.doc_active,
        'mod_id': doc_info.mod_id
    })
    document = insert_doc(document)
    for user_email in doc_info.user_emails:
        user_in_db = get_user(user_email)
        if user_in_db == None:
            raise HTTPException(status_code=404,
                                detail=f"El usuario {user_email} no existe")
        
        process = ProcessInDB(**{
            'user_email': user_email,
            'doc_id': document.doc_id,
            'expiration_id':0,
            'proc_ready': True
        })

        create_process(process)
    return {'Document Inserted': True}


@api.get('/docs/{user_email}')
async def get_docs_from_user(user_email: str):
    user_in_db = get_user(user_email)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail=f"El usuario {user_email} no existe")
    
    docs_id = get_user_docs_id(user_email)
    docs = []
    for doc_id, exp_id, proc_ready in docs_id:
        d = dict(**get_doc(doc_id).dict())
        d = dict(d,**search_expiration(exp_id).dict())
        d = dict(d, **{"proc_ready": proc_ready})
        docs.append(d)
    return {
        'item_found': len(docs),
        'items': docs
    }

@api.get('/user/{user_email}')
async def get_username(user_email: str):
    user_in_db = get_user(user_email)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail=f"El usuario {user_email} no existe")
    return {
        'username': user_in_db.user_name
    }

@api.post("/user/auth/")
async def auth_user(user : UserIn):
    user_in_db = get_user(user.user_email)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")
    if user.user_password == user_in_db.user_password:
        return {"Authentication" : True}
    return {"Authentication" : False}


@api.post("/company/modules/create/")
async def create_module(module : ModuleIn):
    if exist_module(module.mod_parent_id):
        module_in_db = ModuleInDB(**{"mod_name": module.mod_name,
                                    "comp_id": module.comp_id,
                                    "mod_parent_id": module.mod_parent_id})
        try:
            insert_module2(module_in_db)
            return {"Created" : True}
        except Exception as e:
            
            raise HTTPException(status_code=404, #Status code isn't 
                            detail=str(e))
    else:
        raise HTTPException(status_code=404,
                            detail="El módulo padre no existe")


@api.post("/new_user/")
async def create_user(user_in: UserIn):
    try:
        insert_user(user_in)
        return {"Created" : True}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail= str(e))


@api.post("/new_company/")
async def create_company(company : CompanyIn):
    try:
        insert_company(company)
        return {"Created" : True}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail= str(e))


@api.get("/docs/active/get{doc_name}")#nueva
async def get_document_active(doc_name: str):
    doc_in_db = get_doc_by_name(doc_name)
    if doc_in_db == None:
        raise HTTPException(status_code=404,detail="El documento no existe get")
    if doc_in_db.doc_active:
        return {"Active": True}
    else:
        return {"Active": False}


@api.put("/docs/active/update")
async def update_doc_active(document_in_db: DocumentInDB):
    doc_in_db = get_doc_by_name(document_in_db.doc_name)
    if doc_in_db == None:
        raise HTTPException(status_code=404,detail="El documento no existe. update")
    if document_in_db.doc_active:
        document_in_db.doc_active=False
        return {"Active": False}
    else:
        document_in_db.doc_active=True
        return {"Active": True}

@api.put("/expiration")
async def put_expiration(expiration_create_in: ExpirationCreateIn):
    periodicity_type = expiration_create_in.exp_periodicity_type
    if periodicity_type == "day" or periodicity_type == "week" or periodicity_type == "month" or periodicity_type == "year":
        process = search_doc_id(expiration_create_in.doc_id)
        if process == None:
            return {"document": "No exist"}

        elif process.expiration_id == 0:
            expiration_in_db = ExpirationInDB(
                **expiration_create_in.dict(), exp_id=0)
            expiration = insert_expiration(expiration_in_db)
            put_expiration_id(expiration.exp_id, expiration_create_in.doc_id)
            return {"process:": True}

        else:
            return {"Expiration": "Exist, no created"}

    else:
        return {"periodicity_type": "day, week, month, year"}


@api.delete("/expiration")
async def delete_expiration(expiration_delete_in: ExpirationDeleteIn):
    doc_id = expiration_delete_in.doc_id
    process = search_doc_id(doc_id)
    if process == None:
        return {"result": "No exist document or expiration"}

    elif process.expiration_id == 0:
        return {"result": "Expiration not exist"}

    else:
        exp_id = process.doc_id
        delete_expiration_id(doc_id)
        delete_expiration(exp_id)
        return {"delete_expiration": "true"}



@api.post("/expiration")
async def get_expiration(expiration_get_in: ExpirationGetIn):
    exp_id = expiration_get_in.exp_id
    expiration = search_expiration(exp_id)
    if expiration == None:
        return {"expiration": "No exist"}
    expiration = ExpirationGetOut(**expiration.dict())
    return expiration


@api.post("/expiration/update")
async def update_expiration(expiration_update_in: ExpirationUpdateIn):
    if update_expiration_db(expiration_update_in):
        return {"expiration": "update"}
    return {"expiration": "No update"}

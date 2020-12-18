from pydantic import BaseModel
from datetime import date


class ExpirationInDB(BaseModel):
    exp_id: int
    exp_date: str
    exp_periodicity: int
    exp_periodicity_type: str


database_expiration = [ExpirationInDB(**{
    "exp_id": 0,
    "exp_date":"12-05-2019",
    "exp_periodicity": 0,
    "exp_periodicity_type": "no exp"  
})]


def insert_expiration(expiration_in_db: ExpirationInDB):
    expiration_in_db.exp_id = len(database_expiration)+1
    database_expiration.append(expiration_in_db)
    return expiration_in_db


def search_expiration(exp_id: int):
    for expiration in database_expiration:
        if expiration.exp_id == exp_id:
            return expiration


def delete_expiration(exp_id: int):
    for expiration in database_expiration:
        if expiration.exp_id == exp_id:
            expiration.exp_id = -1


def update_expiration_db(datas):
    for expiration in database_expiration:
        if expiration.exp_id == datas.exp_id:
            expiration = ExpirationInDB(**datas.dict())
            return True
        return False

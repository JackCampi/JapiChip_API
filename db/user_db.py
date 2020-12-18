from pydantic import BaseModel
from datetime import date 
from typing import Dict

class UserInDB(BaseModel):
    user_email: str
    user_name: str
    user_last_name: str
    user_password: str
    user_role: str
    comp_id : int

database_users = Dict[str, UserInDB]

database_users = {
    "administrador@lacomercializadora.com": UserInDB(**{"user_email": "administrador@lacomercializadora.com",
                            "user_name":"Ricardo",
                            "user_last_name": "Jaramillo",
                            "user_password": "321",
                            "user_role" : "administrador",
                            "comp_id": 900354115
                            }),

    "asistente@lacomercializadora.com": UserInDB(**{"user_email": "asistente@lacomercializadora.com",
                            "user_name":"Rosa",
                            "user_last_name": "Gonzalez",
                            "user_password": "321",
                            "user_role" : "asistente",
                            "comp_id": 900354115
                            }),

    "admin@contadorasunalenas.com": UserInDB(**{"user_email": "admin@contadorasunalenas.com",
                            "user_name":"Andrea",
                            "user_last_name": "Torres",
                            "user_password": "admin",
                            "user_role" : "administrador",
                            "comp_id": 900354120
                            }),
}

def insert_user(user:UserInDB):
    if user.user_email in database_users.keys():
        raise Exception("User already exists")
    else:
        database_users[user.user_email] = user

def get_user(user_email: str):
    if user_email in database_users.keys():
        return database_users[user_email]
    else:
        return None

def update_user(user_in_db: UserInDB):
    database_users[user_in_db.user_email] = user_in_db
    return user_in_db
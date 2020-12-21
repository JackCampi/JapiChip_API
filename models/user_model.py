from pydantic import BaseModel

class UserIn(BaseModel):
    user_name: str
    user_last_name: str
    user_email: str
    user_password: str
    user_role: str
    comp_id : int


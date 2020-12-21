from pydantic import BaseModel

class CompanyIn(BaseModel):
    comp_id : int
    comp_id_type : str
    comp_name : str
    comp_type : str
    comp_address : str
    comp_country : str
    comp_city : str
    comp_phone : str
    comp_email : str

        

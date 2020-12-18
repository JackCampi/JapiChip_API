from pydantic import BaseModel
from typing import Dict

class CompanyInDB(BaseModel):
    comp_id : int
    comp_id_type : str
    comp_name : str
    comp_type : str
    comp_address : str
    comp_country : str
    comp_city : str
    comp_phone : str
    comp_email : str

database_companies = Dict[str, CompanyInDB]

database_companies = {
    900354115: CompanyInDB(**{"comp_id":900354115,
                                "comp_id_type":"NIT",
                                "comp_name":"La Comercializadora",
                                "comp_type":"Persona Juridica",
                                "comp_address": "Cr 22 a 190",
                                "comp_country": "Colombia",
                                "comp_city": "Bogotá",
                                "comp_phone": "3206112020",
                                "comp_email": "lacomercializadora@lacomercializadora.com"}),

    900354120: CompanyInDB(**{"comp_id":900354120,
                                "comp_id_type":"NIT",
                                "comp_name":"Contadoras Unaleñas",
                                "comp_type":"Persona Juridica",
                                "comp_address": "Cll 59 23",
                                "comp_country": "Colombia",
                                "comp_city": "Medellín",
                                "comp_phone": "3214829939",
                                "comp_email": "info@contadorasunalenas.com"}),
}

def insert_company(comp:CompanyInDB):
    if comp.comp_id in database_companies.keys():
        raise Exception("Company already exists")
    else:
        database_companies[comp.comp_id] = comp

def get_company(emp_id: int):
    if emp_id in database_companies.keys():
        return database_companies[emp_id]
    else:
        return None


def update_company(empresa_in_db: CompanyInDB):
    database_empresas[empresa_in_db.emp_id] = empresa_in_db
    return empresa_in_db
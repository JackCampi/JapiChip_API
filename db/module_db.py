from pydantic import BaseModel
from datetime import date 
from typing import Dict

class ModuleInDB(BaseModel):
    mod_id : int = 0
    mod_name : str
    comp_id : int
    mod_parent_id : int

database_module = [
    ModuleInDB(**{"mod_id" : 0,
                    "mod_name":"Jurídico",
                    "comp_id": 900354115,
                    "mod_parent_id":0}),
    ModuleInDB(**{"mod_id" : 1,
                    "mod_name":"Contable",
                    "comp_id": 900354115,
                    "mod_parent_id":1}),
    ModuleInDB(**{"mod_id" : 2,
                    "mod_name":"Estados Financieros",
                    "comp_id": 900354115,
                    "mod_parent_id":1}),
    ModuleInDB(**{"mod_id" : 3,
                    "mod_name":"Contratos",
                    "comp_id": 900354115,
                    "mod_parent_id":0}),
    ModuleInDB(**{"mod_id" : 4,
                    "mod_name":"Contable",
                    "comp_id": 900354120,
                    "mod_parent_id":4}),
    ModuleInDB(**{"mod_id" : 5,
                    "mod_name":"Impuestos",
                    "comp_id": 900354120,
                    "mod_parent_id":4}),
    ModuleInDB(**{"mod_id" : 6,
                    "mod_name":"Extractos",
                    "comp_id": 900354120,
                    "mod_parent_id":4}),
]

def insert_module2(module: ModuleInDB):
    parent = database_module[module.mod_parent_id]
    if parent.comp_id == module.comp_id:
        module.mod_id = len(database_module)
        database_module.append(module)
    else:
        raise Exception("Invalid parent")

def exist_module(module_id: int):
    return module_id < len(database_module) and module_id >= 0

def get_module(mod_id: int, comp_id: int):
    if mod_id < len(database_module) and mod_id >= 0:
        module = database_module[mod_id]
        if module.comp_id == comp_id:
            return module
        else:
            return None
    else:
        return None

def update_module(module: ModuleInDB):
    database_module[module.mod_id] = module
    return module
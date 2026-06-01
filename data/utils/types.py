
from typing import Any
from data.models import MODELS


TYPES_MAP = (int,float,str,bool)

__all__ = ("match_schema","string_to_type")

def clean_data(schema_name:str,data:dict[str,str]) -> dict[str,Any]:
    """Convert the rows to python Data and verify the structure

    Args:
        schema_name (str): The schema name of the data

        data (dict[str,str]): The strings-data to convert in python Data

    Returns:
        list[dict[str,Any]]|None: Return the clean data or None
    """
    # Convert the rows to python Data and verify the structure
    schema_structure = MODELS[schema_name]
    cleaned = {}
    for key,value in data.items():
        if key not in schema_structure:
            return print(f"Key {key} not found in schema") or None
        cleaned.update({key:string_to_type(schema_structure[key],value)})
        if not isinstance(cleaned[key],schema_structure[key]):
            return print(f"Type mismatch for key {key} expected {schema_structure[key]} got {type(value)}") or None
    return cleaned

def match_schema(schema:dict[str,type],data:dict[str,str]) -> bool:
    """Verify if your schem match with your data

    Args:
        schem (dict[str,type]): Your schemas imported by schemas.py
        data (dict[str,str]): Your data that you want verify

    Returns:
        bool: If the schem match with the data return True else False
    """
    if schema.keys() != data.keys(): # If the key is not present in the data
        return False
    for key,typ in schema.items():

        if not isinstance(data[key],typ): # If the type of the value data doesn't match with the type structure
           return False
    return True


def string_to_type(typ:type, value:str) -> type|None:
    """Translate a string to a type

    Args:
        typ (type): The type you want translate
        value (str): The string that you want translate

    Returns:
        type|None: The translated string-type or None if the translation is not possible
    """
    if isinstance(value,typ):
        return value
    if typ not in TYPES_MAP: # If not a simple Type
        return print(f"Error: Type {typ} not supported") or None
    if typ == int:
        return int(value) if str(value).isdigit() else print("Error: Invalid integer format") or None
    elif typ == bool:
        if value.lower() in ["true", "false"]: # If a boolean string True or False
            return True if value.lower() == "true" else False
        return print("Error: Invalid boolean format") or None
    elif typ == float:
        return float(value) if value.replace('.', '', 1).isdigit() else print("Error: Invalid float format") or None
    elif typ == str:
        return value
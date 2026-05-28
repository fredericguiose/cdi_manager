
TYPES_MAP = (int,float,str,bool)

def match_schema(schema:dict[str,type],data:dict[str,str]) -> bool:
    """Verify if your schem match with your data

    Args:
        schem (dict[str,type]): Your schemas imported by schemas.py
        data (dict[str,str]): Your data that you want verify

    Returns:
        bool: If the schem match with the data return True else False
    """
    for key,typ in schema.items():
        if key not in data: # If the key is not present in the data
            return False
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
    if typ not in TYPES_MAP: # If not a simple Type
        return
    if typ == int:
        return int(value) if value.isdigit() else print("Error: Invalid integer format") or None
    elif typ == bool:
        if value.lower() in ["true", "false"]: # If a boolean string True or False
            return True if value.lower() == "true" else False
        return
    elif typ == float:
        return float(value) if value.replace('.', '', 1).isdigit() else None
    elif typ == str:
        return value
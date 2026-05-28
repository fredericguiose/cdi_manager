import csv
import pathlib
from typing import Any
from .utils.types import clean_data, match_schema
from .schemas import SCHEMAS

_cache = {}
SCHEMAS_PATH = pathlib.Path.cwd() / "data" / "schemas"

# CRUD Operations :

# Get :
def _get(schema_name:str, query:dict[str,Any]={}, primary_key_value=None, schemas_path=SCHEMAS_PATH) -> list[dict[str,Any]]:
    """Get the records from the database.

    Args:
        schema_name (str): The Schema of the database
        query (dict[str,Any], optional): The query to filter records. Defaults to {}.
        primary_key_value: Value of the primary key to look up. Defaults to None.
        schemas_path: The schemas path folder. Defaults to SCHEMAS_PATH.

    Returns:
        list[dict[str,Any]]: The Records that match with query or primary_key
    """
    with open(pathlib.Path(schemas_path / f"{schema_name.lower()}.csv"), mode='r') as f:
        reader = csv.DictReader(f)
        if primary_key_value is not None:
            rows = _get_with_primary(schema_name, reader, primary_key_value)
        else:
            rows = _get_with_query(query, reader)
        rows = [clean_data(schema_name, row) for row in rows]
        return [r for r in rows if r is not None]


def _get_with_query(query:dict[str,str], reader:csv.DictReader):
    """Get rows from the CSV file that match the given query.

    Args:
        query (dict[str,str]): The query to filter rows
        reader (csv.DictReader): The Reader of DictReader

    Returns:
        list[dict[str,str]]: The rows that match with the query
    """
    return [row for row in reader if all(row.get(key) == str(value) for key, value in query.items())]


def _get_with_primary(schema_name, reader:csv.DictReader, primary_key_value) -> list[dict[str,str]]:
    """Get the rows by primary key.

    Args:
        schema_name (str): The Schema Name of the database
        reader (csv.DictReader): The reader of DictReader
        primary_key_value: The value of the primary key to look up

    Returns:
        list[dict[str,str]]: The list of string-data match by primary key
    """
    primary_key = list(SCHEMAS[schema_name].keys())[0]

    if schema_name not in _cache:
        _cache[schema_name] = {row[primary_key]: row for row in reader}
    result = _cache[schema_name].get(str(primary_key_value))
    return [result] if result is not None else []


# Create :
def _create(schema_name:str, entries:list[dict[str,Any]], schemas_path=SCHEMAS_PATH):
    """Create entries in the database.

    Args:
        schema_name (str): The Schema name of the table to create
        entries (list[dict[str,Any]]): The entries to create
        schemas_path: The schemas path folder. Defaults to SCHEMAS_PATH.
    """
    primary_key = list(SCHEMAS[schema_name].keys())[0]
    with open(pathlib.Path(schemas_path / f"{schema_name.lower()}.csv"), mode='a', newline="") as f:
        writer = csv.DictWriter(f, SCHEMAS[schema_name])
        for entry in entries:
            if _entry_exist(schema_name, entry, schemas_path):
                print(f"db._create: Entry {entry} already exists")
                continue
            if not match_schema(SCHEMAS[schema_name], entry):
                print(f"db._create: Entry {entry} does not match schema")
                continue
            writer.writerow(entry)
            if schema_name in _cache:
                _cache[schema_name][str(entry[primary_key])] = {k: str(v) for k, v in entry.items()}


def _entry_exist(schema_name:str, entry:dict[str,Any], schemas_path=SCHEMAS_PATH) -> bool:
    """Return if the entry exists.

    Args:
        schema_name (str): The schema Name
        entry (dict[str,Any]): The Entry to check

    Returns:
        bool: True if the entry exists, False otherwise
    """
    primary_key = list(SCHEMAS[schema_name].keys())[0]
    primary_value = entry.get(primary_key)
    if primary_value is None:
        return False
    return bool(_get(schema_name, query={primary_key: primary_value}, schemas_path=schemas_path))


# Delete :
def _delete(schema_name, query: dict[str, Any], schemas_path=SCHEMAS_PATH):
    """Delete records matching the query.

    Args:
        schema_name (str): The schema name
        query (dict[str,Any]): The query to select records to delete
        schemas_path: The schemas path folder. Defaults to SCHEMAS_PATH.
    """
    all_rows = _get(schema_name, schemas_path=schemas_path)
    rows_to_delete = _get(schema_name, query=query, schemas_path=schemas_path)
    rows_to_keep = [row for row in all_rows if row not in rows_to_delete]

    with open(pathlib.Path(schemas_path / f"{schema_name.lower()}.csv"), mode='w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMAS[schema_name])
        writer.writeheader()
        writer.writerows(rows_to_keep)

    _cache.pop(schema_name, None)


# Update :
def _update(schema_name, query: dict[str, Any], new_data: dict[str, Any], schemas_path=SCHEMAS_PATH):
    """Update records matching the query.

    Args:
        schema_name (str): The schema name
        query (dict[str,Any]): The query to select records to update
        new_data (dict[str,Any]): The new data to apply
        schemas_path: The schemas path folder. Defaults to SCHEMAS_PATH.
    """
    all_rows = _get(schema_name, schemas_path=schemas_path)
    updated_rows = []

    for row in all_rows:
        if all(row[k] == v for k, v in query.items()):
            updated_rows.append({**row, **new_data})
        else:
            updated_rows.append(row)

    with open(pathlib.Path(schemas_path / f"{schema_name.lower()}.csv"), mode='w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMAS[schema_name])
        writer.writeheader()
        writer.writerows(updated_rows)

    _cache.pop(schema_name, None)


# Schema Factory :

def make_db(schema_name: str, schemas_path=SCHEMAS_PATH):
    """Bind all CRUD operations to a specific schema.

    Args:
        schema_name (str): The schema to bind (e.g. "STUDENTS")
        schemas_path: The schemas path folder. Defaults to SCHEMAS_PATH.

    Returns:
        tuple: (get, create, delete, update) bound to schema_name
    """
    def get(query=None, primary_key_value=None):
        return _get(schema_name, query or {}, primary_key_value, schemas_path)

    def create(entries: list[dict[str, Any]]):
        return _create(schema_name, entries, schemas_path)

    def delete(query: dict[str, Any]):
        return _delete(schema_name, query, schemas_path)

    def update(query: dict[str, Any], new_data: dict[str, Any]):
        return _update(schema_name, query, new_data, schemas_path)

    return get, create, delete, update

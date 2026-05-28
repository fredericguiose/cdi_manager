import pathlib
from data.db import _get, _create, _delete, _update
from tests.data import TESTS_DATA_PATH

TESTS_DB_PATH = TESTS_DATA_PATH / "_schemas_test_db"
TESTS_DB_WRITE_PATH = TESTS_DATA_PATH / "_schemas_test_db_write"

_STUDENTS_INITIAL = "id,first_name,last_name\n1,John,Doe\n2,Jane,Smith\n"
_STUDENTS_EMPTY = "id,first_name,last_name\n"


def _setup_write_db(content: str):
    TESTS_DB_WRITE_PATH.mkdir(exist_ok=True)
    (TESTS_DB_WRITE_PATH / "students.csv").write_text(content, encoding="utf-8")


# --- _get ---

def test_get_all():
    data = _get("STUDENTS", schemas_path=TESTS_DB_PATH)
    assert data == [
        {"id": 1, "first_name": "John", "last_name": "Doe"},
        {"id": 2, "first_name": "Jane", "last_name": "Smith"},
    ]

def test_get_with_query_match():
    data = _get("STUDENTS", query={"first_name": "John"}, schemas_path=TESTS_DB_PATH)
    assert data == [{"id": 1, "first_name": "John", "last_name": "Doe"}]

def test_get_with_query_no_match():
    data = _get("STUDENTS", query={"first_name": "Alice"}, schemas_path=TESTS_DB_PATH)
    assert data == []

def test_get_with_primary_key():
    data = _get("STUDENTS", primary_key_value=1, schemas_path=TESTS_DB_PATH)
    assert data == [{"id": 1, "first_name": "John", "last_name": "Doe"}]

def test_get_with_primary_key_not_found():
    data = _get("STUDENTS", primary_key_value=999, schemas_path=TESTS_DB_PATH)
    assert data == []


# --- _create ---

def test_create_one():
    _setup_write_db(_STUDENTS_EMPTY)
    _create("STUDENTS", [{"id": 1, "first_name": "John", "last_name": "Doe"}], schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert data == [{"id": 1, "first_name": "John", "last_name": "Doe"}]

def test_create_multiple():
    _setup_write_db(_STUDENTS_EMPTY)
    _create("STUDENTS", [
        {"id": 1, "first_name": "John", "last_name": "Doe"},
        {"id": 2, "first_name": "Jane", "last_name": "Smith"},
    ], schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 2

def test_create_duplicate_skipped():
    _setup_write_db(_STUDENTS_INITIAL)
    _create("STUDENTS", [{"id": 1, "first_name": "John", "last_name": "Doe"}], schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 2


# --- _delete ---

def test_delete_by_query():
    _setup_write_db(_STUDENTS_INITIAL)
    _delete("STUDENTS", query={"first_name": "John"}, schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 1
    assert data[0]["first_name"] == "Jane"

def test_delete_no_match():
    _setup_write_db(_STUDENTS_INITIAL)
    _delete("STUDENTS", query={"first_name": "Alice"}, schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 2


# --- _update ---

def test_update_existing():
    _setup_write_db(_STUDENTS_INITIAL)
    _update("STUDENTS", query={"id": 1}, new_data={"first_name": "Johnny"}, schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", query={"first_name": "Johnny"}, schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 1
    assert data[0]["id"] == 1

def test_update_no_match():
    _setup_write_db(_STUDENTS_INITIAL)
    _update("STUDENTS", query={"id": 999}, new_data={"first_name": "Ghost"}, schemas_path=TESTS_DB_WRITE_PATH)
    data = _get("STUDENTS", schemas_path=TESTS_DB_WRITE_PATH)
    assert len(data) == 2


tests = [
    test_get_all,
    test_get_with_query_match,
    test_get_with_query_no_match,
    test_get_with_primary_key,
    test_get_with_primary_key_not_found,
    test_create_one,
    test_create_multiple,
    test_create_duplicate_skipped,
    test_delete_by_query,
    test_delete_no_match,
    test_update_existing,
    test_update_no_match,
]

def run():
    for test in tests:
        test()
        print(f"Test {test.__name__} passed")

from tests.cli._helpers import (
    capture_stdout,
    mock_inputs,
    restore_input,
    csv_backup,
    csv_restore,
    csv_write,
    clear_db_cache,
)
from cli.managers.books import add_book, delete_book

_BOOKS_EMPTY = "isbn,title,author,year_published,status\n"
_BOOKS_ONE = "isbn,title,author,year_published,status\n978-3-16-148410-0,Le Petit Prince,Antoine de Saint-Exupery,1943,True\n"


def test_add_book_success():
    backup = csv_backup("books")
    clear_db_cache()
    try:
        csv_write("books", _BOOKS_EMPTY)
        original = mock_inputs("978-3-16-148410-0", "Le Petit Prince", "Antoine de Saint-Exupery", "1943", "")
        try:
            output, _ = capture_stdout(add_book)
            assert "Le Petit Prince" in output
            assert "[OK]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("books", backup)
        clear_db_cache()


def test_add_book_missing_isbn():
    backup = csv_backup("books")
    clear_db_cache()
    try:
        csv_write("books", _BOOKS_EMPTY)
        original = mock_inputs("", "Titre", "Auteur", "2023", "")
        try:
            output, _ = capture_stdout(add_book)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("books", backup)
        clear_db_cache()


def test_add_book_missing_title():
    backup = csv_backup("books")
    clear_db_cache()
    try:
        csv_write("books", _BOOKS_EMPTY)
        original = mock_inputs("978-0-00-000000-0", "", "Auteur", "2023", "")
        try:
            output, _ = capture_stdout(add_book)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("books", backup)
        clear_db_cache()


def test_delete_book_success():
    backup = csv_backup("books")
    clear_db_cache()
    try:
        csv_write("books", _BOOKS_ONE)
        original = mock_inputs("978-3-16-148410-0", "")
        try:
            output, _ = capture_stdout(delete_book)
            assert "[OK]" in output
            assert "succ" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("books", backup)
        clear_db_cache()


tests = [
    test_add_book_success,
    test_add_book_missing_isbn,
    test_add_book_missing_title,
    test_delete_book_success,
]


def run():
    for test in tests:
        test()
        print(f"Test {test.__name__} passed")

from tests.cli._helpers import (
    capture_stdout,
    mock_inputs,
    restore_input,
    csv_backup,
    csv_restore,
    csv_write,
    clear_db_cache,
)
from cli.managers.loans import add_loan, return_loan

_STUDENTS_ONE = "id,first_name,last_name\n1,Jean,Dupont\n"
_BOOKS_ONE = "isbn,title,author,year_published,status\n2001,Les Miserables,Victor Hugo,1862,True\n"
_BOOKS_ONE_AVAILABLE = "isbn,title,author,year_published,status\n2001,Les Miserables,Victor Hugo,1862,True\n"
_LOANS_EMPTY = "id,student_id,isbn,status\n"
_LOANS_ONE_ACTIVE = "id,student_id,isbn,status\n1,1,2001,False\n"


def test_add_loan_missing_student_id():
    backup_students = csv_backup("students")
    backup_books = csv_backup("books")
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        csv_write("books", _BOOKS_ONE)
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("", "2001", "")
        try:
            output, _ = capture_stdout(add_loan)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        csv_restore("books", backup_books)
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_add_loan_missing_book_isbn():
    backup_students = csv_backup("students")
    backup_books = csv_backup("books")
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        csv_write("books", _BOOKS_ONE)
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("1", "", "")
        try:
            output, _ = capture_stdout(add_loan)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        csv_restore("books", backup_books)
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_return_loan_missing_isbn():
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("", "")
        try:
            output, _ = capture_stdout(return_loan)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_add_loan_success():
    backup_students = csv_backup("students")
    backup_books = csv_backup("books")
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        csv_write("books", _BOOKS_ONE)
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("1", "2001")
        try:
            output, _ = capture_stdout(add_loan)
            assert "[OK]" in output
            assert "Jean" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        csv_restore("books", backup_books)
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_return_loan_success():
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("loans", _LOANS_ONE_ACTIVE)
        original = mock_inputs("2001", "")
        try:
            output, _ = capture_stdout(return_loan)
            assert "[OK]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_return_loan_not_found():
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("999", "")
        try:
            output, _ = capture_stdout(return_loan)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("loans", backup_loans)
        clear_db_cache()


tests = [
    test_add_loan_missing_student_id,
    test_add_loan_missing_book_isbn,
    test_add_loan_success,
    test_return_loan_missing_isbn,
    test_return_loan_success,
    test_return_loan_not_found,
]


def run():
    for test in tests:
        test()
        print(f"Test {test.__name__} passed")

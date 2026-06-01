from tests.cli._helpers import (
    capture_stdout,
    mock_inputs,
    restore_input,
    csv_backup,
    csv_restore,
    csv_write,
    clear_db_cache,
)
from cli.managers.students import add_student, delete_student, verify_student

_STUDENTS_EMPTY = "id,first_name,last_name\n"
_STUDENTS_ONE = "id,first_name,last_name\n1,Jean,Dupont\n"
_BOOKS_ONE = "isbn,title,author,year_published,status\n2001,Les Miserables,Victor Hugo,1862,True\n"
_LOANS_EMPTY = "id,student_id,isbn,status\n"
_LOANS_ONE = "id,student_id,isbn,status\n1,1,2001,False\n"


def test_add_student_success():
    backup_students = csv_backup("students")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_EMPTY)
        original = mock_inputs("Jean", "Dupont", "")
        try:
            output, _ = capture_stdout(add_student)
            assert "[OK]" in output
            assert "Jean" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        clear_db_cache()


def test_add_student_missing_first_name():
    backup_students = csv_backup("students")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_EMPTY)
        original = mock_inputs("", "Dupont", "")
        try:
            output, _ = capture_stdout(add_student)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        clear_db_cache()


def test_add_student_missing_last_name():
    backup_students = csv_backup("students")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_EMPTY)
        original = mock_inputs("Jean", "", "")
        try:
            output, _ = capture_stdout(add_student)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        clear_db_cache()


def test_delete_student_success():
    backup_students = csv_backup("students")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        original = mock_inputs("1", "")
        try:
            output, _ = capture_stdout(delete_student)
            assert "[OK]" in output
            assert "supprim" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        clear_db_cache()


def test_verify_student_no_loans():
    backup_students = csv_backup("students")
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        csv_write("loans", _LOANS_EMPTY)
        original = mock_inputs("1", "")
        try:
            output, _ = capture_stdout(verify_student)
            assert "[ERREUR]" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        csv_restore("loans", backup_loans)
        clear_db_cache()


def test_verify_student_with_loans():
    backup_students = csv_backup("students")
    backup_books = csv_backup("books")
    backup_loans = csv_backup("loans")
    clear_db_cache()
    try:
        csv_write("students", _STUDENTS_ONE)
        csv_write("books", _BOOKS_ONE)
        csv_write("loans", _LOANS_ONE)
        original = mock_inputs("1", "")
        try:
            output, _ = capture_stdout(verify_student)
            assert "Jean" in output
            assert "Les Miserables" in output
        finally:
            restore_input(original)
    finally:
        csv_restore("students", backup_students)
        csv_restore("books", backup_books)
        csv_restore("loans", backup_loans)
        clear_db_cache()


tests = [
    test_add_student_success,
    test_add_student_missing_first_name,
    test_add_student_missing_last_name,
    test_delete_student_success,
    test_verify_student_no_loans,
    test_verify_student_with_loans,
]


def run():
    for test in tests:
        test()
        print(f"Test {test.__name__} passed")

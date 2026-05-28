"""
Define your following data structures for Strict-Type Programming
"""


STUDENTS = {
    "id": int,
    "first_name": str,
    "last_name": str,
}

BOOKS = {
    "isbn": str,
    "title": str,
    "author": str,
    "year_published": int,
    "status": bool,
}

LOANS = {
    "id": int,
    "student_id": int,
    "isbn": str,
    "status": bool,
}
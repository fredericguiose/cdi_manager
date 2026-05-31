"""
Define your following data structures for Strict-Type Programming
Note : The first key it's reserved for the primary key and HE MUST UNIQUE !!!
"""

from data.db import make_db


__all__ = (
    "STUDENTS",
    "BOOKS",
    "LOANS",
    "SCHEMAS"
)

STUDENTS = make_db("STUDENTS")
BOOKS = make_db("BOOKS")
LOANS = make_db("LOANS")

SCHEMAS = {
    "STUDENTS": { "id": int, "first_name": str,"last_name": str,},
    "BOOKS":{"isbn": str, "title": str, "author": str, "year_published": int,"status": bool,},
    "LOANS": {"id": int, "student_id": int, "isbn": str, "status": bool,},
}
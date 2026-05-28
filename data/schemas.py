"""
Define your following data structures for Strict-Type Programming
Note : The first key it's reserved for the primary key and HE MUST UNIQUE !!!
"""

SCHEMAS = {
    "STUDENTS": { "id": int, "first_name": str,"last_name": str,},
    "BOOKS":{"isbn": str, "title": str, "author": str, "year_published": int,"status": bool,},
    "LOANS": {"id": int, "student_id": int, "isbn": str, "status": bool,},
}
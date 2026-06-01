from data.db import make_db

__all__ = (
    "get",
    "create",
    "delete",
    "update",
)

get,create,delete,update = make_db("LOANS")
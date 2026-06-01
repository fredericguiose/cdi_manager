import sys
import io
import builtins
import pathlib
import os

_SCHEMAS_PATH = pathlib.Path.cwd() / "data" / "schemas"

_ORIGINAL_SYSTEM = os.system


def capture_stdout(func, *args, **kwargs):
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        result = func(*args, **kwargs)
        return sys.stdout.getvalue(), result
    finally:
        sys.stdout = old


def mock_inputs(*values):
    it = iter(values)
    original = builtins.input
    def _fake(prompt=""):
        sys.stdout.write(prompt)
        return str(next(it))
    builtins.input = _fake
    return original


def restore_input(original):
    builtins.input = original


def mock_clear():
    os.system = lambda cmd: None
    return _ORIGINAL_SYSTEM


def restore_clear(original):
    os.system = original


def clear_db_cache():
    from data import db
    db._cache.clear()


def csv_backup(name):
    path = _SCHEMAS_PATH / f"{name}.csv"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def csv_restore(name, content):
    path = _SCHEMAS_PATH / f"{name}.csv"
    path.write_text(content, encoding="utf-8")


def csv_write(name, content):
    path = _SCHEMAS_PATH / f"{name}.csv"
    path.write_text(content, encoding="utf-8")

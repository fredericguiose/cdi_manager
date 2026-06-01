from tests.cli._helpers import (
    capture_stdout,
    mock_inputs,
    restore_input,
    mock_clear,
    restore_clear,
)
from cli.utils import display


def test_separator_default():
    output, _ = capture_stdout(display.separator)
    assert output == ("-" * 50 + "\n")


def test_separator_custom():
    output, _ = capture_stdout(display.separator, char="*", length=10)
    assert output == ("*" * 10 + "\n")


def test_separator_zero_length():
    output, _ = capture_stdout(display.separator, length=0)
    assert output == "\n"


def test_success():
    output, _ = capture_stdout(display.success, "Operation reussie")
    assert output == "[OK] Operation reussie\n"


def test_error():
    output, _ = capture_stdout(display.error, "Erreur critique")
    assert output == "[ERREUR] Erreur critique\n"


def test_info():
    output, _ = capture_stdout(display.info, "Information utile")
    assert output == "[INFO] Information utile\n"


def test_title():
    original_clear = mock_clear()
    try:
        output, _ = capture_stdout(display.title, "Mon Titre")
        assert "=" * 50 in output
        assert "Mon Titre" in output
    finally:
        restore_clear(original_clear)


def test_header():
    output, _ = capture_stdout(display.header, "Sous-titre")
    assert "-" * 50 in output
    assert "Sous-titre" in output


def test_table():
    headers = ["Nom", "Age", "Ville"]
    rows = [
        ["Alice", "25", "Paris"],
        ["Bob", "30", "Lyon"],
    ]
    output, _ = capture_stdout(display.table, headers, rows)
    assert "Nom" in output
    assert "Alice" in output
    assert "Bob" in output
    assert "Paris" in output


def test_table_empty_rows():
    headers = ["Colonne A", "Colonne B"]
    rows = []
    output, _ = capture_stdout(display.table, headers, rows)
    assert "Colonne A" in output
    assert "Colonne B" in output


def test_menu_valid_input():
    original = mock_inputs("1")
    try:
        output, _ = capture_stdout(display.menu, "Menu Test", ["Option A", "Option B"])
        assert "1. Option A" in output
        assert "2. Option B" in output
    finally:
        restore_input(original)


def test_menu_invalid_input():
    original = mock_inputs("abc")
    try:
        output, result = capture_stdout(display.menu, "Menu Test", ["Option A"])
        assert result == -1
        assert "Option A" in output
    finally:
        restore_input(original)


def test_pause():
    original = mock_inputs("")
    try:
        output, _ = capture_stdout(display.pause)
        assert "Appuyez" in output
        assert "Entr" in output
    finally:
        restore_input(original)


tests = [
    test_separator_default,
    test_separator_custom,
    test_separator_zero_length,
    test_success,
    test_error,
    test_info,
    test_title,
    test_header,
    test_table,
    test_table_empty_rows,
    test_menu_valid_input,
    test_menu_invalid_input,
    test_pause,
]


def run():
    for test in tests:
        test()
        print(f"Test {test.__name__} passed")

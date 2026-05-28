import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def separator(char: str = '-', length: int = 50):
    print(char * length)


def title(text: str):
    clear()
    separator('=')
    print(f"  {text}")
    separator('=')


def header(text: str):
    separator()
    print(f"  {text}")
    separator()


def success(text: str):
    print(f"[OK] {text}")


def error(text: str):
    print(f"[ERREUR] {text}")


def info(text: str):
    print(f"[INFO] {text}")


def table(headers: list[str], rows: list[list]):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    separator()
    print("  " + "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    separator()
    for row in rows:
        print("  " + "  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))
    separator()


def menu(title_text: str, options: list[str]) -> int:
    title(title_text)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    separator()
    choice = input("Votre choix : ")
    return int(choice) if choice.isdigit() else -1


def pause():
    input("\nAppuyez sur Entrée pour continuer...")

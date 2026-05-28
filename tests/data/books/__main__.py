import pathlib
from tests import run as _run

run = lambda: _run(pathlib.Path(__file__).parent)

if __name__ == "__main__":
    run()

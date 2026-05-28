import pathlib

def run(target:pathlib.Path=pathlib.Path(__file__).parent):
    """Run all tests of a module
    """
    for path in target.iterdir():
        if path.is_file() and path.suffix == ".py" and not path.stem.startswith("_"): # Verify if it's a Python file and if is a test file
            module_name = ".".join(path.relative_to(pathlib.Path.cwd()).with_suffix("").parts) # Transform the path to a module path
            module = __import__(module_name,fromlist=["run"])  # Import the module to run its tests
            module.run()
        elif path.is_dir() and not path.stem.startswith("_"):
            module_name = ".".join((path / "__main__").relative_to(pathlib.Path.cwd()).with_suffix("").parts) # The main file of the module to run its tests
            module = __import__(module_name,fromlist=["run"])
            module.run() # Run the Runner of the module
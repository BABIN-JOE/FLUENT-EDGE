import importlib
import sys

def check_library(lib_name, alias=None):
    """
    Tries to import a library and handles errors if the library is not found.

    :param lib_name: The name of the library to be imported.
    :param alias: Optional alias to assign the library to a different name in the global namespace.
    """
    try:
        # Import the library with an alias if provided, else just import it
        if alias:
            globals()[alias] = importlib.import_module(lib_name)
        else:
            importlib.import_module(lib_name)
        # Print success message if the library is loaded successfully
        print(f"✅ {lib_name} loaded successfully.", flush=True)
    except ImportError as e:
        # Print error message and exit if the library cannot be imported
        print(f"❌ Failed to import {lib_name}. Error: {e}", flush=True)
        sys.exit(1)

def check_model_path(path, description="Model"):
    """
    Checks if the specified path exists and handles errors if not.

    :param path: The path to check.
    :param description: A description for the path (e.g., "Model" or "Data").
    """
    import os
    # Check if the path exists
    if not os.path.exists(path):
        # Print error message and exit if the path is not found
        print(f"❌ {description} not found at '{path}'", flush=True)
        sys.exit(1)
    else:
        # Print success message if the path is found
        print(f"✅ {description} found at '{path}'", flush=True)

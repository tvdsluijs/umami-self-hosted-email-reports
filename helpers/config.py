import json

def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file {file_path} not found. Exiting.")
        exit(1)

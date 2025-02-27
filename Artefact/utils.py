import os
import json

def read_json(filename: str) -> dict:
    filename = f"./Artefact/{filename}"

    if os.path.exists(filename):
        try:
            return json.loads(open(filename, "r").read())
        
        except json.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)
            exit()
    else:
        print(f"JSON file '{filename}' could not be found")
        exit()

def write_json(filename: str, data_str: str) -> None:
    filename = f"./Artefact/{filename}"

    if os.path.exists(filename):
        try:
            data_dump = json.dumps(data_str)
            open(filename, "w").write(data_dump)
            return
        
        except Exception as e:
            print("Unable to write to JSON: ", e)
            exit()
    else:
        print(f"JSON file '{filename}' could not be found")
        exit()

def search_dict(data: dict, key: str, value: str) -> list[dict]:
    return list(filter(lambda x: x[key] == value, data))
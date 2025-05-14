import os
import re
import hashlib

ROOT_PATH = "resources"
EXTENSION = ".txt"

os.makedirs(ROOT_PATH, exist_ok=True)

def get_data(file_name):
    final_file_name = hash_file_name(file_name)
    # READ FILE
    file_path = f"{ROOT_PATH}/{final_file_name}{EXTENSION}"
    if os.path.exists(file_path):
        f = open(file_path, "r")
        data = f.read()
        f.close()
        return data
    else:
        return None

def save_data(data, file_name, mode="a"):
    final_file_name = hash_file_name(file_name)
    # WRITE FILE
    f = open(f"{ROOT_PATH}/{final_file_name}{EXTENSION}", mode)
    f.write(data)
    f.flush()
    f.close()


def hash_file_name(file_name: str) -> str:
    # Encode the file name to bytes
    encoded = file_name.encode('utf-8')
    
    # Hash using SHA256
    hash_object = hashlib.sha256(encoded)
    
    # Return the hex digest (64-character string)
    return hash_object.hexdigest()


def is_valid_filename(filename: str) -> bool:
    # Check for path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return False

    # Reject empty or overly long names
    if not filename or len(filename) > 70:
        return False

    # Match only allowed characters (letters, numbers, underscores, hyphens, and dots)
    if not re.match(r'^[\w\-. ]+$', filename):
        return False

    return True

import re
import os

def sanitize_filename(filename: str) -> str:
    filename = os.path.basename(filename)
    filename = re.sub(r'[^a-zA-Z0-9.\-_]', '_', filename)
    return filename

def get_file_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip('.').lower()
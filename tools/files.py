import os

BASE = "workspace"


def safe(path):
    full = os.path.abspath(os.path.join(BASE, path))
    base = os.path.abspath(BASE)

    if not full.startswith(base):
        raise Exception("Fuera de workspace")

    return full


def read_file(path):
    with open(safe(path), "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    p = safe(path)
    os.makedirs(os.path.dirname(p), exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"OK {path}"
import os

BASE = os.path.abspath(os.path.join(os.getcwd(), "workspace"))
print("WORKSPACE REAL:", os.path.abspath(BASE))
def safe(path):
    # normaliza
    path = path.replace("\\", "/")
    full = os.path.abspath(os.path.join(BASE, path))

    base = BASE

    if not full.startswith(base):
        raise Exception(f"Fuera de workspace: {path}")

    return full


def read_file(path):
    with open(safe(path), "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    p = safe(path)

    os.makedirs(os.path.dirname(p), exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"OK {p}"
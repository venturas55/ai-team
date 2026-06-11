import json
from tools.files import write_file


def apply_dev_output(text: str):

    results = []

    try:
        data = json.loads(text)
    except Exception as e:
        return [f"❌ INVALID JSON: {str(e)}"]

    if "files" not in data:
        return ["❌ Missing 'files' key"]

    for file in data["files"]:

        path = file.get("path", "").strip()
        content = file.get("content", "")

        if not path or len(path) < 2:
            results.append(f"⚠️ Invalid path: {path}")
            continue

        if content is None:
            results.append(f"⚠️ Empty content: {path}")
            continue

        results.append(write_file(path, content))

    return results
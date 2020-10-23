import json
import os


def load_responses(root_dir, language):
    file_path = os.path.join(root_dir, "gitlab", "data", f"{language}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path) as f:
        return json.load(f)

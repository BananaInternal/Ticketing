import os

GITLAB_URL = os.environ.get("CHATBOX_GITLAB_URL", None)
GITLAB_TOKEN = os.environ.get("CHATBOX_GITLAB_TOKEN", None)
GITLAB_PROJECT = os.environ.get("CHATBOX_GITLAB_PROJECT", "0")

print(f"Config: [url: {GITLAB_URL}, token: {GITLAB_TOKEN}, proj: {GITLAB_PROJECT}]")

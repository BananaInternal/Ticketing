import os

GITLAB_URL = os.environ.get("CHATBOX_GITLAB_URL", None)
GITLAB_TOKEN = os.environ.get("CHATBOX_GITLAB_TOKEN", None)
GITLAB_MAIN_PROJECT = os.environ.get("CHATBOX_GITLAB_MAIN_PROJECT", None)
GITLAB_PROJECTS = os.environ.get("CHATBOX_GITLAB_PROJECTS", "").split(",")

print(f"Config: [url: {GITLAB_URL}, token: {GITLAB_TOKEN}, proj: {GITLAB_PROJECTS}]")

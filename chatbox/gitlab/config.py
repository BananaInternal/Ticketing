import os

GITLAB_URL = os.environ.get("CHATBOX_GITLAB_URL", None)
GITLAB_TOKEN = os.environ.get("CHATBOX_GITLAB_TOKEN", None)
GITLAB_MAIN_PROJECT = os.environ.get("CHATBOX_GITLAB_MAIN_PROJECT", None)
GITLAB_PROJECTS = os.environ.get("CHATBOX_GITLAB_PROJECTS", "").split(",")
CLOSE_ON_REPLY = os.environ.get("CHATBOX_CLOSE_ON_REPLY", False)

print(f"Config: [url: {GITLAB_URL}, token: {GITLAB_TOKEN}, " +
      f"proj: {GITLAB_PROJECTS}, closeOnReply: {CLOSE_ON_REPLY}]")

import os

GITLAB_URL = os.environ.get("CHATBOX_GITLAB_URL", None)
GITLAB_TOKEN = os.environ.get("CHATBOX_GITLAB_TOKEN", None)
GITLAB_PROJECT = os.environ.get("CHATBOX_GITLAB_PROJECT", "0")
CLOSE_ON_REPLY = os.environ.get("CHATBOX_CLOSE_ON_REPLY", False)

print(f"Config: [url: {GITLAB_URL}, token: {GITLAB_TOKEN}, " \
      f"proj: {GITLAB_PROJECT}, closeOnReply: {CLOSE_ON_REPLY}]")

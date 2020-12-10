import json
import os.path as path
import re
import requests
import time
from gitlab import config
from gitlab.replies import load_responses
from nlp.labeler import NlpLabeler
from nlp import polyglot
from requests.exceptions import ConnectionError

DEBUG = True

headers = {"Private-Token": config.GITLAB_TOKEN}
root_dir = path.join(
    path.dirname(path.realpath(__file__)),
    path.pardir,
)
nlp_work_dir = path.join(
    root_dir,
    "nlp",
    "data"
)
nlp_labeler = NlpLabeler(nlp_work_dir)
inbox_map_path = path.join(
    root_dir,
    "gitlab",
    "data",
    "inbox_map.json"
)
with open(inbox_map_path, "r") as inbox_map_file:
    inbox_map = json.load(inbox_map_file)
    print(inbox_map)


def post_reply(project, iid, reply):
    if len(reply) == 0:
        return

    url = f"{config.GITLAB_URL}/api/v4/projects/{project}/issues/{iid}/notes"
    if DEBUG:
        print(f"Posting reply to issue {iid}: {reply}")
        print(f"\tUrl {url}")

    res = requests.post(url,
                        headers=headers,
                        json={"body": reply})
    if res.status_code != 201:
        print(f"Failed to reply: {res.json()}")


def set_labels(project, iid, labels):
    url = f"{config.GITLAB_URL}/api/v4/projects/{project}/issues/{iid}" \
          f"?add_labels={','.join(labels)}"
    if DEBUG:
        print(f"Editing issue {iid}")
        print(f"\tUrl {url}")

    res = requests.put(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to edit issue: {res.json()}")


def close_ticket(project, iid):
    url = f"{config.GITLAB_URL}/api/v4/projects/{project}/issues/{iid}"
    edits = {"state_event": "close"}
    if DEBUG:
        print(f"Closing issue {iid} - {url}")

    res = requests.put(url,
                       headers=headers,
                       json=edits)
    if res.status_code != 200:
        print(f"Failed to close: {res.json()}")


def move_ticket(from_project, to_project, iid):
    url = f"{config.GITLAB_URL}/api/v4/projects/{from_project}/issues/{iid}/move"
    edits = {"to_project_id": to_project}
    res = requests.post(url,
                        headers=headers,
                        json=edits)
    if res.status_code >= 400:
        print(f"Failed to move: {res.json()}")
    return res.json()


def process_new(project):
    if DEBUG:
        print("Processing new issues")

    # vedi Gitlab issue api
    # https://docs.gitlab.com/ee/api/issues.html
    print(f"Processing new issues in project {project}")
    url = f"{config.GITLAB_URL}/api/v4/projects/{project}/issues?" \
          f"state=opened&labels=None"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch issues: {res.json()}")
        return

    # Check if we have to move it
    to_move = project in inbox_map

    for issue in res.json():
        print(f"New issue: {issue['web_url']}")
        iid = issue["iid"]
        labels, reply = analyze(issue["description"])
        if DEBUG:
            print(f"\tlabels: {labels}, reply: {reply}, to_move: {to_move}")
        if to_move:
            labels.add(inbox_map[project])
            issue = move_ticket(project, config.GITLAB_MAIN_PROJECT, iid)

        # Reload iid / project id in case it changed
        iid = issue["iid"]
        issue_proj = issue["project_id"]

        if len(labels) != 0:
            set_labels(issue_proj, iid, labels)
        if reply:
            post_reply(issue_proj, iid, reply)
            if config.CLOSE_ON_REPLY:
                close_ticket(issue_proj, iid)


def analyze(text):
    """
    Analyze the text for:
    - language labeling
    - automated response

    :param text:
    :return:
    """
    labels = set()
    labels.add("ok")  # This issue has been processed

    text = re.sub("<!--.*?-->", "", text, flags=re.DOTALL)
    text = text.replace("\n", " ")
    language = polyglot.get_language(text)
    if language is None:
        return labels, None

    labels.add(language)
    replies_data = load_responses(root_dir, language)
    replies = []

    nlp_labels = nlp_labeler.label(text, language)
    for nlp_label in nlp_labels:
        reply_part = replies_data[nlp_label]
        if reply_part is not None:
            replies.append(reply_part)
            labels.add(nlp_label)

    if len(replies) == 0:
        reply = None
    else:
        reply = "{}\n{}\n{}".format(replies_data["__begin"],
                                    "\n\n".join(replies),
                                    replies_data["__end"])
    return labels, reply


def start():
    while True:
        try:
            for project in config.GITLAB_PROJECTS:
                process_new(project)
        except ConnectionError:
            print(f"Failed to reach {config.GITLAB_URL}, trying again in 2 minutes...")
        time.sleep(60 * 2)

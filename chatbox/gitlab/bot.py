import json
import os.path as path
import re
import requests
from gitlab import config
from nlp.labeler import NlpLabeler
from nlp import polyglot
from requests.exceptions import ConnectionError

DEBUG = False

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
    if DEBUG:
        print(inbox_map)


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

    # Gitlab issue api
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
        labels = analyze(issue["title"], issue["description"])
        if DEBUG:
            print(f"\tlabels: {labels}, to_move: {to_move}")
        if to_move:
            labels.add(inbox_map[project])
            issue = move_ticket(project, config.GITLAB_MAIN_PROJECT, iid)

        # Reload iid / project id in case it changed when moving
        iid = issue["iid"]
        issue_proj = issue["project_id"]

        if len(labels) != 0:
            set_labels(issue_proj, iid, labels)


def analyze(title, text):
    """
    Analyze the text for:
    - language labeling
    - automated response

    :param title:
    :param text:
    :return:
    """
    is_from_form = re.match("^Service Desk \(from .+@.+\): contact2_*", title)
    if is_from_form:
        return analyze_form(title, text)
    else:
        return analyze_mail(text)


def analyze_form(title, text):
    labels = set()
    labels.add("ok")  # This issue has been processed
    labels.add("form")

    title_data = re.sub("^Service Desk \(from .+@.+\): contact2_",
                        "", title).split("_")

    language = None
    topic = None
    if len(title_data) == 2:
        language = title_data[0]
        topic = title_data[1].lower()
    if language is None:
        return labels
    else:
        labels.add(language)
    if topic is not None:
        labels.add(topic)

    text = re.sub("<!--.*?-->", "", text, flags=re.DOTALL)
    text = text.replace("\n", " ")
    labels.update(nlp_labeler.label(text, language))
    return labels


def analyze_mail(text):
    labels = set()
    labels.add("ok")  # This issue has been processed
    labels.add("mail")

    text = re.sub("<!--.*?-->", "", text, flags=re.DOTALL)
    text = text.replace("\n", " ")
    language = polyglot.get_language(text)
    if language is None:
        return labels

    labels.add(language)
    labels.update(nlp_labeler.label(text, language))
    return labels


def start():
    try:
        for project in config.GITLAB_PROJECTS:
            process_new(project)
    except ConnectionError:
        print(f"Failed to reach {config.GITLAB_URL}")

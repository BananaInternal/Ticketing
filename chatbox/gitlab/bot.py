import requests
import os.path as path
import re
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


def post_reply(iid, reply):
    url = f"{config.GITLAB_URL}/api/v4/projects/{config.GITLAB_PROJECT}/issues/{iid}/notes"
    if DEBUG:
        print(f"Posting reply to issue {iid}: {reply}")
        print(f"\tUrl {url}")

    res = requests.post(url,
                        headers=headers,
                        json={"body": reply})
    if res.status_code != 201:
        print(f"Failed to reply: {res.json()}")


def set_labels(iid, labels):
    url = f"{config.GITLAB_URL}/api/v4/projects/{config.GITLAB_PROJECT}/issues/{iid}" \
          f"?add_labels={','.join(labels)}"
    if DEBUG:
        print(f"Editing issue {iid}")
        print(f"\tUrl {url}")

    res = requests.put(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to edit issue: {res.json()}")


def process_new():
    if DEBUG:
        print("Processing new issues")

    url = f"{config.GITLAB_URL}/api/v4/projects/{config.GITLAB_PROJECT}/issues?" \
          f"state=opened&labels=None"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch issues: {res.json()}")
        return
    for issue in res.json():
        print(f"New issue: {issue['web_url']}")
        iid = issue["iid"]
        labels, reply = analyze(issue["description"])
        if DEBUG:
            print(f"\tlabels: {labels}, reply: {reply}")
        if reply:
            post_reply(iid, reply)
        if len(labels) != 0:
            set_labels(iid, labels)


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
            process_new()
        except ConnectionError:
            print(f"Failed to reach {config.GITLAB_URL}, trying again in 2 minutes...")
        time.sleep(60 * 2)

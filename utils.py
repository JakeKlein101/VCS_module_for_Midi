import os
import ctypes
import json


# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""

# Functions:


def handle_commit(commit_message):  # TODO: Research and find a way to make reversable commits.
    global REPO_PATH
    if not os.path.exists(REPO_PATH):  # TODO: Parse the conf file.
        print("repo path" + REPO_PATH)
        print("No repository found.")
    else:
        print("Commit message: ", commit_message)  # create file that contains the metadata for commits


def handle_init(path):
    global REPO_PATH
    conf_json = {}
    if path:
        REPO_PATH = os.path.join(path, ".gitbit")
    else:
        REPO_PATH = os.path.join(os.getcwd(), ".gitbit")

    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
        ctypes.windll.kernel32.SetFileAttributesW(REPO_PATH, FILE_ATTRIBUTE_HIDDEN)

        conf_json["repo_data"] = []
        conf_json["repo_data"].append(
            {'repo_path': REPO_PATH}
        )
        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
    else:
        print("There is already a repository in this working directory.")


def handle_end_repo(args):
    pass  # TODO: deletes the repository and creates a file that will delete the remote origin on push.




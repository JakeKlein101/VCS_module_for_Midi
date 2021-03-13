import os
import ctypes
import json


# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""

# Utility functions:


def conf_parse():
    """
    Used on all occasitons except init. Used to open the configuration file and set up the needed data
    about the repository.
    """
    global REPO_PATH

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)
        REPO_PATH = conf_content["repo_data"]["repo_path"]
        print("path: " + REPO_PATH)

# Argument handlers:


def handle_commit(commit_message):  # TODO: Research and find a way to make reversable commits.
    conf_parse()
    global REPO_PATH
    if not os.path.exists(REPO_PATH):
        print("repo path" + REPO_PATH)
        print("No repository found.")
    else:
        print("Commit message: ", commit_message)  # create file that contains the metadata for commits


def handle_init():
    global REPO_PATH
    conf_json = {}
    REPO_PATH = os.path.join(os.getcwd(), ".gitbit")

    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
        ctypes.windll.kernel32.SetFileAttributesW(REPO_PATH, FILE_ATTRIBUTE_HIDDEN)

        conf_json["repo_data"] = {"repo_path": REPO_PATH}

        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
    else:
        print("There is already a repository in this working directory.")





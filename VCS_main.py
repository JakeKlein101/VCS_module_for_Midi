import os
import ctypes
import json

# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""
COMMIT = 0


# Utility functions:
def find_mid_files():
    """
    Searches for all the .mid files in the current working directory and returns a list of them.
    """
    ret_dict = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mid"):
            ret_dict.append(file.title())
    return ret_dict


def conf_parse():
    """
    Used on all occasitons except init. Used to open the configuration file and set up the needed data
    about the repository.
    """
    global REPO_PATH
    global COMMIT

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)
        REPO_PATH = conf_content["repo_path"]
        COMMIT = conf_content["commit_count"]
        print("commit:", COMMIT)


def conf_update():
    """
    Used on all occasions except init.
    Serves as a closing function to "conf_parse".
    It updates the configuration file with the changes that have been made when the program was executed.
    """
    global REPO_PATH
    global COMMIT

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["commit_count"] += 1

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)


def delete_fifth_last():
    """
    Used to keep commit amount managable. It always keeps the latest 5 commits in the repository for rollback options.
    """
    global COMMIT
    global REPO_PATH

    path_to_delete = os.path.join(REPO_PATH, "commit " + str(COMMIT - 5))
    os.rmdir(path_to_delete)

# Argument handlers:


def handle_commit(commit_message):
    conf_parse()  # Extracts the data from the configuration file into global variables before operation.
    global REPO_PATH
    global COMMIT

    if os.path.exists(REPO_PATH):
        # TODO: enter the current and previous file into the commit system and make comparisons.

        print("Commit message: ", commit_message)
        if COMMIT >= 5:
            delete_fifth_last()

        os.mkdir(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
        COMMIT += 1
        conf_update()  # Updates the configuration file with changes.
    else:
        print("repo path" + REPO_PATH)
        print("No repository found.")


def handle_init():
    global REPO_PATH
    global COMMIT

    conf_json = {}
    REPO_PATH = os.path.join(os.getcwd(), ".gitbit")

    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
        ctypes.windll.kernel32.SetFileAttributesW(REPO_PATH, FILE_ATTRIBUTE_HIDDEN)

        conf_json["repo_path"] = REPO_PATH
        conf_json["commit_count"] = COMMIT
        conf_json["versioned_file_names"] = find_mid_files()

        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
    else:
        print("There is already a repository in this working directory.")

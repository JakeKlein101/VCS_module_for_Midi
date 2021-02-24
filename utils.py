import os
import ctypes

# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""

# Functions:


def handle_commit(commit_message):  # TODO: Research and find a way to make reversable commits.
    if not os.path.exists(REPO_PATH):  # TODO: Make REPO_PATH global.
        print("No repository found.")
    else:
        print("Commit message: ", commit_message)  # create file that contains the metadata for commits


def handle_init(path):
    if path:
        joined_path = os.path.join(path, ".gitbit")
    else:
        joined_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gitbit")
        # TODO: Fix, the path is the path of the file not the cmd.
        print(joined_path)

    if os.path.exists(joined_path):
        os.mkdir(joined_path)
        ctypes.windll.kernel32.SetFileAttributesW(joined_path, FILE_ATTRIBUTE_HIDDEN)
    else:
        print("There is already a repository in this working directory.")




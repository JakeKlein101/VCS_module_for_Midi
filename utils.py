import os


def handle_commit(commit_message):
    print("yessirski:", commit_message)  # create file that contains the metadata for commits


def handle_init(folder_path):
    print(folder_path)
    os.mkdir(os.path.join(folder_path, ".gitbit"))




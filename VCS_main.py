import os
import ctypes
import json
import shutil
import diff_module
import client_class

# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""
COMMIT = 0
VERSIONED_FILE_NAMES = []
REMOTE_AUTH = None
REMOTE_REPO_ID = -1
REMOTE_COMMIT = -1


# Utility functions:

def get_paths_of_files_to_compare():
    """
    gets the paths to the latest commited file and the second to last commited file.
    :return: returns both paths.
    :rtype: str, str
    """
    global REPO_PATH
    global COMMIT
    global VERSIONED_FILE_NAMES

    latest_file_path = os.path.join(REPO_PATH, "commit " + str(COMMIT), VERSIONED_FILE_NAMES[0])
    second_to_last_file_path = os.path.join(REPO_PATH, "commit " + str(COMMIT - 1), VERSIONED_FILE_NAMES[0])

    return latest_file_path, second_to_last_file_path


def copy_midi_file_to_commit_dir():
    """
    Iterates through all the .mid files that were detected and copies the current instances to the commit folder.
    """
    global REPO_PATH
    global COMMIT
    global VERSIONED_FILE_NAMES

    file_name = VERSIONED_FILE_NAMES[0]

    # for file_name in VERSIONED_FILE_NAMES:
    shutil.copyfile(os.path.join(os.getcwd(), file_name),
                    os.path.join(REPO_PATH, "commit " + str(COMMIT), file_name))


def find_midi_files():
    """
    Searches for all the .mid files in the current working directory and returns a list of them.
    :rtype: list
    """
    ret_list = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mid"):
            ret_list.append(file)
    return ret_list


def delete_fifth_last():
    """
    Used to keep commit amount managable. It always keeps the latest 5 commits in the repository for rollback options.
    """
    global COMMIT
    global REPO_PATH

    path_to_delete = os.path.join(REPO_PATH, "commit " + str(COMMIT - 5))
    shutil.rmtree(path_to_delete)


# Configuration file modfication methods:

def conf_parse():
    """
    Used on all occasitons except init. Used to open the configuration file and set up the needed data
    about the repository.
    """
    global REPO_PATH
    global COMMIT
    global VERSIONED_FILE_NAMES
    global REMOTE_AUTH
    global REMOTE_REPO_ID
    global REMOTE_COMMIT

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)
        REPO_PATH = conf_content["repo_path"]
        COMMIT = conf_content["commit_count"]
        VERSIONED_FILE_NAMES = conf_content["versioned_file_names"]
        REMOTE_AUTH = conf_content["remote_auth"]
        REMOTE_REPO_ID = conf_content["remote_repo_id"]
        REMOTE_COMMIT = conf_content["remote_commit"]


def update_remote_auth_status():
    """
    Changes the REMOTE_AUTH status to True after a succesfull authorization with the remote repo.
    """
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["remote_auth"] = True

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)


def modify_commit_counter(num):
    """
    Updates the commit_counter by an amount that is passed in the num argument.
    :param num: the amount to add to the commit counter(can be negative to decrease the commit counter).
    """
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["commit_count"] += num

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)


def set_repo_id(repo_id):
    """
    Sets the remote repository id as the argument given.
    The user has to input the ID only once, and then it will be automatically pulled from the conf.json file.
    :param repo_id: The id of the remote repository.
    """
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["remote_repo_id"] = repo_id

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)


def set_remote_commit(commit_num):
    """
    Sets the remote_commit as the argument given.
    :param commit_num: The number of the latest commit that was pushed.
    """
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["remote_commit"] = commit_num

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)


# Argument handlers:

def handle_commit():
    conf_parse()  # Extracts the data from the configuration file into global variables before operation.
    global REPO_PATH
    global COMMIT

    if os.path.exists(REPO_PATH):
        if COMMIT >= 5:
            delete_fifth_last()

        os.mkdir(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
        copy_midi_file_to_commit_dir()

        if COMMIT > 0:  # The files will only be sent to be checked for diff after more than 1 commit.
            latest_file_path, second_to_last_file_path = get_paths_of_files_to_compare()
            return_code = diff_module.main_diff(latest_file_path, second_to_last_file_path)
            if return_code == 0:
                print("No changes were made.")
                shutil.rmtree(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
                modify_commit_counter(-1)
            else:
                print("Committed succesfully.")
        else:
            print("Committed succesfully.")

        COMMIT += 1
        modify_commit_counter(1)  # Updates the configuration file with changes.
    else:
        print("No repository found.")


def handle_init():
    global REPO_PATH
    global COMMIT

    conf_json = {}
    REPO_PATH = os.path.join(os.getcwd(), ".gitbit")

    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
        ctypes.windll.kernel32.SetFileAttributesW(REPO_PATH, FILE_ATTRIBUTE_HIDDEN)  # Creates a hidden directory.

        conf_json["repo_path"] = REPO_PATH
        conf_json["commit_count"] = COMMIT
        conf_json["versioned_file_names"] = find_midi_files()
        conf_json["remote_auth"] = False
        conf_json["remote_repo_id"] = -1
        conf_json["remote_commit"] = -1

        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
        print("Repository created successfully.")
    else:
        print("There is already a repository in this working directory.")


def handle_delete():
    conf_parse()
    global REPO_PATH

    user_input = input("Are you sure you want to delete the repository? y/n: ").lower()
    if user_input == "y":
        shutil.rmtree(REPO_PATH)
        print("Repo deleted successfully.")
    elif user_input == "n":
        print("Regret isnt always a bad thing :)")
    elif user_input != "y" or user_input != "n":
        print("Enter a valid letter.")


def handle_push():
    global REMOTE_AUTH
    global VERSIONED_FILE_NAMES
    global COMMIT
    global REMOTE_REPO_ID
    global REMOTE_COMMIT
    conf_parse()

    if COMMIT >= 1:
        if COMMIT > REMOTE_COMMIT:
            client = client_class.Client()
            client.start_client()

            if not REMOTE_AUTH:
                if client.auth_user():
                    print("connection authorized")
                    update_remote_auth_status()
                else:
                    print("no auth")

            if int(REMOTE_REPO_ID) > -1:
                client.push_to_remote(VERSIONED_FILE_NAMES[0], REMOTE_REPO_ID)
                set_remote_commit(COMMIT)

            else:
                REMOTE_REPO_ID = input("Enter a repository ID: ")
                set_repo_id(REMOTE_REPO_ID)
                client.push_to_remote(VERSIONED_FILE_NAMES[0], REMOTE_REPO_ID)
                set_remote_commit(COMMIT)

        elif COMMIT == REMOTE_COMMIT:
            print("The latest commit was already pushed.")
        else:  # Should be impossible to get here.
            print("How?")
    else:
        print("No commmits to push.")

import os
import ctypes
import json
import shutil
import diff_module

# consts:

FILE_ATTRIBUTE_HIDDEN = 0x02
REPO_PATH = ""
COMMIT = 0
VERSIONED_FILE_NAMES = []


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

    for file_name in VERSIONED_FILE_NAMES:
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


def conf_parse():
    """
    Used on all occasitons except init. Used to open the configuration file and set up the needed data
    about the repository.
    """
    global REPO_PATH
    global COMMIT
    global VERSIONED_FILE_NAMES

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)
        REPO_PATH = conf_content["repo_path"]
        COMMIT = conf_content["commit_count"]
        VERSIONED_FILE_NAMES = conf_content["versioned_file_names"]


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
    shutil.rmtree(path_to_delete)

# Argument handlers:


def handle_commit(commit_message):
    conf_parse()  # Extracts the data from the configuration file into global variables before operation.
    global REPO_PATH
    global COMMIT

    if os.path.exists(REPO_PATH):
        print("Commit message: ", commit_message)
        if COMMIT >= 5:
            delete_fifth_last()

        os.mkdir(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
        copy_midi_file_to_commit_dir()

        if COMMIT > 0:  # The files will only be sent to be checked for diff after more than 1 commit.
            latest_file_path, second_to_last_file_path = get_paths_of_files_to_compare()
            return_code = diff_module.main_diff(latest_file_path, second_to_last_file_path)
            if return_code == 0:
                shutil.rmtree(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
            elif return_code == 1:
                print("Committed succesfully.")

        COMMIT += 1
        conf_update()  # Updates the configuration file with changes.
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

        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
    else:
        print("There is already a repository in this working directory.")


def handle_delete():
    conf_parse()
    global REPO_PATH

    user_input = input("Are you sure you want to delete the repository? y/n: ")
    if user_input == "y":
        shutil.rmtree(REPO_PATH)
    elif user_input == "n":
        print("Regret isnt always a bad thing :)")
    elif user_input != "y" or user_input != "n":
        print("Enter a valid letter.")


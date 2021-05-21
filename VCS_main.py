import os
import json
import ctypes
import shutil
import diff_module
import client_class
import conf_file_utils  # TODO: Add to project summary.
from clint.textui import colored


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

# Argument handlers:


def handle_init():
    """
    Handles the init opcode. Firstly, it will created a hidden directory named ".gitbit" in the directory that the CMD
    window was opened in. then it will create a JSON file with all the fields needed and will set defaults for them.
    """
    global REPO_PATH
    global COMMIT

    conf_json = {}
    REPO_PATH = os.path.join(os.getcwd(), ".gitbit")

    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
        ctypes.windll.kernel32.SetFileAttributesW(REPO_PATH, FILE_ATTRIBUTE_HIDDEN)  # Creates a hidden directory.

        conf_json["repo_path"] = REPO_PATH
        conf_json["commit_count"] = COMMIT
        conf_json["versioned_file_names"] = []
        conf_json["remote_auth"] = False
        conf_json["remote_repo_id"] = -1
        conf_json["remote_commit"] = -1

        with open(os.path.join(REPO_PATH, "conf.json"), "w") as conf_file:
            json.dump(conf_json, conf_file)
        print("Repository created successfully.")
    else:
        print("There is already a repository in this working directory.")


def handle_add(filename):  # TODO: Add to Project summary.
    global VERSIONED_FILE_NAMES
    conf_parse()

    if filename in find_midi_files():
        VERSIONED_FILE_NAMES.append(filename)
        print(f"{filename} added to version control.")
        conf_file_utils.update_versioned_files_list(VERSIONED_FILE_NAMES)

    else:
        print(f"There is no file named {filename} in working directory.")


def handle_commit():
    """
    Handles the commit opcode. Firstly, it will check if there are 5 commits and will call the helper function
    accordingly. After that it will create a directory for the commit and call the function to copy the file
    to the created dir. If there is more than one commit, it will get the paths to the latest and second latest MIDI
    files that were committed, and will call the main_diff method in diff_module.py.
    """
    global REPO_PATH
    global COMMIT
    global VERSIONED_FILE_NAMES
    conf_parse()  # Extracts the data from the configuration file into global variables before operation.

    if VERSIONED_FILE_NAMES:
        if os.path.exists(REPO_PATH):
            if COMMIT >= 5:
                delete_fifth_last()

            os.mkdir(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
            copy_midi_file_to_commit_dir()  # TODO: Make it work with multiple MIDI files.

            if COMMIT > 0:  # The files will only be sent to be checked for diff after more than 1 commit.
                latest_file_path, second_to_last_file_path = get_paths_of_files_to_compare()
                return_code = diff_module.main_diff(latest_file_path, second_to_last_file_path)
                if return_code == 0:
                    print("No changes were made.")
                    shutil.rmtree(os.path.join(REPO_PATH, "commit " + str(COMMIT)))
                    conf_file_utils.modify_commit_counter(-1)
                else:
                    print("Committed succesfully.")
            else:
                print("Committed succesfully.")

            COMMIT += 1
            conf_file_utils.modify_commit_counter(1)  # Updates the configuration file with changes.
        else:
            print("No repository found.")
    else:
        print("No MIDI files added to repository.")


def handle_push():
    """
    Handles the push opcode. Firstly it will check if there are commits to push using the commit counter from the JSON
    file, after that it will check if there were commits made since the last push, if there are new commits, a new
    client object will be created and started. It will check if the repo is already authenticated with the server,
    if not it will initiate the auth_user() method in the Client object, if the authentication was succesfull,
    the remote auth field will be set as true. After that it will check if there is a repo id in the JSON file,
    if there is one it will use it, otherwise will ask the client, and the initiate the push_to_remote() method
    in the client object.
    """
    global REMOTE_AUTH
    global VERSIONED_FILE_NAMES
    global COMMIT
    global REMOTE_REPO_ID
    global REMOTE_COMMIT
    conf_parse()

    if COMMIT >= 1:
        if COMMIT > REMOTE_COMMIT:
            client = client_class.Client()
            if client.start_client():
                if not REMOTE_AUTH:
                    if client.auth_user():
                        print("Connection authorized")
                        conf_file_utils.update_remote_auth_status(True)
                    else:
                        return

                if int(REMOTE_REPO_ID) > -1:
                    if client.push_to_remote(VERSIONED_FILE_NAMES[0], REMOTE_REPO_ID):
                        conf_file_utils.set_remote_commit(COMMIT)
                        print("Pushed commits successfully.")
                    else:
                        conf_file_utils.update_remote_auth_status(False)

                else:
                    REMOTE_REPO_ID = input("Enter a repository ID: ")
                    conf_file_utils.set_repo_id(REMOTE_REPO_ID)
                    if client.push_to_remote(VERSIONED_FILE_NAMES[0], REMOTE_REPO_ID):
                        conf_file_utils.set_remote_commit(COMMIT)
                        print("Pushed commits successfully.")
                    else:
                        conf_file_utils.update_remote_auth_status(False)
                        conf_file_utils.set_repo_id(-1)

        elif COMMIT == REMOTE_COMMIT:
            print("The latest commit was already pushed.")
    else:
        print("No commmits to push.")


def handle_rollback(rollback_amount):  # TODO: Add to Project summary.
    pass


def handle_delete():
    """
    Handles the delete opcode. Firstly it will ask if the client is sure he wants to delete the repository, if he
    answers yes, then the hidden ".gitbit" directory will be deleted. If he answered no,
    then the deletion will be cancelled.
    """
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


def handle_status():  # TODO: Add to Project summary.
    global REMOTE_AUTH
    global VERSIONED_FILE_NAMES
    global COMMIT
    global REMOTE_REPO_ID
    global REMOTE_COMMIT
    conf_parse()

    print("\nStatus report for gitbit repository. If a field is equal to -1, "
          "it means that it wasnt affected since init.")
    print(f"Authorization with the server: {REMOTE_AUTH}")

    print("\nMIDI files in the working directory:\n")
    for filename in find_midi_files():
        if filename in VERSIONED_FILE_NAMES:
            print(colored.green(f"    -{filename}"))
        else:
            print(colored.red(f"    -{filename}"))

    print(f"\nTotal number of commits: {COMMIT}")
    print(f"Last commit pushed: {REMOTE_COMMIT}")


def handle_preview(filename):  # TODO: Add to Project summary.
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame

    if filename in find_midi_files():
        print("CTRL+C to stop preview.")
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)

        # listen for interruptions
        try:
            # use the midi file you just saved
            clock = pygame.time.Clock()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                clock.tick(30)  # check if playback has finished
        except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            raise SystemExit
    else:
        print(f"The file {filename} doesn't exist in the current working directory.")
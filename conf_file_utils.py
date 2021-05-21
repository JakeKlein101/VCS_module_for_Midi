import os
import json

# Configuration file modfication methods:


def update_remote_auth_status(bool_arg):
    """
    Changes the REMOTE_AUTH status to True after a succesfull authorization with the remote repo.
    """
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["remote_auth"] = bool_arg

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


def update_versioned_files_list(new_list):
    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "r") as conf_file:
        conf_content = json.load(conf_file)

        # The changes to the configuration file are done here:
        conf_content["versioned_file_names"] = new_list

    with open(os.path.join(os.getcwd(), ".gitbit", "conf.json"), "w") as conf_file:
        json.dump(conf_content, conf_file)



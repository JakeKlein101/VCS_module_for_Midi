class RemoteRepoRecieveError(Exception):
    def __str__(self):
        return "the passed content wasnt recieved on the other end."


class RepoDoesntBelongToAccountError(Exception):
    def __str__(self):
        return "This repository doesn't belong to this account."


class UserNotFoundError(Exception):
    def __str__(self):
        return "There is no account with this username."


class FileNotFoundInRemoteRepoError(Exception):  # TODO: Add to Project summary.
    def __str__(self):
        return "The needed files were not found in the remote repository database."


class WrongPasswordError(Exception):
    def __str__(self):
        return "Wrong password."


class RemoteRepoRecieveError(Exception):
    def __str__(self):
        return "the passed content wasnt recieved on the other end."


class RepoDoesntBelongToAccountError(Exception):
    def __str__(self):
        return "This repository doesn't belong to this account."


class UserNotFoundError(Exception):
    def __str__(self):
        return "There is no account with this username."


class WrongPasswordError(Exception):
    def __str__(self):
        return "Wrong password."


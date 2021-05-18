class RemoteRepoRecieveError(Exception):
    def __str__(self):
        return "the passed content wasnt recieved on the other end."


class RepoDoesntBelongToAccountError(Exception):
    def __str__(self):
        return "This repository doesnt belong to the account."

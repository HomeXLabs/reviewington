import json
import os

def recurse_setdefault(res, array, currentPath):
    if len(array) == 0:
        return
    elif len(array) == 1:
        res[(array[0], os.path.join(currentPath, array[0]))] = {}
    else:
        recurse_setdefault(
            res.setdefault((array[0], os.path.join(currentPath, array[0])), {}),
            array[1:],
            os.path.join(currentPath, array[0]),
        )

class RepoFile:
    """Class for formatting and munging the ContentFile Data format.

    An example response for each attribute can be viewed in the "Default
    Response" section of:
    https://docs.github.com/en/rest/reference/repos#get-repository-content
    """

    def __init__(self, pr_comment):
        self.type = pr_comment.type
        self.size = pr_comment.size
        self.path = pr_comment.path
        self.download_url = pr_comment.download_url

    def __str__(self):
        """Returns a string serialized JSON of the RepoFile."""
        return json.dumps(self.__dict__)

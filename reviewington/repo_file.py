import json


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

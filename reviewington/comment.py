import json

from github.PullRequestComment import PullRequestComment


class Comment:
    """Class for formatting and munging the PullRequestComment Data format.

    An example response for each attribute can be viewed in the "Default
    Response" section of:
    https://docs.github.com/en/rest/reference/pulls#list-review-comments-in-a-repository
    """

    def __init__(self, pr_comment: PullRequestComment):
        self.body = pr_comment.body
        self.created_at = pr_comment.created_at.strftime("%B %d, %Y %I:%M %p")
        self.diff_hunk = pr_comment.diff_hunk
        self.html_url = pr_comment.html_url
        self.in_reply_to_id = pr_comment.in_reply_to_id
        self.path = pr_comment.path
        self.pull_request_url = pr_comment.pull_request_url
        self.updated_at = pr_comment.updated_at.strftime("%B %d, %Y %I:%M %p")
        self.user_avatar_url = pr_comment.user.avatar_url
        self.user_html_url = pr_comment.user.html_url
        self.user_login = pr_comment.user.login

    def __str__(self):
        """Returns a string serialized JSON of the comment."""
        return json.dumps(self.to_json())

    def to_json(self):
        return self.__dict__

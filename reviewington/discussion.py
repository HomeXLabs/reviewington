from typing import List
import json
import markdown

from github.PullRequestComment import PullRequestComment

from reviewington.comment import Comment
from reviewington.diff2html import diff2html
from reviewington.tags import normalize_tag


class CommentBody:
    """Class to store the user and body of a PullRequestComment."""

    def __init__(self, comment: Comment):
        self.user_login = comment.user_login
        self.user_html_url = comment.user_html_url
        self.user = {"login": self.user_login, "url": self.user_html_url}
        self.body = markdown.markdown(comment.body, extension=["fenced_code"]).replace(
            "\n", "<br/>"
        )
        self.created_at = comment.created_at
        self.updated_at = comment.updated_at


class Discussion:
    """Class for formatting and munging the PullRequestComment Data format.

    An example response for each attribute can be viewed in the "Default
    Response" section of:
    https://docs.github.com/en/rest/reference/pulls#list-review-comments-in-a-repository
    """

    def __init__(self, comments: List[Comment]):
        self.head_comment = [c for c in comments if c.in_reply_to_id is None][0]
        self.pull_request_url = self.head_comment.pull_request_url
        self.html_url = self.head_comment.html_url
        self.path = self.head_comment.path
        self.tag = normalize_tag(self.head_comment.body.split(":")[0])
        self.diff_hunk = diff2html(self.head_comment.diff_hunk, self.path)
        self.comments = [CommentBody(c) for c in comments]

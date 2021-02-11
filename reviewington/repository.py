import os
from typing import List
from pathlib import Path
from github import Github
from reviewington.comment import Comment
from reviewington.discussion import Discussion

from dotenv import load_dotenv

load_dotenv()


class Repository:
    def __init__(self, repo_id):
        self.github = Github(self.get_github_pat())
        self.repo = self.github.get_repo(repo_id)
        self.name = self.repo.full_name

    def get_github_pat(self):
        home = str(Path.home())
        with open(f"{home}/.reviewington/config") as f:
            credentials_content = f.read()

        key, value = credentials_content.split(":")
        github_pat = value.strip()

        return github_pat

    def get_pr_comments(self) -> List[Comment]:
        pr_comments = self.repo.get_pulls_review_comments()
        return [Comment(c) for c in pr_comments]

    def get_pr_discussions(self) -> List[Discussion]:
        pr_comments = self.get_pr_comments()
        discussions = {}
        for comment in pr_comments:
            if comment.diff_hunk not in discussions:
                discussions[comment.diff_hunk] = [comment]
            else:
                discussions[comment.diff_hunk].append(comment)

        return [Discussion(comments) for comments in discussions.values()]

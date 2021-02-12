import os
from typing import List
from pathlib import Path

from github import Github
from github.GithubException import UnknownObjectException

from reviewington.comment import Comment
from reviewington.discussion import Discussion
from reviewington.repo_file import recurse_setdefault, RepoFile

class Repository:
    def __init__(self, repo_id):
        self.github = Github(self.get_github_pat())
        self.repo = self.get_git_repo(repo_id)
        self.name = self.repo.full_name

    def get_github_pat(self):
        home = str(Path.home())
        try:
            with open(f"{home}/.reviewington/config") as f:
                credentials_content = f.read()
        except IOError:
            return None

        _, value = credentials_content.split(":")
        github_pat = value.strip()

        return github_pat

    def get_git_repo(self, repo_id):
        """Gets github repo object unless Github Personal Access Token doesn't have permissions."""
        try:
            return self.github.get_repo(repo_id)
        except UnknownObjectException as e:
            print(e)
            print("Cannot find Github repo, if it's a private repo check if PAT has permissions.")
            exit(-1)

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

    def get_repo_contents(self):
        filenames = []

        contents = self.repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                filenames.append(RepoFile(file_content))

        return filenames

    def get_repo_filenames(self):
        """Create a tree structure by recursively nesting the filepaths."""
        res = {}
        filenames = [f.path for f in self.get_repo_contents()]
        for f in filenames:
            recurse_setdefault(res, f.split("/"), "/")
        return res

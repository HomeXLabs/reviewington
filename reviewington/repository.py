from typing import List
import os

from github import Github
from reviewington.comment import Comment
from reviewington.discussion import Discussion

from dotenv import load_dotenv

load_dotenv()

# WIP Just using local .env for now
def get_remote_info():
    """Get the org and repo name from git remote origin."""

    org_name = os.getenv("ORG_NAME")
    repo_name = os.getenv("REPO_NAME")
    return f"{org_name}/{repo_name}"


class Repository:
    github = Github(os.getenv("GITHUB_PAT"))

    def __init__(self, repo_id: str):
        self.repo = Repository.github.get_repo(repo_id)
        self.pr_discussions = self.get_pr_discussions()

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


if __name__ == "__main__":
    repo = Repository(get_remote_info())
    for comment in repo.get_pr_comments():
        print(comment)

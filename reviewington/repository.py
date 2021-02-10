import os
from github import Github
from comment import Comment

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

    def __init__(self, repo_id):
        self.repo = Repository.github.get_repo(repo_id)

    def get_pr_comments(self):
        pr_comments = self.repo.get_pulls_review_comments()
        return [Comment(c) for c in pr_comments]


if __name__ == "__main__":
    repo = Repository(get_remote_info())
    for comment in repo.get_pr_comments():
        print(comment)

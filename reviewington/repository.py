import os
from github import Github
from comment import Comment
from repo_file import RepoFile

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



if __name__ == "__main__":
    repo = Repository(get_remote_info())
    for comment in repo.get_pr_comments():
        print(comment)

    for filename in repo.get_repo_contents():
        print(filename)

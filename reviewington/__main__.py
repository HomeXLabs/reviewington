import os

from github import Github

# import git # This is needed to get remote info locally

from reviewington.comment import Comment

from dotenv import load_dotenv

load_dotenv()

# WIP Just using local .env for now
def get_remote_info():
    """Get the org and repo name from git remote origin."""

    org_name = os.getenv("ORG_NAME")
    repo_name = os.getenv("REPO_NAME")
    return f"{org_name}/{repo_name}"


def get_github_repo():
    GITHUB_PAT = os.getenv("GITHUB_PAT")
    g = Github(GITHUB_PAT)

    repo_id = get_remote_info()
    print(repo_id)
    repo = g.get_repo(repo_id)
    return repo


def main():
    repo = get_github_repo()
    pr_comments = repo.get_pulls_review_comments()

    for comment in pr_comments:
        print(Comment(comment))


if __name__ == "__main__":
    main()

import os
import subprocess

from pathlib import Path
from distutils.dir_util import copy_tree


def setup_github_token():
    github_token = input("Please Enter Github Token:")

    home_dir = str(Path.home())

    config_dir = os.path.join(home_dir, ".reviewington")
    config_path = os.path.join(config_dir, "config")

    if not os.path.exists(config_dir):
        subprocess.run(["mkdir", config_dir])


    with open(config_path, "w") as f:
        f.write(f"GITHUB TOKEN: {github_token}" + "\n")


def setup_github_action():

    if not os.path.exists("github_template_files"):
        subprocess.run(["mkdir", "github_template_files"])
        copy_tree("reviewington/github_templates", "github_template_files")


if __name__ == "__main__":
    setup_github_token()
    setup_github_action()

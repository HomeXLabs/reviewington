import os
import subprocess

from pathlib import Path


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
    template_dir_name = "github_action_template"
    template_user_dir = ".github/workflows"
    action_file_name = "review_checker.yml"

    current_dir, current_filename = os.path.split(__file__)

    action_file_path = os.path.join(
        current_dir, template_dir_name, action_file_name
    )  # this is the path inside package
    action_file_path_dst = os.path.join(
        template_user_dir, action_file_name
    )  # this is user's local path

    user_action = input(
        "Press y to create github action file inside your project main directory. This action will create or add template file to .github/workflows directory: \n"
    )

    if user_action == "y":
        if not os.path.exists(".github"):
            subprocess.run(["mkdir", ".github"])
            subprocess.run(["mkdir", template_user_dir])
            subprocess.run(["cp", action_file_path, action_file_path_dst])
            return

        subprocess.run(["cp", action_file_path, action_file_path_dst])
    else:
        print("Skipping action file generation...")
        return


if __name__ == "__main__":
    setup_github_token()
    setup_github_action()

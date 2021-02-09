import os
import subprocess

from pathlib import Path


github_token = input("Please Enter Github Token:")

home_dir = str(Path.home())

config_dir = os.path.join(home_dir, ".reviewington")
config_path = os.path.join(config_dir, "config")

if not os.path.exists(config_dir):
    subprocess.run(["mkdir", config_dir])


with open(config_path, "w") as f:
    f.write(f"GITHUB TOKEN: {github_token}" + "\n")

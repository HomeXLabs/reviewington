import os


current_dir, current_filename = os.path.split(__file__)
about_path = os.path.join(current_dir, "about.txt")

f = open(about_path, "r")
file_contents = f.read()

print(file_contents)

f.close()

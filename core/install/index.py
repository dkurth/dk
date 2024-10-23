import os
import re
import subprocess
import sys

'''
Code for a dk command can be in its own repo, such as https://github.com/dkurth/dreamhostify.
Running `dk install gh:dkurth/dreamhostify` should clone the repo into the user commands directory.
'''

execution_context = sys.argv[1]
# args with the execution_context stripped out (so args[0] is the first argument)
args = sys.argv[2:]

# This starts in the directory containing this command's code

# Begin main code here

if len(args) == 0:
    print("Pass what you want to install, like `dk install gh:user/repo`")
    sys.exit(1)

location = args[0]

command_name = None
if len(args) > 1:
    command_name = args[1]

if location[:3] == "gh:":
    # the arg is a shortcut to a GitHub repo
    location = location[3:]
    if len(location.split('/')) != 2:
        print("Something is wrong with this repo location. It should look like https://github.com/username/reponame")
        sys.exit(1)
    location = f'https://github.com/{location}'
else:
    print("Unrecognized format for the command location. Pass something like `dk install gh:user/repo`")
    sys.exit(1)

# Now location looks like a valid GitHub repo.
# Clone it into the user commands directory.

# TODO I would like to ask some global dk object for the path to the user directory, rather than hardcode it here.
os.chdir("../../user/")

repo_name = location.split('/')[-1]
if command_name is None:
    command_name = repo_name

if os.path.exists(command_name):
    print(f"The directory {command_name} already exists.")
else:
    try:
        subprocess.run(["git", "clone", location, command_name], check=True)
        print(f"Successfully installed {repo_name} as a dk command.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        sys.exit(1)
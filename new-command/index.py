import os
import re
import sys
import shutil

'''
Set up boilerplate for a new command.
'''

# Ensure the current directory context is this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Begin main code here

# You must provide a command name
if len(sys.argv) == 1:
    print("Please provide a command name: `dk new-command my-command-name`")
    sys.exit()

# Ensure the command does not already exist
command = sys.argv[1]
directories = [name for name in os.listdir('..') if os.path.isdir(f"../{name}")]
if command in directories:
    print(f"{command} already exists!")
    sys.exit(1)

# Create the directory for the command
os.mkdir(f"../{command}")

# Copy the boilerplate Python and description files
shutil.copy(
     os.path.join(script_dir, 'boilerplate.py'),
     os.path.join("..", command, "index.py"),
)

shutil.copy(
     os.path.join(script_dir, 'boilerplate.md'),
     os.path.join("..", command, "description.md")
)

# Update description.md to include the actual command name
with open(os.path.join("..", command, "description.md"), 'r') as fh:
    desc = fh.read()

desc = desc.replace('{command}', command)

with open(os.path.join("..", command, "description.md"), 'w') as fh:
    fh.write(desc)

print(f"'{command}' created successfully!")
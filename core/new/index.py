import os
import re
import sys
import shutil

'''
Set up boilerplate for a new command.
'''

execution_context = sys.argv[1]
args = sys.argv[2:]

# Begin main code here

# You must provide a command name
if len(args) == 0:
    print("Please provide a command name: `dk new-command my-command-name`")
    sys.exit()

# Ensure the command does not already exist
command = args[0]
directories = [name for name in os.listdir('..') if os.path.isdir(f"../{name}")]
if command in directories:
    print(f"{command} already exists!")
    sys.exit(1)

# Create the directory for the command
command_dir = f"../../commands/{command}"
os.mkdir(command_dir)

# Copy the boilerplate Python and description files
script_dir = os.path.dirname(os.path.abspath(__file__))
shutil.copy(
     os.path.join(script_dir, 'boilerplate.py'),
     os.path.join(command_dir, "index.py"),
)

shutil.copy(
     os.path.join(script_dir, 'boilerplate.md'),
     os.path.join(command_dir, "description.md")
)

# Update description.md to include the actual command name
with open(os.path.join(command_dir, "description.md"), 'r') as fh:
    desc = fh.read()

desc = desc.replace('{command}', command)

with open(os.path.join(command_dir, "description.md"), 'w') as fh:
    fh.write(desc)

print(f"'{command}' created successfully!")
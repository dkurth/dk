import os
import sys
import importlib
import importlib.util

# Rules
# Every command starts out in its own directory.
# Every command receives a directory as its first argument (the execution_context).
# This is the directory from which dk was initially run.
# Some commands (like "list") won't use this, but many will.


CORE_COMMMANDS_DIR = "core"
USER_COMMANDS_DIR = "user"

def main():

    # save the directory in which the dk command was run
    execution_context = os.getcwd()

    # the directory containing dk.py
    dk_context = os.path.dirname(os.path.abspath(__file__))

    # parse the command name and list of args (if any)
    if len(sys.argv) == 1:
        # default command
        command = "list"
        args = []
    else:
        command = sys.argv[1]
        # everything after the command is an arg to pass along
        # every command receives the execution directory as its first arg
        args = sys.argv[2:] 

    # check whether the command exists
    os.chdir(dk_context)

    core_commands = [name for name in os.listdir(CORE_COMMMANDS_DIR) if os.path.isdir(os.path.join(CORE_COMMMANDS_DIR, name))]
    user_commands = [name for name in os.listdir(USER_COMMANDS_DIR) if os.path.isdir(os.path.join(USER_COMMANDS_DIR, name))]

    if command in core_commands:
        command_dir = f"{CORE_COMMMANDS_DIR}/{command}"
    elif command in user_commands:
        command_dir = f"{USER_COMMANDS_DIR}/{command}"
    else:
        print("I do not recognize that command. Run `dk list` to see a list of commands.")
        sys.exit(1)

    # move into the command directory 
    os.chdir(command_dir)
    
    # run the command    
    try:
        command_script = "index.py" 
        sys.argv = [command_script, execution_context] + args
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location("index", command_script)
        index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(index)
    except Exception as e:
        print(f"Failed to execute {command}: {e}")
    

if __name__ == "__main__":
    main()
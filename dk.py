import os
import sys
import importlib
import importlib.util

def run_command(command, args):
    try:
        # save the args and working dir before modifying them
        args_orig = sys.argv
        cwd_orig = os.getcwd()

        command_script = "index.py" 
        os.chdir(command)
        sys.argv = [command_script] + args
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location("index", command_script)
        index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(index)
    except Exception as e:
        print(f"Failed to execute {command}: {e}")
    finally:
        # put back the original args, in case it matters
        sys.argv = args_orig
        os.chdir(cwd_orig)

def main():

    print("cwd = ", os.getcwd())

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("cwd = ", os.getcwd())

    if len(sys.argv) == 1:
        command = "list"
    else:
        command = sys.argv[1]
        args = sys.argv[2:] # everything after the command is an arg to pass along

    directories = [name for name in os.listdir('.') if os.path.isdir(name)]

    if command not in directories:
        print("I do not recognize that command. Run `dk list` to see a list of commands.")
        sys.exit(1)
    
    run_command(command, args)

if __name__ == "__main__":
    main()
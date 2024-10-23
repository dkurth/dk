import os
import re
import sys

'''
Each directory under `dk` represents a command that can be run.
Each should contain a description.md with a short and long description of the command.
This code can be run two ways:
    list - print the short description of each command
    list {command} - print the long description of a single command
'''

# TODO define these in {root}/shared and import them. Maybe should go in a config.yml.
CORE_COMMANDS_DIR = 'core'
USER_COMMANDS_DIR = 'user'

def parse_description(root_dir, command):
    '''
    Parse the short and long descriptiong from a command's description.md file.
    '''

    markdown_file = f"../../{root_dir}/{command}/description.md"

    # The lack of a description is not a fireable offense.
    if not os.path.isfile(markdown_file):
        return {
            "short": f"No description.md file found at {markdown_file}, cwd={os.getcwd()}",
            "long":  f"No description.md file found at {markdown_file}, cwd={os.getcwd()}",
        }

    with open(markdown_file, 'r') as file:
        content = file.read()
    
    sections = content.split('# ')
    descriptions = {}

    for section in sections:
        if section.startswith('short'):
            descriptions['short'] = section.split('\n', 1)[1].strip()
        elif section.startswith('long'):
            descriptions['long'] = section.split('\n', 1)[1].strip()
    
    return descriptions


def print_header(header):
    print(f'''
=== {header} ===
''')


def print_table(data, col_width=None):
    '''
    Given tuples of two items each, print them as a left and right column.
    '''
    if col_width is None:
        max_left_len = max(len(left) for left, _ in data)
        col_width = max_left_len + 2

    for left, right in data:
        print(
            "",
            format_output(left.ljust(col_width)), 
            format_output(right.ljust(col_width))
        )


def get_ansi_color(name = None):
    '''
    Look up the ansi codes to wrap text in so it displays with the given color.
    '''
    
    colors = {
        "black":        ["\033[30m", "\033[0m"],
        "red":          ["\033[31m", "\033[0m"],
        "green":        ["\033[32m", "\033[0m"],
        "yellow":       ["\033[33m", "\033[0m"],
        "blue":         ["\033[34m", "\033[0m"],
        "magenta":      ["\033[35m", "\033[0m"],
        "cyan":         ["\033[36m", "\033[0m"],
        "white":        ["\033[37m", "\033[0m"],
        "kelly_green":  ["\033[38;5;82m", "\033[0m"],
        "bright_yellow": ["\033[93m", "\033[0m"],
    }

    if name is None or name not in colors:
        # default
        name = "magenta" 

    return colors[name]


def colorize(text, color):
    '''
    Wrap text in ansi codes to colorize it in the terminal.
    '''
    ansi_codes = get_ansi_color(color)
    return f"{ansi_codes[0]}{text}{ansi_codes[1]}"


def format_output(text):
    # Colorize text in `back ticks`
    backtick_color = "bright_yellow"
    return re.sub(r'`(.*?)`', lambda m: colorize(m.group(1), backtick_color), text)


def print_formatted(text):
    print(format_output(text))


def get_dk_ignore():
    '''
    Directories in the main dk folder that are NOT commands can be specified 
    in a .dkignore file, and they will not show up in the list output.
    '''
    dk_ignore_path = "../.dkignore"
    if os.path.exists(dk_ignore_path):
        with open(dk_ignore_path, "r") as fh:
            ignore_these = [line.strip() for line in fh.readlines()]
        return ignore_these
    return []


# TODO move this to {root}/shared/utils.py
def get_all_commands():
    os.chdir("../..")
    core_commands = [name for name in os.listdir(CORE_COMMANDS_DIR) if os.path.isdir(os.path.join(CORE_COMMANDS_DIR, name))]
    user_commands = [name for name in os.listdir(USER_COMMANDS_DIR) if os.path.isdir(os.path.join(USER_COMMANDS_DIR, name))]
    os.chdir(os.path.join(CORE_COMMANDS_DIR, 'list'))

    directories_to_ignore = get_dk_ignore()

    core_commands = [d for d in core_commands if d not in directories_to_ignore]
    core_commands.sort()

    user_commands = [d for d in user_commands if d not in directories_to_ignore]
    user_commands.sort()

    return {'core': core_commands, 'user': user_commands}


# The list command does not use the execution_context
# execution_context = sys.argv[1]
args = sys.argv[2:]

# special case -- quiet mode, just print out the command names, one per line
if len(args) == 1 and (args[0] == '--quiet' or args[0] == '-q'):
    commands = get_all_commands()
    [print(d) for d in commands['core']]
    [print(d) for d in commands['user']]
elif len(args) == 0:
    # short description
    commands = get_all_commands()
    # print_header("Core Commands")
    output = [(d, parse_description(CORE_COMMANDS_DIR, d)['short']) for d in commands['core']]
    # print_table(output)
    # print_header("User Commands")
    output.extend(
        [(d, parse_description(USER_COMMANDS_DIR, d)['short']) for d in commands['user']]
    )
    print_table(output)
else:
    # long description
    command = args[0]
    commands = get_all_commands()
    if command in commands['core']:
        print_formatted(parse_description(CORE_COMMANDS_DIR, command)['long'])
    elif command in commands['user']:
        print_formatted(parse_description(USER_COMMANDS_DIR, command)['long'])
    else:
        print("Something weird happened.")


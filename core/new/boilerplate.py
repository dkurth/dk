import os
import re
import sys

'''
Notes go here.
'''

execution_context = sys.argv[1]
# args with the execution_context stripped out (so args[0] is the first argument)
args = sys.argv[2:]

# Move into the directory from which the dk command was executed by the user
# (Remove this if you need to start in the directory containing this command's code)
os.chdir(execution_context)

# Begin main code here


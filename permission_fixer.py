#!/usr/bin/env python

"""
permission_fixer.py

A simple recursive loop that takes a set of windows files (no permissions, ack!)
and gives them default permissions.  (Files: 0640, dirs: 0750)
"""

__author__ = "Michael J. Harms"
__date__ = "070622"
__usage__ = "permission_fixer.py file|directory"

import os, sys

def permissionFixer(dir):
    """
    Recursively change permissions of a directory.
    """

    # Get the contents of the directory
    contents = [os.path.join(dir,c) for c in os.listdir(dir)]
   
    # For all files/dirs in directory, fix permissions.  Call new instances of
    # permissionFixer function for directories.
    for c in contents:
        if os.path.isdir(c):
            os.chmod(c,0755)
            permissionFixer(c)
        elif os.path.isfile(c):
            os.chmod(c,0644)
        else:
            pass

def main():
    
    try:
        input = sys.argv[1]
    except IndexError:
        print __usage__
        sys.exit()

    if os.path.isdir(input):
        permissionFixer(input)
    elif os.path.isfile(input):
        os.chmod(input,0644)
    else:
        err = "%s does not exist" % input
        raise IOError(err)

# Call if program is called from command line.
if __name__ == "__main__":
    main()


#!/usr/bin/env python
__description__ = \
"""
Deletes all sub-sub-directories with PATTERN in the name that are inside
input_dir.
"""
__usage__ = "input_dir PATTERN"
__author__ = "Michael J. Harms"
__date__ = "091230"

import os, sys, re, shutil

class DeleteOuttakesError(Exception):
    """
    General error class for this module.
    """

    pass


def main(argv=None):
    """
    Function to parse arguments and do operations.
    """

    # If arguments were not passed to main, grab the command line arguments
    if argv == None:
        argv = sys.argv[1:]

    # Parse arguments
    try:
        input_dir = argv[0]
        pattern = argv[1]
    except IndexError:
        err = __usage__
        raise DeleteOuttakesError(err)

    # Create a list of all directories (but not files) within input_dir
    dir_list = [os.path.join(input_dir,d) for d in os.listdir(input_dir)
                if os.path.isdir(os.path.join(input_dir,d))]
   
    # Create a list of subdirectories of directories in dir_list that
    # contain "pattern" within their name. 
    to_delete = []
    for d in dir_list:
        to_delete.extend([os.path.join(d,x) for x in os.listdir(d)
                          if re.search(pattern,x) != None])

    # Print everything that we are going to delete
    for x in to_delete:
        print x

    if len(to_delete) == 0:
        print "No sub-sub-directories within \"%s\" matched \"%s\"!" % \
            (input_dir,pattern)
        return

    # A somewhat-hacked sanity check with the user
    answer = raw_input("Delete the listed directories? ")
    if answer[0].capitalize() == "Y":
        for x in to_delete:
            shutil.rmtree(x)
    else:
        print "Canceled."
        

# If the script itself was called, run main
if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
fix_lines.py

Fixes stupid "\r" mangling on files I get from some people.
"""

__author__ = "Michael J. Harms"
__date__ = "060521"
__usage__ = "fix_lines.py file_or_dir"

import os, sys

def runConversion(file_input):
    """
    Runs conversion on file_input (either recursively on a directory or on a 
    file).  
    """

    if os.path.isfile(file_input):

        # Read input file
        f = open(file_input,'r')
        input = f.read()
        f.close()
        
        # Convert file
        file_lines = ["%s\n" % l for l in input.split("\r")]
       
        # Write file
        g = open(file_input,'w')
        g.writelines(file_lines)
        g.close()
       
    elif os.path.isdir(file_input):
        # If this is a directory, make a list of all objects in directory and
        # recursively call runConversion.
        file_list = os.listdir(file_input)
        file_list = [os.path.join(file_input,f) for f in file_list]
        for file in file_list:
            runConversion(file)
    else:
        # If something doesn't exist.
        err = "%s does not exist!" % file_input
        raise IOError(err)

def main():
    
    try:
        file_input = sys.argv[1]
    except IndexError:
        print __usage__
        sys.exit()

    runConversion(file_input)


# If called from the command line.
if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
dos_unix.py

Converts DOS-style line endings to UNIX-style line endings.
"""

__author__ = "Michael J. Harms"
__date__ = "060521"
__usage__ = "dos_unix.py file_or_dir"

import os, sys

def convertLines(file_lines):
    """
    Converts DOS-style line endings to UNIX-style line endings.
    """

    # Go through file, looking for errant DOS endings and replacing them with
    # correct endings.  Return list of all lines in file. 
    for line_number, line in enumerate(file_lines):
        try:
            end_index = line.index("\r\n")
        except ValueError:
            continue

        file_lines[line_number] = "%s\n" % line[:end_index]

    return file_lines

def runConversion(file_input):
    """
    Runs conversion on file_input (either recursively on a directory or on a 
    file).  
    """

    if os.path.isfile(file_input):

        # Read input file
        f = open(file_input,'r')
        file_lines = f.readlines()
        f.close()

        # Convert file
        file_lines = convertLines(file_lines) 
       
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

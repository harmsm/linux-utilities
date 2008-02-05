#!/usr/bin/env python
__description__ = \
"""
Combine a set of R-compatible files, re-indexing line counter and adding a 
column for the input file.  All comments and blank lines are removed.  The
program assumes that each data file has a single-line header and a %10i first
column containing line numbers.  
"""
__author__ = "Michael J. Harms"
__date__ = "080205"

import os, sys

def combineFiles(to_combine):
    """
    Combine files in to_combine.
    """

    header = None
    out = []
    for file in to_combine:
   
        f = open(file,'r')
        contents = f.readlines()
        f.close()

        # Remove comments and blank lines
        contents = [l for l in contents if l[0] != "#" and l.strip() != ""] 

        # Deal with header
        if header == None:
            header = contents[0]
            header = "%s%10s%s" % (header[:10],"type",header[10:])
        contents = contents[1:]

        # Grab file name (splitting at "_")
        file_root = file.split("_")[0]
        if file_root == "":
            file_root = file        

        # Remove counter and add file_root to contents
        contents = ["%10s%s" % (file_root,l[10:]) for l in contents]

        out.extend(contents)

    # Add counter and re-append header
    out = ["%10i%s" % (i,l) for i, l in enumerate(out)]
    out.insert(0,header)

    return out 
        

def main():
    """
    If called from command line.
    """

    try:
        to_combine = sys.argv[1:]
    except IndexError:
        print __usage__ 
        sys.exit()

    for file in to_combine:
        if not os.path.isfile(file):
            print "%s does not exist!" % file
            sys.exit()

    out = combineFiles(to_combine)

    print "".join(out)

if __name__ == "__main__":
    main()


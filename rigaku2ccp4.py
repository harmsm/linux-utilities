#!/usr/bin/env python
__description__ = \
"""
rigaku2ccp4.py

Converts a rigaku reflection file into ccp4-readable format.

format:
(i, j, k, I, sigI)
%6i%6i%6i%14.5E%14.5E
"""
__author__ = "Michael J. Harms"
__date__ = "080501"
__usage__ = "rigaku2ccp4.py input_file [num_header_lines]"

import sys

def convertFile(input_file,num_header_lines=10):
    """
    """

    f = open(input_file,'r')
    input_lines = f.readlines()
    f.close()

    header = input_lines[0:num_header_lines]

    reflections = input_lines[num_header_lines:]

    out = ["%6i%6i%6i%14.5E%14.5E\n" % tuple([float(c) for c in l.split()])
           for l in reflections]
    out.insert(0,"".join(header))

    return out 


def main():
    """
    To run it called from command line.
    """   

    try: 
        input_file = sys.argv[1]
    except IndexError:
        print __usage__
        sys.exit()

    try:
        num_header_lines = int(sys.argv[2])
    except (IndexError,ValueError):
        num_header_lines = 10


    out = convertFile(input_file,num_header_lines)

    print "".join(out)

if __name__ == "__main__":
    main()

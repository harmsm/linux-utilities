#!/usr/bin/env python
__description__ = \
"""
    Do diff-style comparison between files, with three modifications.
        1) No order.  This simply counts the number of times that line X occurs
           in each file and makes sure that the number is the same.
        2) Split each line into columns and recombine with a single space
           between each column.  This makes sure the comparision is not screwed
           up by space differences between each column.
        3) If "precision" is specified, it is assumed that every column is a 
           float and the data are rounded to the specified decimal place prior
           to comparision.
"""

__author__ = "Michael J. Harms"
__date__ = "080708"
__usage__ = "unorderedDiff.py file1 file2 [precision]"

import os, sys

def unorderedDiff(f1,f2,precision=None):
    """
    Do diff-style comparison between files, with three modifications.
        1) No order.  This simply counts the number of times that line X occurs
           in each file and makes sure that the number is the same.
        2) Split each line into columns and recombine with a single space
           between each column.  This makes sure the comparision is not screwed
           up by space differences between each column.
        3) If "precision" is specified, it is assumed that every column is a 
           float and the data are rounded to the specified decimal place prior
           to comparision.
    """

    # Split and recombine each line to fix spacing and (if specified) float 
    # precision.
    if precision == None:
        f1 = [len(l.split())*"%s " % tuple(l.split()) for l in f1]
        f2 = [len(l.split())*"%s " % tuple(l.split()) for l in f2]
    else:
        fmt = "%" + (".%iF " % precision) 

        f1 = [len(l.split())*fmt % tuple([float(x) for x in l.split()])
              for l in f1]
           
        f2 = [len(l.split())*fmt % tuple([float(x) for x in l.split()])
              for l in f2]

    # Count the number of instances of each line in each file
    f1_dict = dict([(k,0) for k in f1])
    f2_dict = dict([(k,0) for k in f2])
    for k in f1_dict.keys():
        f1_dict[k] = len([l for l in f1 if l == k])
    for k in f2_dict.keys():
        f2_dict[k] = len([l for l in f2 if l == k])
 
    # Compare contents of f1_dict and f2_dict, keeping track of whether the
    # line is only seen in f1 or f2 or whether it is found more/fewer times in 
    # a particular file.
 
    only_in_f1 = {}
    only_in_f2 = {}
    more_in_f1 = {}
    more_in_f2 = {}
 
    f1_keys = f1_dict.keys()
    for k in f1_keys:
        if not f2_dict.has_key(k):
            only_in_f1[k] = f1_dict[k]
            f1_dict.pop(k)
        else:
            diff = (f1_dict[k] - f2_dict[k])
            if diff > 0:
                more_in_f1[k] = diff
            elif diff < 0:
                more_in_f2[k] = -diff

            f1_dict.pop(k)
            f2_dict.pop(k)

    f2_keys = f2_dict.keys()
    for k in f2_keys:
        if not f1_dict.has_key(k):
            only_in_f2[k] = f2_dict[k]
            f2_dict.pop(k)
        else:
            diff = (f1_dict[k] - f2_dict[k])
            if diff > 0:
                more_in_f1[k] = diff
            elif diff < 0:
                more_in_f2[k] = diff

            f1_dict.pop(k)
            f2_dict.pop(k)
            

    return only_in_f1, only_in_f2, more_in_f1, more_in_f2



def main():
    """
    Function to call if run from command line
    """

    # Parse command line
    try:
        file1_input = sys.argv[1]
        file2_input = sys.argv[2]
    except IndexError:
        sys.stderr.write("%s\n" % __usage__)
        sys.exit()

    try:
        precision = int(sys.argv[3])
    except IndexError:
        precision = None
    except ValueError:
        sys.stderr.write("%s\n" % __usage__)
        sys.exit()

    # Read in files
    if not os.path.isfile(file1_input) or not os.path.isfile(file2_input):
        err = "Both file1 and file2 must exist!\n"
        sys.stderr.write(err)
        sys.exit()

    f = open(file1_input,'r')
    file1 = f.readlines()
    f.close()

    f = open(file2_input,'r')
    file2 = f.readlines()
    f.close()

    # Do comparision
    output = unorderedDiff(file1,file2,precision)
    
    # Print output
    labels = ["only in %s" % file1_input,"only in %s" % file2_input,
              "more in %s" % file1_input,"more in %s" % file2_input]
    for i, x in enumerate(output):
        if len(x) != 0:
            print "%s:" % labels[i]

            for d in x.keys():
                print "  \"%s\", %i times" % (d,x[d])




if __name__ == "__main__":
    main()

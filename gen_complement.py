#!/usr/bin/env python
"""
gen_complement.py

Generates a reversed, complementary primers for all primers in a file.
"""

__author__ = "Michael J. Harms"
__date__ = "060521"
__usage__ = "gen_complement.py primer_file"


import os, sys

def reverseSeq(seq_string):
    """
    Generate reverse complement of a sequence.
    """

    bp_dict = {'A':'T','T':'A','G':'C','C':'G',' ':' '}
    new_seq = [bp_dict[seq_string[i]] for i in range(len(seq_string))]
    new_seq.reverse()

    return "".join(new_seq)


def main():

    # Parse command line
    try:
        primer_file = sys.argv[1]
        primer_out = sys.argv[2]
    except IndexError:
        print __usage__
        sys.exit()

    if not os.path.isfile(primer_file):
        err = "%s does not exist!" % primer_file
        raise IOError(err)

    # Read in primer file
    f = open(primer_file,'r')
    lines = f.readlines()
    f.close()

    # Strip comments and blank lines
    lines = [l for l in lines if l[0] != "#" and l.strip() != ""] 

    # Parse primer file and generate reverse primers
    out = []
    for line_counter, line in enumerate(data):

        # Find primer entries
        if line[0] != ">":
            continue

        # Strip spaces out of spequence
        column = line.split()
        seq = data[line_counter + 1][:-1]
        seq = "".join([ x for x in seq if x != ' '])

        # Write out sequence and reversed sequence
        out.append(4*"%s" % (column[5],'_F\t',seq,'\t\n'))
        out.append(4*"%s" % (column[5],'_R\t',reverseSeq(seq),'\t\n'))

    # Write output file
    print "".join(out)

if __name__ == "__main__":
    main()
    

#!/usr/bin/env python
__description__ = \
"""
Grab all movie files from input_dir and place in output_dir.
"""
__author__ = "Michael J. Harms"
__date__ = "081127"
__usage__ = "grabMovieFiles.py input_dir output_dir"

import os, sys, shutil

EXT_TO_TAKE = [".avi",".mpg","mpeg",".mov",".flv",".wmv"]
EXT_TO_TAKE.extend([x.upper() for x in EXT_TO_TAKE])

def grabMovieFiles(input_dir,output_dir):
    """
    """

    input_dirs = [(d,os.path.join(input_dir,d)) for d in os.listdir(input_dir)]
    input_dirs = [d for d in input_dirs if os.path.isdir(d[1])]

    for d in input_dirs:
        file_list = [(f,os.path.join(d[1],f)) for f in os.listdir(d[1])]
        file_list = [f for f in file_list if os.path.isfile(f[1])]
        ext_list = [f[1][-4:] for f in file_list]

        for i, e in enumerate(ext_list):
            if e in EXT_TO_TAKE:
                file_name = "%s_%s" % (d[0],file_list[i][0])
                output_file = os.path.join(output_dir,file_name)
                print "cp %s %s" % (file_list[i][1],output_file)
                shutil.copy(file_list[i][1],output_file)


def main(argv=None):
    """
    """

    if argv == None:
        argv = sys.argv[1:]

    try:
        input_dir = argv[0]
        output_dir = argv[1]
    except IndexError:
        print __usage__
        sys.exit()

    grabMovieFiles(input_dir,output_dir) 

if __name__ == "__main__":
    main()

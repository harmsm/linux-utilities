#!/usr/bin/env python
"""
md_backup.py

Takes directories containing MD trajectories and copies all files except the 
actual trajectories to a new directory.  Full paths to the trajectories are
placed in the TRAJECTORY_LOCATIONS.txt file.  A summary of all skipped 
trajectories is placed in the top of the output directory.
"""

__author__ = "Michael J. Harms"
__date__ = "071114"
__usage__ = "md_backup.py input_dir output_dir"

import os, sys, shutil,time

TRAJ_OUT = "TRAJECTORY_LOCATIONS.txt"
TRAJ_EXTENSIONS = ["trr","veldcd","dcd","xtc"]
FILE_HEADER = \
"""
This is a back up of a molecular dynamics calculation.  It takes too much space
to store trajectories in duplicate (triplicate, etc.), so all files except the
actual trajectory(s) are preserved here.  It should be possible to recreate the 
trajectory(s) using only the contents of this directory.  This file lists the
location of the original trajectories as of %s.  \n\n"""


def mdBackup(input_dir,root,files,output_root):
    """
    Copy all files in dir to analgous dir in output_root if they do not have
    extensions in TRAJ_EXTENSIONS.  If they do have such an extension, do not
    copy them, but append their names ot the TRAJ_OUT file.  Return the list of
    skipped trajectories.
    """

    # Determine absolute path to new directory and create it
    out_dir = os.path.join(output_root,root)

    # Try to make a directory; if it exists already, continue
    try:
        os.mkdir(out_dir)
    except OSError, (error_code,error_string):
        if error_code == 17:
            pass
        else:
            raise OSError(error_string)

    # Create list of files to copy, excluding any file with .ext ext. or .ext.
    # where ext is in TRAJ_EXTENSIONS
    to_copy = []
    for f in files:
        file_parts = f.split(".")
        if len([x for x in file_parts if x in TRAJ_EXTENSIONS]) == 0:
            to_copy.append(f)
    
    # Create pairs of src, dest to copy and copy
    copy_list = [(os.path.join(root,f),os.path.join(out_dir,f))
                 for f in to_copy]
    for f in copy_list:
        print f[0], "-->", f[1]
        shutil.copy(f[0],f[1])

    # Determine which files are trajectory files and place them in TRAJ_OUT
    trajectory_files = [os.path.join(root,f) for f in files if f not in to_copy]
    if len(trajectory_files) > 0:
        out_file = os.path.join(out_dir,TRAJ_OUT)
        out = open(out_file,'w')
        out.write(FILE_HEADER % time.asctime())
        for f in trajectory_files:
            out.write("%s\n" % f)
        out.close()

    return trajectory_files


def main():
    """
    Function to be called if user calls program from command line.
    """

    # Parse command line
    try:
        input_dir = os.path.abspath(sys.argv[1])
        output_dir = os.path.abspath(sys.argv[2])
    except IndexError:
        print __usage__
        sys.exit()

    # Make sure that input directory exists and is a directory
    if not os.path.isdir(input_dir):
        err = "%s is not a directory!" % input_dir
        raise IOError(err)

    # Make sure that the output directory does not exist
    if os.path.exists(output_dir):
        err = "Output directory cannot exist prior to backup"
        raise IOError(err)
    
    # Set up root directory within output directory
    os.mkdir(output_dir)
    os.chdir(os.path.split(input_dir)[0])

    # Perform recursive copy operation on entire directory
    input_root = os.path.split(input_dir)[-1]
    skipped_trajectories = []
    for root, dirs, files in os.walk(input_root):
        skipped = mdBackup(input_root,root,files,output_dir)
        skipped_trajectories.extend(skipped)

    # Write all skipped trajectories to file
    traj_file = "ALL_%s" % TRAJ_OUT
    out_file = os.path.join(output_dir,traj_file)
    out = open(out_file,"w")
    out.write(FILE_HEADER % time.asctime())
    for t in skipped_trajectories:
        out.write("%s\n" % t)

    if len(skipped_trajectories) == 0:
        out.write("No trajectories were in this directory!\n")

    out.close()


# Run if called from command line
if __name__ == "__main__":
    main()

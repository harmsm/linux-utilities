__description__ = \
"""
PRETTY MUCH A HACK.

Take the output from xmlFlattener.py and create a bash script that will run 
AtomicParsley to edit the meta data in all of the relevant mp4 files.  It also
copies existing mp4 files generated with ripper.sh and puts them in a "final" 
directory with a sane name.
"""

import shutil, sys

f = open(sys.argv[1],'r')
lines = f.readlines()
f.close()

for i, l in enumerate(lines):

    v = "%i" % (i + 1)
    mp4_file = "../msb_%s.mp4" % (v.zfill(2))

    col = [c.strip() for c in l.split(';')]

    s1 = "--title \"%s: %s\"" % (col[1],col[2])
    s2 = "--TVShowName \"%s\"" % (col[1])
    s3 = "--TVEpisode \"%s\"" % (col[2])
    s4 = "--TVSeasonNum \"%s\"" % (col[3])
    s5 = "--TVEpisodeNum \"%s\"" % (col[4])

    jpg_file = "%s.jpg" % (col[0][:-4])
    s6 = "--artwork %s" % jpg_file

    s7 = "--description \"%s\"" % (col[5])
    
    title = col[2].replace(" ","-")
    new_file = "../final/msb_%s-%s_%s.mp4" % (col[3],col[4],title)

    shutil.copy(mp4_file,new_file)

    print "AtomicParsley %s -W %s %s %s %s %s %s %s" % (new_file,s1,s2,s3,s4,
                                                        s5,s6,s7)

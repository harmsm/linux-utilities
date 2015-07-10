#!/usr/bin/env python

import sys, os
import hashlib

def calcFileMd5sum(filename):
    """
    Calculate the md5sum of a file of arbitrary size, returning its hash in
    hex.
    """   

    m = hashlib.md5()

    # Read file in as 128 byte chunks
    with open(filename) as f: m.update(f.read(128))
    
    return m.hexdigest()


def recursiveHashCalc(directory):

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):
        for f in files:
            filename = os.path.join(root,f)
            md5 = calcFileMd5sum(filename)

            print filename, md5
        
        #path = root.split(os.pathsep)
        #print (len(path) - 1) *'---' , os.path.basename(root)       
        #for f in files:
        #    print len(path)*'---', f

recursiveHashCalc(sys.argv[1])

#f = open('file.txt','r')
#lines = f.readlines()
#f.close()

#out_dict = {}
#for l in lines:
#    c = l.split("  ")

#    try:
#        v = out_dict[c[0]]
#        
#        if v.startswith("2013-"):
#            continue
#        elif c[1].startswith("2013-"):
#            out_dict[c[0]] = c[1].strip()
#        else:
#            print "DEATH", v, c[1].strip()

#    except KeyError:
#        out_dict[c[0]] = c[1].strip()

#files_to_keep = out_dict.values()

#for l in lines:
#    f = l.split("  ")[1].strip()
#    
#    if f not in files_to_keep:
#        print f 

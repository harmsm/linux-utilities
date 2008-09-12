#!/usr/bin/env python
__description__ = \
"""
Combine a set of pdf files using pyPdf.
"""
__author__ = "Michael J. Harms"
__date__ = "080911"
__usage__ = "combinePdf.py file1.pdf file2.pdf file3.pdf ..."

import os, sys, time

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    print "pyPdf must be installed to use this script!"
    print "Website: (http://pybrary.net/pyPdf/)"
    sys.exit()


def main():
    """
    """

    # Parse command line
    pdf_files = sys.argv[1:]
    if len(pdf_files) == 0:
        print __usage__
        sys.exit()

    # Make sure there is more than one pdf file
    if len(pdf_files) == 1:
        print "In the spirit of gnu tar, this script cowardly refuses to"
        print "combine one pdf file!"
        sys.exit()

    # Create unique name for output file
    localtime = time.localtime()
    localtime = [str(x) for x in localtime]
    localtime = [x.zfill(2) for x in localtime]
    localtime[0] = localtime[0].zfill(4)
    output_file = "%s-%s-%s_%s-%s-%s.pdf" % tuple(localtime[:6])

    # Combine pdf files in order 
    output = PdfFileWriter()
    for pdf in pdf_files:
        input = PdfFileReader(file(pdf,"rb"))
        num_pages = input.getNumPages()
        for i in range(num_pages):
            output.addPage(input.getPage(i))

    # Write final pdf  
    stream = file(output_file,"wb")
    output.write(stream) 
    stream.close()


if __name__ == "__main__":
    main()



#!/usr/bin/env python
__description__ = \
"""
presentationCreator.py

Takes an input file that has a list of svg files.  Each layer from these svg
files is written out sequentially to pdf files.  (For a three layer svg, this 
would mean layer0.pdf, layer0+layer1.pdf, layer0+layer1+layer2.pdf).  All of 
the pdf files are combined into a single pdf.   Optionally, the input file can
contain specific layers to be written out.
"""
__author__ = "Michael J. Harms"
__date__ = "080826"
__usage__ = "presentationCreator.py input_file output_pdf [summary]"

import os, sys
from subprocess import *

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    print "pyPdf must be installed to use this script!"
    print "Website: (http://pybrary.net/pyPdf/)"
    sys.exit()

class PresentationCreatorError(Exception):
    """
    General error class for this module.
    """

    pass


def readFile(input_file):
    """
    Read file of format:

    directory1 [whitespace delimited list of layers].
    directory2 [whitespace delimited list of layers].
    ...

    If layers are not specified, all layers in the svg file are used 
    sequentially.
    """

    f = open(input_file,'r')
    lines = f.readlines()
    f.close()

    lines = [l for l in lines if l[0] != "#" and l.strip() != ""]

    svg_files = []
    for line in lines:
        # Parse line
        columns = line.split()
        if len(columns) == 0:
            err = "Mangled input! (%s)\n" % line
            raise PresentationCreatorError(err)

        # Grab svg file
        svg = columns[0]
        if not os.path.isfile(svg):
            err = "%s does not exist!\n" % svg
            raise PresentationCreatorError(err)

        # If no layers are specified, just record the svg 
        if len(columns) == 1:
            svg_files.append([svg,None])

        # If layers are specified, record them along with the svg file
        else:
            try:
                layers = [int(c) for c in columns[1:]]
            except ValueError:
                err = "Mangled input! (%s)\n" % line
                raise PresentationCreatorError(err)

            svg_files.append([svg,layers])

    return svg_files

def svg2pdf(svg_file,pdf_file):
    """
    Convert an svg file to a pdf file using inkscape.
    """

    command = "inkscape %s -A %s -T -z" % (svg_file,pdf_file)
    try:
        retcode = call(command, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Terminated by signal", -retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e


def extractLayers(svg_file,layers_to_write=[],summary=False):
    """
    Extract layers from an inkscape svg file and write to pdfs.  The list of 
    pdf files is returned.
    """

    # Read svg file
    if not os.path.isfile(svg_file):
        err = "%s does not exist!" % svg_file
        raise PresentationCreatorError(err)
    f = open(svg_file,'r')
    raw_lines = f.readlines()
    f.close()

    # Go into the directory containing the svg file
    curr_dir = os.getcwd()
    svg_split = os.path.split(svg_file)
    svg_name = svg_split[-1]
    svg_dir = svg_split[0]
    os.chdir(svg_dir)

    # Remove white space so lines are easily parsable
    lines = [l.strip() for l in raw_lines]

    # Find each layer
    layer_key = "inkscape:groupmode=\"layer\""
    key_size = len(layer_key)
    layers = [i for i, l in enumerate(lines) if l[:key_size] == layer_key]

    # Find the display line for this layer
    display_key = "style=\"display:"
    key_size = len(display_key)
    display_lines = []
    for line_number in layers:
        for i in range(line_number,len(lines)):
            if lines[i][:key_size] == display_key:
                display_lines.append(i)
                break

    # If there is only one layer, no display lines will be found.  Nothing else
    # needs to be done, so write out pdf and return.
    if len(display_lines) == 0:
        pdf_file = os.path.join(curr_dir,"presentationCreator_tmp_%i.pdf" % 0)
        svg2pdf(svg_name,pdf_file)
        os.chdir(curr_dir)
        return [pdf_file]

    # Decide which layers to write out
    if summary:
        if layers_to_write == None:
            layers_to_write = [len(display_lines)-1]
        else:
            layers_to_write = [layers_to_write[-1]]
    else:
        if layers_to_write == None:
            layers_to_write = range(len(display_lines)) 
   
    # Turn every layer off
    out_lines = raw_lines[:]
    for line in display_lines:
        split = out_lines[line].split("inline")
        if len(split) == 2:
            out_lines[line] = "%snone%s" % tuple(split)

    # Turn layers on sequentially, writing out to pdf if the layer is in 
    # layers_to_write
    pdf_list = []
    for i, line in enumerate(display_lines):

        # Turn this layer on
        split = out_lines[line].split("none")
        out_lines[line] = "%sinline%s" % tuple(split)

        # If we need to write it
        if i in layers_to_write:
            layers_to_write.remove(i)

            # Dump lines to temporary svg file
            tmp_svg = "presentationCreator_tmp_%i.svg" % line
            g = open(tmp_svg,'w')
            g.writelines(out_lines)
            g.close()

            # Run inkscape to convert to pdf
            pdf_file = os.path.join(curr_dir,
                                    "presentationCreator_tmp_%i.pdf" % line)
            svg2pdf(tmp_svg,pdf_file)
            pdf_list.append(pdf_file)

            # Delete temporary svg file
            os.remove(tmp_svg) 

    # Print out any layers that were not found
    if len(layers_to_write) != 0:
        print "Warning! The following layers were not found in %s:" % svg_file
        print "    %s" % ("".join(["%i " % i for i in layers_to_write])) 

    os.chdir(curr_dir)

    return pdf_list


def main():
    """
    """

    # Parse command line
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print __usage__
        sys.exit()

    summary = False
    try:
        if sys.argv[3][0] == "s":
            summary = True
    except IndexError:
        pass 

    # Get list of pdf files
    svg_files = readFile(input_file)

    # Make sure overwriting the output file is okay
    if os.path.isfile(output_file):
        query = "\"%s\" already exists!  Overwrite [y|n]\n" % output_file 
        answer = raw_input(query).strip()
 
        if answer[0].lower() != "y":
            sys.exit() 
        else:
            os.remove(output_file)
  
    # Combine pdf files in order 
    output = PdfFileWriter()
    for svg in svg_files:
    
        # Some pretty output to the command line
        if svg[1] == None:
            out = "%s, all layers" % svg[0]
        else:
            out = ["%i " % i for i in svg[1]]
            out = "%s, layers %s" % (svg[0],"".join(out))
        print out

        # Extract svg layers to pdf files and append to output pdf
        pdf_files = extractLayers(svg[0],svg[1],summary)
        for pdf in pdf_files:

            input = PdfFileReader(file(pdf,"rb"))
            num_pages = input.getNumPages()
            for i in range(num_pages):
                output.addPage(input.getPage(i))

            os.remove(pdf)
    
    # Write final pdf  
    stream = file(output_file,"wb")
    output.write(stream) 
    stream.close()


if __name__ == "__main__":
    main()



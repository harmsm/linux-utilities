#!/usr/bin/env python
__description__ = \
"""
Grab the data from a particular set of element names and spit out in a simple, 
delimited format.  (If the elements in STUFF_TO_GRAB are nested, it will only 
grab text data from the innermost nesting.)
"""
__author__ = "Michael J. Harms"
__date__ = "121222"
__usage__ = "python xmlFlattener.py dir_with_xml_files"

# a list of xml elements to grab
STUFF_TO_GRAB = ["title","series_name","mpaa"]
DELIMITER = ","

import sys, os
import xml.parsers.expat

class XmlOutput:
    """
    A class that records the contents of an expat.Parse call into a dictionary
    attribute of the class that can then be printed out in pretty format.
    """

    def __init__(self,stuff_to_grab):
        """
        Initialize the class, building a dictionary to store the output
        from keys in stuff_to_grab.
        """

        self.stuff_to_grab = stuff_to_grab[:]
        self.grab_dict = dict([(s,[]) for s in self.stuff_to_grab])
        self.current_key = None

    def start_element(self,name, attrs):
        """
        Handler for start elements.  Recrod the name of the current key that
        we just got to.
        """

        if name in self.grab_dict.keys():
            self.current_key = name
        else:
            self.current_key = None 

    def character_data(self,data):
        """
        Record the character data.
        """

        if self.current_key:
            self.grab_dict[self.current_key].append(data)

    def printOutput(self,delimiter=","):
        """
        Print the contents of the file in a pretty, delimited fashion.
        """

        to_print = []
        for s in self.stuff_to_grab:
            output = self.grab_dict[s]
            output = " ".join(output)
            output = output.strip()
            output = output.replace(" ","_")

            to_print.append(output)
           
        print delimiter.join(to_print) 

def main(argv=None):
    """
    Main function.
    """

    # If no argv is passed, grab it from the command line
    if argv == None:
        argv = sys.argv[1:]

    # Initialize parser

    # parse the arguments   
    try:
        directory = argv[0]
    except IndexError:
        err = "Specify a directory!\n"
        raise IndexError(err)

    # Create a list of xml files in the directory
    file_list = os.listdir(sys.argv[1])
    xml_list = [f for f in file_list if f[-4:] == ".xml"]

    # Print out header line
    print DELIMITER.join(STUFF_TO_GRAB)

    # Go through each xml file...
    for x in xml_list:

        # Create an output object to hold the output
        xml_out = XmlOutput(STUFF_TO_GRAB)

        # Initialize the parser, making the parser use handler functions from 
        # the output class.
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = xml_out.start_element
        p.CharacterDataHandler = xml_out.character_data

        print x

        # Open the file and parse it
        file_handle = open(x,'r')
        p.ParseFile(file_handle)
        file_handle.close()

        # Print the output from the xml file
        xml_out.printOutput(DELIMITER)

# If the program is called from the command line.  (This is useful if you want
# to use the xmlOutput class in a different program.  If you type 
# "import xmlFlattener" in python, it will execute the contents of the script, 
# thus putting the class into the namespace and making it accessible for use.
# If the argument parsing etc. was global, it would also execute.  By putting 
# in this __name__ check, the main function will only execute if xmlFlattener
# is the calling script).
if __name__ == "__main__":
    main()

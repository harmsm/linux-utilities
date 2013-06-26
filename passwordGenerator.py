#!/usr/bin/env python
__description__ = \
"""
Generate a random password of user-specified length.  Uses 52 characters,
10 digits, and 5 punctuation marks (plus any extra characters specified by the
user) to generate a random string of user-specified length.
"""
__date__ = "130626"
__author__ = "Michael J. Harms"
__usage__ = "generatePassword.py password_length [... extra characters ...]"

import string, sys
from random import choice

DEFAULT_PUNC = ".,!_-"

def main(argv=None):
    """
    Main function for generating random passwords.
    """

    # Parse arguments
    if argv == None:
        argv = sys.argv[1:]

    try:
        password_length = int(argv[0])
    except IndexError:
        err = "Incorrect arguments!\n\nUsage:\n\n%s\n\n" % __usage__
        raise IndexError(err)

    try:
        extra_characters = "".join(argv[1:])
        extra_characters = list(extra_characters)
    except IndexError:
        extra_characters = [] 

    # Create a list of possible characters
    characters = list(string.letters)
    characters.extend(list(string.digits))
    characters.extend(list(DEFAULT_PUNC))
    characters.extend(extra_characters)

    # Make each character unique
    characters = dict([(c,[]) for c in characters]).keys()

    # Generate and return a random password
    return "".join([choice(characters) for i in range(password_length)])

# If called from the command line
if __name__ == "__main__":
    print main()

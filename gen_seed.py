#!/usr/bin/env python

"""
gen_seed.py

Spits out a random eight digit integer.
"""

import random

print "%8i" % int(1e8*random.random())

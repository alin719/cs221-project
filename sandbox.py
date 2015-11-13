# Authors: Austin Ray, Bruno De Martino, Alex Lin
# File: sandbox.py
# ----------------
# This file exists so we can play around with different packages.
# As we develop useful functions, we will port groups of similar functions
# from sandbox.py into other package files.
#
# Note: Commenting encouraged so other people can learn from what you've done!

import collections
import numpy, scipy, math
import re

myStr = """1 teaspoon's coarse salt, plus more 
for cooking water. """

correctSplit = [word for word in re.split("([^a-zA-Z0-9_\''])", myStr) if word is not '' and word is not ' ']
print correctSplit

for trigram in zip(correctSplit, correctSplit[1:], correctSplit[2:]):
	print(trigram)

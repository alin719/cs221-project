# Authors: Austin Ray, Bruno De Martino, Alex Lin
# File: sandbox.py
# ----------------
# This file exists so we can play around with different packages.
# As we develop useful functions, we will port groups of similar functions
# from sandbox.py into other package files.
#
# Note: Commenting encouraged so other people can learn from what you've done!

import collections, copy
import numpy, scipy, math
import re

myStr = """1 teaspoon's coarse salt, plus more 
for cooking water. """

correctSplit = [word for word in re.split("([^a-zA-Z0-9_\''])", myStr) if word is not '' and word is not ' ']
print correctSplit

# 'zip()' basically takes the transpose of a matrix
for trigram in zip(correctSplit, correctSplit[1:], correctSplit[2:]):
	print(trigram)


print ""


def myAppend(li, n):
	li.append(n)

def setEqual(li1, li2):
	li1 = li2

def setEqual_dc(li1, li2):
	li1 = copy.deepcopy(li2)

def setEqual_elems(li1, li2):
	li1 = li2[:]

def setEqual_li(lili1, li2):
	lili1[0] = li2

def setEqual_ret(li1, li2):
	return li2

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
print "listA: ", listA, "listB: ", listB, "listC: ", listC

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
myAppend(listA, 2)
setEqual(listB, listC)
print "listA: ", listA, "listB: ", listB, "listC: ", listC

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
myAppend(listA, 3)
setEqual_dc(listB, listC)
print "listA: ", listA, "listB: ", listB, "listC: ", listC

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
myAppend(listA, 20)
setEqual_elems(listB, listC)
print "listA: ", listA, "listB: ", listB, "listC: ", listC

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
myAppend(listA, 40)
liliB = [listB]
setEqual_li(liliB, listC)

listB = liliB[0]
print "listA: ", listA, "listB: ", listB, "listC: ", listC

listA = [0, 1]
listB = [4, 5]
listC = [7, 8]
myAppend(listA, 60)
listB = setEqual_ret(listB, listC)
print "listA: ", listA, "listB: ", listB, "listC: ", listC

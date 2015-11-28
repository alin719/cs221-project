# Authors: Austin Ray, Bruno De Martino, Alex Lin
# File: sandbox.py
# ----------------
# This file exists so we can play around with different packages.
# As we develop useful functions, we will port groups of similar functions
# from sandbox.py into other package files.
#
# Note: Commenting encouraged so other people can learn from what you've done!

import collections, itertools, copy
import numpy, scipy, math
import re

def test_makeTrigrams():
	myStr = """1 teaspoon's coarse salt, plus more 
	for cooking water. """

	correctSplit = [word for word in re.split("([^a-zA-Z0-9_\''])", myStr) if word is not '' and word is not ' ']
	print correctSplit

	# 'zip()' basically takes the transpose of a matrix
	for trigram in zip(correctSplit, correctSplit[1:], correctSplit[2:]):
		print(trigram)
	print ""

def test_passByReference1():
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

	def changeFirstElem(li):
		newElem = [99, 99, 99]
		li[0] = newElem

	def changeAllElems1(li):
		for i in xrange(0, len(li)):
			myElem = li[i]
			myElem = [i]
			li[i] = myElem

	def changeAllElems2(li):
		counter = 0
		for elem in li:
			elem = [counter]
			counter += 1

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

	print ""

def test_passByReference2():
	listA = [0, 1]
	listB = [4, 5]
	listC = [7, 8]
	listD = [listA, listB, listC]
	myAppend(listA, 60)
	myAppend(listB, 6)
	listB = setEqual_ret(listB, listC)
	print "listA: ", listA, "listB: ", listB, "listC: ", listC, "listD: ", listD

	listA = [0, 1]
	listB = [4, 5]
	listC = [7, 8]
	listD = [listA, listB, listC]
	changeFirstElem(listD)
	print "listA: ", listA, "listB: ", listB, "listC: ", listC, "listD: ", listD

	listA = [0, 1]
	listB = [4, 5]
	listC = [7, 8]
	listD = [listA, listB, listC]
	changeAllElems1(listD)
	print "listA: ", listA, "listB: ", listB, "listC: ", listC, "listD: ", listD

	listA = [0, 1]
	listB = [4, 5]
	listC = [7, 8]
	listD = [listA, listB, listC]
	changeAllElems2(listD)
	print "listA: ", listA, "listB: ", listB, "listC: ", listC, "listD: ", listD

def test_slicing():
	listA = [5, 6, 7, 8, 9, 10, 11]
	numEndElems = 3
	listB = listA[-numEndElems:]
	print "listA: ", listA, "listB: ", listB

	print ""

def test_split1():
	sent = """Preheat the oven to 325 degrees F. Line a 9 x 1  baking 
pan with a kitchen towel. Line the brioche pan 
with plastic wrap. """
	sent = sent.replace(". ", ". @ ")
	sentVec = sent.split("@")
	print sentVec

	print ""

def test_split2():
	sent = """spicy seared scallop canapes 

MAKES 48 

6 tablespoons all-purpose flour """
	sentVec = sent.split("\n")
	print sentVec
	print "\n".join(sentVec)

	print ""

def test_chain1():
	listA = [0, 1]
	listB = [4, 5]
	listC = [7, 8]
	bigList = [listA, listB, listC]
	flattenedList = list(itertools.chain(*bigList))
	print "bigList: ", bigList
	print "flattenedList: ", flattenedList

	print ""

def test_chain2():
	listA = "hello "
	listB = "beautiful "
	listC = "world!"
	bigList = [listA, listB, listC]
	flattenedList = "".join(bigList)
	print "bigList: ", bigList
	print "flattenedList: ", flattenedList

	print ""

def test_isupper():
	word1 = "HELLO"
	word2 = "HELLo"
	print "word1.isupper(): ", word1.isupper()
	print "word2.isupper(): ", word2.isupper()
	print ""

def test_regex1():
	sent = """Preheat the oven to 325 degrees F. Line a 9 x 1  baking 
pan with a kitchen towel. Line the brioche pan 
with plastic wrap. """
	sentVec = re.split("([^a-zA-Z0-9_\''])", sent)
	print "sentVec: ", sentVec
	print ""


# test_slicing()
# test_split1()
# test_chain1()
test_chain2()
test_split2()
test_isupper()
test_regex1()

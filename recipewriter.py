"""
 Authors: Austin Ray, Bruno De Martino, Alex Lin
 File: randomwriter.py
 ---------------------
 This file includes all main code for the recipe writer.
"""

import collections, itertools
import numpy, scipy, math, random
import os, sys
import Queue, Set, string
import tokenize
#include "lexicon.h" ---- set()
#include "queue.h"   ----- Queue()
#include "tokenscanner.h"  ---- tokenize

### Data Structures 
class Ingredient:
    def __init__(self):
    	self.amount = ""
	    self.units = ""
	    self.ingredientName = ""
	    self.entireLine = ""          # Contains amount, units, and ingredient name
	    self.lineWithoutAmount = ""

	    self.wordsInIngredient = []            # Vector of strings
	    self.nonUnitWordsInIngredient = []     # Vector of strings
	    self.endSeed = []                      # Vector of strings

class InstructionSentence:
    def __init__(self):
    	self.isGoodSentence = True
	    self.isServingSentence = True

	    self.firstWord = ""
	    self.sentence = ""
	    self.sentenceSubbed = ""

	    self.order1EndSeedsInside = []       # Vector of strings
	    self.order2EndSeedsInside = []       # Vector of vector of strings
	    self.nonUnitWordsInIngredient = []   # Vector of strings
	    self.endSeed = []                    # Vector of strings
	    self.tokensInSentence = []           # Vector of strings

class InstructionStep:
	def __init__(self):
	    self.stepNumber = 0
	    self.numSentences = 0
	    self.allText = ""
	    self.allTextEdited = ""
	    self.instructionSentences = []    # Vector of InstructionSentence's
	    self.sentenceStringVec = []       # Vector of strings


"""
Class: Recipe
 * ------------------------------------------------
 * Recipe contains the ingredients, name, serving size
 * and instructions for a recipe. It also implements
 * very useful functions for the whole program.

    string name
    string allRecipeText
    string allIngredientsText
    string allInstructionsText
    string allInstructionsTextEdited
    int numServings
    int numInstructions
    int numIngredients
    int indStartRecipe
    int recipeCharLength
    bool instructionsAreNumbered
    Vector<ingredient> ingredients
    Vector<instructionStep> instructionSteps
    Vector<Vector<string>> endSeeds
    Vector<instructionSentence> goodInstructionSentences
    Vector<instructionSentence> servingInstructionSentences
    Vector<string> finalIngredientWords
    Vector<string> instructions
    Vector<string> NORMAL_UNITS
    Vector<string> NORMAL_UNITS_PLURAL
    Vector<string> ABNORMAL_UNITS
    Vector<string> DESCRIPTORS
    Vector<string> STANDALONES
    Vector<string> INSTRUCTION_VERBS
    Vector<string> VALID_AFTER_WORDS
    Vector<string> VALID_BEFORE_WORDS
    Map<string,int> UNIT_TO_VOLUME    #Volume in milliliters (cc, cm^3)

 * ------------------------------------------------
"""
class Recipe:

	self.VALID_AFTER_WORDS = ["to", "in", "into", "on", "are", ".", ",", ";", "is"]
    self.VALID_BEFORE_WORDS = ["NUMBERS", "the", "and", "with"]
    self.NORMAL_UNITS = ["teaspoon", "tablespoon", "pound", "cup", "ounce", \
            "bunch", "strip", "clove", "stalk", "stick", "loaf", \
            "rind", "slice", "sprig", "head", "ear", "can", "pint", \
            "quart", "gallon", "sheet"]
    self.NORMAL_UNITS_PLURAL = ["teaspoons", "tablespoons", "pounds", "cups", "ounces", \
            "bunches", "strips", "cloves", "stalks", "sticks", "loaves", \
            "rinds", "slices", "sprigs", "heads", "ears", "cans", "pints", \
            "quarts", "gallons", "sheets"]
    self.ABNORMAL_UNITS = ["Pinch of", "Juice of", "Zest of"]
    self.DESCRIPTORS = ["large", "small", "whole", "thin", "coarse", "red", "green",
            "rack", "hot", "medium", "baby", "fresh", "dried", "frozen",
            "boneless", "skinless", "ripe", "pink", "coarsely chopped", "cold",
            "minced", "grated", "finely grated", "ground", "hot", "freshly ground"]
    self.STANDALONES = ["Freshly ground pepper", "Coarse salt", \
            "Coarse salt and freshly ground pepper", \
            "Fresh tarragon and tarragon flowers", \
            "Creamy Tarragon Vinaigrette", \
            "Freshly ground black pepper", \
            "Canola oil", \
            "Coarse salt and freshly ground black pepper", \
            "Lime wedges", \
            "Cooking spray", \
            "Cold water" \
            "Crushed Ice"]
    self.INSTRUCTION_VERBS = ["Fill", "Mix", "Place", "Stir", "In", "Process", "Heat", "Whisk", \
            "Combine", "With", "Puree", "Squeeze", "Bring", "Put", "Using", "Toss", "Melt", \
            "Prepare", "Pour", "Preheat", "Soak", "Halve", "Line", "Cut", "Add", "Pulse", \
            "Mash", "Blend", "Sprinkle", "Beat", "Arrange", "Set", "Fit", "Scoop", "Cover"]
    self.UNIT_TO_VOLUME = {}
    self.UNIT_TO_VOLUME["cup"] = 237
    self.UNIT_TO_VOLUME["teaspoon"] = 5
    self.UNIT_TO_VOLUME["tablespoon"] = 15
    self.UNIT_TO_VOLUME["pint"] = 473
    self.UNIT_TO_VOLUME["quart"] = 950
    self.UNIT_TO_VOLUME["gallon"] = 3800
    self.UNIT_TO_VOLUME["can"] = 474

    def __init__(self):
        self.name = ""
        self.numServings = 0
        self.numIngredients = 0
        self.numInstructions = 0
        self.allRecipeText = ""
        self.indStartRecipe = 0
        self.recipeCharLength = 0
        self.allIngredientsText = ""
        self.allInstructionsText = ""

    ## Setters
    def setAllRecipeText(newAllRecipeText):
        self.allRecipeText = newAllRecipeText
    def setAllIngredientsText(newAllIngredientsText):
        self.allIngredientsText = newAllIngredientsText
    def setAllInstructionsText(newAllInstructionsText):
        self.allInstructionsText = newAllInstructionsText
    def setName(newName):
        self.name = newName
    def setNumServings(newNumServings):
        self.numServings = newNumServings
    def setNumInstructions(newNumInstructions):
        self.numInstructions = newNumInstructions
    def setNumIngredients(newNumIngredients):
        self.numIngredients = newNumIngredients
    def setIndStartRecipe(newIndStartRecipe):
        self.indStartRecipe = newIndStartRecipe
    def setRecipeCharLength(newRecipeCharLength):
        self.recipeCharLength = newRecipeCharLength
    def setIngredients(newIngredients):
        self.ingredients = newIngredients
    def setInstructions(newInstructions):
        self.instructions = newInstructions
    def setEndSeeds(newEndSeeds):
        self.endSeeds = newEndSeeds
    def setInstructionSteps(newInstructionSteps):
        self.instructionSteps = newInstructionSteps

    # Getters 
    def getAllRecipeText():
        return self.allRecipeText
    def getAllIngredientsText():
        return self.allIngredientsText
    def getAllInstructionsText():
        return self.allInstructionsText
    def getName():
        return self.name
    def getNumServings():
        return self.numServings
    def getNumInstructions():
        return self.numInstructions
    def getNumIngredients():
        return self.numIngredients
    def getIndStartRecipe():
        return self.indStartRecipe
    def getRecipeCharLength():
        return self.recipeCharLength
    def getIngredients():
        return self.ingredients
    def getInstructions():
        return self.instructions
    def getEndSeeds():
        return self.endSeeds
    def getInstructionSteps():
        return self.instructionSteps
    def getGoodInstructionSentences():
        return self.goodInstructionSentences
    def getServingInstructionSentences():
        return self.servingInstructionSentences

    # Other Function Implementations */
    def addInstructionStep(newInstructionStep):
        instructionSteps += newInstructionStep
        return instructionSteps

    def fillInstructionSentenceTokens():
        for i in xrange(0, len(goodInstructionSentences)):
            instructionSentence myInstructionSentence = goodInstructionSentences[i]
            TokenScanner scanner(myInstructionSentence.sentence)
            while (scanner.hasMoreTokens()):
                currentToken = scanner.nextToken()
                myInstructionSentence.tokensInSentence += currentToken
            goodInstructionSentences[i] = myInstructionSentence

    def divideInstructionSentences():
        for i in xrange(0, len(instructionSteps)):
            myInstructionStep = instructionSteps[i]
            stepText = myInstructionStep.allText
            stepText = stringReplace(stepText, ". ", ". @ ")
            sentenceVec = stringSplit(stepText, "@")
            for j in xrange(0, len(sentenceVec)):
                sentence = sentenceVec[j]
                sentence = trim(sentence)
                if (sentence=="") continue
                instructionSentence newInstructionSentence
                newInstructionSentence.sentence += sentence
                TokenScanner scanner(newInstructionSentence.sentence)
                while (scanner.hasMoreTokens()):
                    currentToken = scanner.nextToken()
                    newInstructionSentence.tokensInSentence += currentToken
                myInstructionStep.instructionSentences.append(newInstructionSentence)
                myInstructionStep.sentenceStringVec.append(sentence)
            instructionSteps[i] = myInstructionStep

    def findFinalIngredientWords():
        lastWords = []
        for i in xrange(0, len(endSeeds)):
            endSeed = endSeeds[i]
            lastWord = endSeed[len(endSeed)-1]
            lastWords += lastWord
            if (len(endSeed)==1) continue
            lastWords += endSeed[len(endSeed)-2]
        finalIngredientWords = lastWords

    def findSeedsInInstructionSentences():
        servingWords = []
        servingWords += "Serve", "serve", "Served", "served"
        for i in xrange(0, len(instructionSteps)):
            myInstructionStep = instructionSteps[i]
            for j in xrange(0, len(myInstructionStep.instructionSentences)):
                myInstructionSent = myInstructionStep.instructionSentences[j]
                sentence = myInstructionSent.sentence
                myInstructionSent.isServingSentence = False
                TokenScanner scanner(sentence)
                scanner.ignoreWhitespace()
                scanner.addWordCharacters("'")
                previousPreviousToken = ""
                previousToken = ""
                currentToken = ""
                while (scanner.hasMoreTokens()):
                    previousPreviousToken = previousToken
                    previousToken = currentToken
                    currentToken = scanner.nextToken()
                    if (previousPreviousToken == "") continue
                    if (previousToken in finalIngredientWords and
                            !(previousPreviousToken in self.VALID_BEFORE_WORDS and
                              currentToken in self.VALID_AFTER_WORDS)):
                        myInstructionSent.isGoodSentence = False
                        break
                    elif (previousToken in finalIngredientWords):
                        myInstructionSent.order1EndSeedsInside += previousToken
                        myInstructionSent.isGoodSentence = True
                    else:
                        myInstructionSent.isGoodSentence = True
                    if (previousPreviousToken in servingWords or previousToken in servingWords or currentToken in servingWords):
                        myInstructionSent.isServingSentence = True
                myInstructionSent.sentence = stringReplace(myInstructionSent.sentence, "\n", "")
                if (myInstructionSent.isGoodSentence) goodInstructionSentences += myInstructionSent
                if (myInstructionSent.isServingSentence) servingInstructionSentences += myInstructionSent
                myInstructionStep.instructionSentences[j] = myInstructionSent
            instructionSteps[i] = myInstructionStep

    def printGoodSentences():
        print self.name
        print "-----------------------------------------"
        for i in xrange(0, len(goodInstructionSentences)):
            myInstructionSent = goodInstructionSentences[i]
            if (len(myInstructionSent.order1EndSeedsInside)==0) continue
            sentence = myInstructionSent.sentence
            sentence = stringReplace(sentence, "\n", "")
            print "   Sentence: ", sentence
            print "      Seeds: ", myInstructionSent.order1EndSeedsInside
        print "\n\n"

    def separateInstructions():
        myInstructionSteps = []
        #print name
        if (instructionsAreNumbered):
            index = 1
            boundsOfSteps = []
            while (True):
                stepStart1 = ""
                stepStart2 = ""
                stepStart3 = ""
                stepStart4 = ""
                if (index == 1) stepStart1 = "\n" + integerToString(index) + ". "
                else:
                    stepStart1 = " \n" + integerToString(index) + ". "
                    stepStart2 = " \n\n" + integerToString(index) + ". "
                    stepStart3 = " \n\n\n" + integerToString(index) + ". "
                    stepStart4 = " \n\n\n\n" + integerToString(index) + ". "

                officialStepStart = ""
                indexOfStart = stringIndexOf(self.allInstructionsText, stepStart1)
                officialStepStart = stepStart1
                if (indexOfStart==-1):
                    indexOfStart = stringIndexOf(self.allInstructionsText, stepStart2)
                    officialStepStart = stepStart2
                if (indexOfStart==-1):
                    indexOfStart = stringIndexOf(self.allInstructionsText, stepStart3)
                    officialStepStart = stepStart3
                if (indexOfStart==-1):
                    indexOfStart = stringIndexOf(self.allInstructionsText, stepStart4)
                    officialStepStart = stepStart4

                if (!boundsOfSteps.isEmpty()) boundsOfSteps[index-2] += indexOfStart
                if (indexOfStart != -1):
                    indexOfRealStart = indexOfStart + len(officialStepStart)
                    boundOfStep = []
                    boundOfStep += indexOfRealStart
                    boundsOfSteps += boundOfStep
                else:
                    boundsOfLastStep = boundsOfSteps[len(boundsOfSteps)-1]
                    boundsOfLastStep += len(self.allInstructionsText)-1
                    break
                index += 1
            for i in xrange(0, len(boundsOfSteps)):
                boundsOfStep = boundsOfSteps[i]
                newInstructionStep = InstructionStep()
                newInstructionStep.stepNumber = i+1
                newInstructionStep.allText = self.allInstructionsText[boundsOfStep[0] : boundsOfStep[1]]
                newInstructionStep.allText = trim(newInstructionStep.allText)
                myInstructionSteps += newInstructionStep
        else:
            newInstructionStep = InstructionStep()
            newInstructionStep.stepNumber = 0
            newInstructionStep.allText = trim(self.allInstructionsText)
            if (startsWith(newInstructionStep.allText,"\n")) newInstructionStep.allText = newInstructionStep.allText[0]
            myInstructionSteps += newInstructionStep
        #print myInstructionSteps[0].allText
        instructionSteps = myInstructionSteps
        return myInstructionSteps

    def printAllInstructionText():
        print self.name
        print "------------------------------------------"
        print self.allInstructionsText, "\n\n"

    def printAllInstructionSteps():
        print self.name
        print "------------------------------------------"
        i=1
        for (iStep in instructionSteps):
            print "   Step ", i, ": ", iStep.allText
            i += 1
        print "\n\n"

    # MODIFY THIS SO IT CAN HANDLE AN END SEED LENGTH OF 3
    def fillEndSeeds(endSeedLength):
        for i in xrange(0, len(ingredients)):
            myIngredient = ingredients[i]
            words = myIngredient.wordsInIngredient
            numWords = len(words)
            if (numWords == 1):
                myIngredient.endSeed += words[0]
            elif (numWords == 2):
                if (isUnit(words[0])) myIngredient.endSeed += words[1]
                else:
                    for j in reversed(xrange(1, endSeedLength+1)):
                        myIngredient.endSeed += words[numWords-j]
            else:
                for j in reversed(xrange(1, endSeedLength+1)):
                    myIngredient.endSeed += words[numWords-j]
            ingredients[i] = myIngredient
            endSeeds.append(myIngredient.endSeed)

    def printEndSeeds():
        print self.name
        print "---------------------------------"
        for (endSeed in endSeeds):
            print "   ", endSeed

    def printIngredients():
        for i in xrange(0, len(ingredients)):
            print "   ", ingredients[i].entireLine
            print "        Amount: ", ingredients[i].amount
            print "        Units: ", ingredients[i].units
            print "        Words: ", ingredients[i].wordsInIngredient
            print "        Non-Unit Words: ", ingredients[i].nonUnitWordsInIngredient
            print "        End Seed: ", ingredients[i].endSeed
        print "   End Seeds:"
        for (endSeed in endSeeds):
            print "   ", endSeed

    def isUnit(word):
        for j in xrange(0, len(self.NORMAL_UNITS)):
            if (word == self.NORMAL_UNITS[j] or word == NORMAL_UNITS_PLURAL[j]):
                return True
        return False

    def vectorContains(vec, word):
        return word in vec

    def vectorContains(superVec, subVec):
        for (member in superVec):
            if (subVec == member) return True
        return False

    def findIngredientAmounts():
        for i in xrange(0, len(ingredients)):
            myIngredient = ingredients[i]
            line = myIngredient.entireLine
            if (isdigit(line[0])):
                numString = ""
                for j in xrange(1, len(line)-3):
                    previousChar = line[j-1]
                    currentChar = line[j]
                    nextChar = line[j+1]
                    nextNextChar = line[j+2]
                    nextNextNextChar = line[j+3]
                    if (isdigit(previousChar) and !isdigit(nextChar) and
                            currentChar==' ' and !(nextChar=='t' and nextNextChar=='o' and nextNextNextChar==' ')):
                        numString += charToString(previousChar)
                        break
                    elif (isdigit(previousChar) and !isdigit(nextChar) and (currentChar=='-' or currentChar=='x')):
                        for k in reversed(xrange(0, len(numString))):
                            if (numString[k] == ' '):
                                numString = numString[:-1]   # Used .erase() before
                                break
                            else:
                                numString = numString[:-1]   # Used .erase() before
                        break
                    else:
                        numString += charToString(previousChar)
                myIngredient.amount = numString
            else:
                myIngredient.amount = "NO_LEADING_NUMBER"
            ingredients[i] = myIngredient

    def findIngredientUnits():
        for i in xrange(0, len(ingredients)):
            myIngredient = ingredients[i]
            line = myIngredient.entireLine
            myVec = stringSplit(line, " ")
            theUnits = ""
            unitsFound = False
            for i in xrange(0, len(myVec))):
                if (isUnit(myVec[i])):
                    theUnits = myVec[i]
                    unitsFound = True
                    break
                if (unitsFound) break
            myIngredient.units = theUnits
            ingredients[i] = myIngredient

    def fillIngredientWords():
        for i in xrange(0, len(ingredients)):
            myIngredient = ingredients[i]
            line = myIngredient.entireLine
            wordsInIngredient = stringSplit(line, " ")
            for i in xrange(0, len(wordsInIngredient))):
                word = wordsInIngredient[i]
                newWord = ""
                for (ch in word):
                    if (!isalpha(ch)) newWord += " "
                    else newWord += charToString(ch)
                wordsInIngredient[i] = newWord

            ingredientWords = []
            validWord = True
            for i in xrange(0, len(wordsInIngredient))):
                currentWord = wordsInIngredient[i]
                for (ch in currentWord):
                    if (isdigit(ch)) validWord = False
                if (validWord):
                    word = wordsInIngredient[i]
                    newWord = ""
                    for (ch in word):
                        if (ch==',') newWord += ""
                        elif (ch=='-') newWord += " "
                        elif (!isalpha(ch)) newWord += " "
                        else newWord += charToString(ch)
                    newWord = trim(newWord)
                    wordSplit = stringSplit(newWord, " ")
                    for (newWord2 in wordSplit):
                        ingredientWords.append(newWord2)
                validWord = True

            nonUnitIngredientWords = []
            for (word in ingredientWords):
                if (!isUnit(word)) nonUnitIngredientWords += word
            myIngredient.wordsInIngredient = ingredientWords
            myIngredient.nonUnitWordsInIngredient = nonUnitIngredientWords
            ingredients[i] = myIngredient

    def separateIngredients(Lexicon adjectives):
        ingredientsText = self.allIngredientsText
        myIngredients = []
        payAttention = False
        inParentheses = False
        pastComma = False
        ingredientsStarted = False
        wordsInIngredient = 0
        currentWord = ""

        for currentIndex in xrange(1, len(ingredientsText)-2):
            previousChar = ingredientsText[currentIndex-1]
            currentChar = ingredientsText[currentIndex]
            nextChar = ingredientsText[currentIndex+1]

            if (isalpha(previousChar)) currentWord += charToString(previousChar)
            elif (currentWord != ""):
                wordsInIngredient += 1
                currentWord = ""

            if (previousChar == '\n' and isdigit(currentChar) and !inParentheses):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (currentIndex==1 and isdigit(previousChar)):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (previousChar == '\n' and isupper(currentChar) and ingredientsStarted and !inParentheses):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (ingredientsStarted):
                if (currentChar == ',' and !inParentheses and !(currentWord in adjectives and wordsInIngredient < 2)):
                    payAttention = False
                    pastComma = True

                elif (currentChar == '('):
                    payAttention = False
                    inParentheses = True
                elif (currentChar == ')'):
                    inParentheses = False
                    if (!pastComma):
                        payAttention = True

            if (payAttention):
                currentIngredient = myIngredients[len(myIngredients)-1]
                currentLine = currentIngredient.entireLine
                if (currentChar == ')' or (currentChar == ' ' and currentLine[len(currentLine)-1] == ' ')) continue
                if (currentIndex==1 and isdigit(previousChar)) currentLine += charToString(previousChar)
                if (currentChar != '\n') currentLine += charToString(currentChar)
                if (currentIndex==len(ingredientsText))-2 and isalpha(nextChar)) currentLine += charToString(nextChar)
                currentIngredient.entireLine = currentLine
                myIngredients.set(len(myIngredients)-1, currentIngredient)
        ingredients = myIngredients

    def removeCaps():
        recipeText = self.allRecipeText
        capsLineIndices = []
        inMakeServeLine = False
        belowMakeServeLine = False
        inHeaderLine = False
        for currentIndex in xrange(1, len(recipeText)-2):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            makesOrServes = ""
            if (!belowMakeServeLine):
                makesOrServes = recipeText[currentIndex:currentIndex + 6]
                if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                    inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            if (inHeaderLine):
                if (currentChar == '\n'):
                    inHeaderLine = False
            elif (isalpha(currentChar) and isalpha(nextChar) and
                     isupper(currentChar) and isupper(nextChar) and !inMakeServeLine):
                capsLineIndices.append(currentIndex)
                inHeaderLine = True

        newRecipeText = removeCapsLinesWithIndices(recipeText, capsLineIndices)
        self.allRecipeText = newRecipeText
        self.recipeCharLength = newRecipeText.length()

    def removeCapsLinesWithIndices(recipeText, capsLineIndices):
        newRecipeText = recipeText
        for i in reversed(xrange(0, len(capsLineIndices))):
            previousSlashNIndex = 0
            nextSlashNIndex = 0
            ind = 0
            previousChar = ''
            currentChar = ''
            nextChar = ''

            ind = capsLineIndices[i]
            while (True):
                if (ind > 0) previousChar = recipeText[ind-1]
                currentChar = recipeText[ind]
                if (ind < (int(recipeText.length())-2)) nextChar = recipeText[ind+1]
                if (previousChar == '\n' or ind == 0):
                    previousSlashNIndex = ind
                    break
                ind -= 1

            ind = capsLineIndices[i]
            while (True):
                if (ind > 0) previousChar = recipeText[ind-1]
                currentChar = recipeText[ind]
                if (ind < (int(recipeText.length())-2)):
                    nextChar = recipeText[ind+1]
                if (nextChar == '\n' or ind == int(recipeText.length())-1):
                    nextSlashNIndex = ind
                    break\
                ind += 1

            lineLength = nextSlashNIndex - previousSlashNIndex + 1
            lineString = recipeText[previousSlashNIndex: previousSlashNIndex + lineLength]
            #print lineString
            stringReplaceInPlace(newRecipeText, lineString, "")
        return newRecipeText

    def findNumServings():
        numServingsString = ""
        recipeText = self.allRecipeText
        inMakeServeLine = False
        belowMakeServeLine = False
        for currentIndex in xrange(0, len(recipeText)-7):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            makesOrServes = ""
            if (!belowMakeServeLine):
                makesOrServes = recipeText[currentIndex: currentIndex + 6]
                if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                    inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            if (inMakeServeLine):
                if (isdigit(currentChar)):
                    numServingsString += charToString(currentChar)
                if (numServingsString != "" and !isdigit(nextChar)) break
                if (nextChar == '\n'):
                    if (len(numServingsString) == 0) numServingsString = "10"
                    break
        returnInt = -1
        if (numServingsString != "") returnInt = stringToInteger(numServingsString)
        return returnInt

    def findTitle():
        title = ""
        recipeText = self.allRecipeText
        currentIndex = 0
        while (True):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            nextNextChar = recipeText[currentIndex+2]
            if (nextChar == '\n' and nextNextChar == '\n'):
                break
            elif (currentChar == '\n'):
                pass
            else:
                title += charToString(currentChar)
            currentIndex += 1
        return title

    def findAllIngredients():
        allIngredients = "\n"
        recipeText = self.allRecipeText
        inMakeServeLine = False
        belowMakeServeLine = False
        haveSeenNumbers = False
        for currentIndex in xrange(0, len(recipeText)-3):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            nextNextChar = recipeText[currentIndex+2]
            makesOrServes = ""
            if (currentIndex < len(recipeText)-7):
                makesOrServes = recipeText[currentIndex, currentIndex+6]
            if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                haveSeenNumbers = False
                inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            elif (belowMakeServeLine):
                if (isdigit(currentChar)) haveSeenNumbers = True
                if (allIngredients == "" and currentChar == '\n'):
                    pass
                else:
                    if ((currentChar == '\n' and isalpha(nextChar) and haveSeenNumbers and
                         (getWord(currentIndex+1, recipeText) in self.INSTRUCTION_VERBS)) or
                            (currentChar == '\n' and isdigit(nextChar) and nextNextChar == '.')):
                        self.allInstructionsText = recipeText[currentIndex:]
                        instructionsAreNumbered = (currentChar == '\n' and isdigit(nextChar) and nextNextChar == '.')
                        break
                    else:
                        allIngredients += charToString(currentChar)
        return allIngredients

    def getWord(currentIndex, recipeText):
        returnWord = ""
        while (True):
            currentChar = recipeText[currentIndex]
            if (!isalpha(currentChar)) break
            else returnWord += charToString(currentChar)
            currentIndex += 1
        return returnWord




"""Recipe-Related Function Prototypes

string getAllText(ifstream & infile)
int findIndEndLastRecipe(int indStartRecipe, string & allText)
int findIndPreviousTitle(int index, string & allText)
Map<string,string> invertMap(Map<string,string> map)
void fillRecipes(Vector<Recipe> & allRecipes, string & allText)
void splitRecipes(Vector<Recipe> & allRecipes, Lexicon & adjectives, int endSeedLength)
void printListOfRecipesIngredients(Vector<Recipe> & allRecipes, int startingIndex, int numToPrint)
void giveRecipesAdjectives(Vector<Recipe> & allRecipes, Lexicon & adjectives)
void makeListAllIngredients(Vector<Recipe> & allRecipes)
void printRecipeEndSeeds(Vector<Recipe> & allRecipes, int startingIndex=-5, int numToPrint=-5)
void makeEndSeedMap(Vector<Recipe> & allRecipes, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap)
void deleteOneIngredientRecipes(Vector<Recipe> & allRecipes)
void makeIngredientMarkov(Vector<ingredient> & allIngredients, string & allIngredientsString, Map<Vector<string>,Vector<string>> & reverseSeedMap,
                          int seedLength, int endSeedLength, int defaultSeedLength=1)
void compileAllIngredients(Vector<Recipe> & allRecipes, Vector<ingredient> & allIngredients, string & allIngredientsString)
Vector<string> makeRandomIngredientsList(Map<Vector<string>,Vector<string>> & reverseSeedMap, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap,
                                         int numIngredients, int seedLength, int endSeedLength, int endSeedSeedLength)
Vector<string> makeRandomInstructions(Vector<instructionSentence> & bigVec, Vector<string> ingredientsList)
bool vectorContains(Vector<string> vec, string word)
bool vectorContains(Vector<Vector<string>> superVec, Vector<string> subVec)
void refineReverseSeedMapKeys(Map<Vector<string>,Vector<string>> & reverseSeedMap)
string refineRandomInstructions(Vector<string> & instructions, Vector<instructionSentence> & servingSentencesWithoutSeeds)
"""


# Main Program */
def main():
    ifstream adj_infile
    adj_filename = "adjectives.txt"
    if (!openFile(adj_infile, adj_filename)):
        error("Can't open " + adj_filename)
    Lexicon adjectives(adj_filename)
    adj_infile.close()

    ifstream adj_infile2
    if (!openFile(adj_infile2, adj_filename)):
        error("Can't open " + adj_filename)ƒ
    properAdjectives = []
    for i in xrange(0, len(adjectives) / 2):
        word = ""
        getLine(adj_infile2, word)
        if (isupper(word[0])):
        	properAdjectives += word
    adj_infile2.close()

    ifstream infile

    fileName = "MarthaStewart-LivingCookbook.txt"
    infile.open(fileName.c_str())
    print "            Random Recipe Writer | CS 106B | Winter 2015 | Austin Ray"
    print "   -----------------------------------------------------------------------------\n"

    greet = ""
    greet += "   Hello there! I am a random recipe writer! Thanks for checking me out!\n"
    greet += "   I am able to create random recipes for you based on the recipes found in\n"
    greet += "   The Martha Stewart Living Cookbook\" by using Markov chains. If you want to\n"
    greet += "   know how I do this, enter \"explain\", otherwise enter \"start\" to begin: "
    start = getLine(greet)
    if (start=="explain"):
        print "\n\n   -----------------------------Program Explanation-----------------------------\n"
        print "   ", "   The first thing I do is separate all of Martha's recipes into C++ objects."
        print "   ", "Next, I do some refinement on each recipe, separating ingredients from"
        print "   ", "instructions, separating ingredients from each other, etc. After that," <<endl
        print "   ", "I realize that the last two words of each ingredient are the best"
        print "   ", "description of that ingredient. So I make a C++ map to associate"
        print "   ", "each \"end seed\" with other end seeds that they've been seen with in"
        print "   ", "recipes. This is the Markov chain that allows me to add new ingredients"
        print "   ", "to the recipe that go well with previous ingredients. Next, I create another"
        print "   ", "Markov chain to associate words in an ingredient with the words behind"
        print "   ", "(to the left of) them. This allows me to add a new ingredient just by its"
        print "   ", "end seed, then fill in the rest of the line from right to left, forming"
        print "   ", "a complete ingredient. In this way, I create my full ingredients list."
        print "   ", "Since it uses a Markov chain, more ingredients means less cohesiveness"
        print "   ", "between all of the ingredients. You've been Warned!"
        print "   ", "   Next, for the title, I examine the ingredients in my recipe, adding"
        print "   ", "good words for titles and ignoring the bad ones. Oh, and I also add"
        print "   ", "a special adjective at the beginning of the title to give each recipe"
        print "   ", "its own personal flair. Next, for the instructions, I first look at"
        print "   ", "all the instruction sentences I've seen in the cookbook. We can see"
        print "   ", "that certain sentences are too complicated to try to fit my freshly"
        print "   ", "picked ingredients into, while others are simple and allow me to work"
        print "   ", "my ingredients in just fine. Primarily, this includes sentences that"
        print "   ", "use small connector words like with, and, to, the, etc. around their"
        print "   ", "ingredients. This allows me to input my ingredients without creating"
        print "   ", "too crazy of a sentence - pretty cool, huh? Next, I associate each"
        print "   ", "sentence with the ingredients found in it. When I go to write the"
        print "   ", "instructions for my newly generated recipe, I look at my ingredients"
        print "   ", "and try to find simple sentences I've seen them in before. If I find"
        print "   ", "a good sentence with the ingredient in it, I put that sentence down"
        print "   ", "as an instruction step and move on to my other ingredients. If I can't"
        print "   ", "find a good sentence with an ingredient, I just take any old simple"
        print "   ", "sentence and insert my ingredient into it, replacing the one that was"
        print "   ", "there before. After I've written instructions that include all of my"
        print "   ", "ingredients, I then add a good ending sentence, if one isn't there"
        print "   ", "already. And voila! You have your scrumptious new randomly generated"
        print "   ", "recipe. Happy cooking!"
    print "\n\n   -------------------------------Main Program----------------------------------\n"
    seedLength = 2
    endSeedLength = 2
    numIngredients = 0
    endSeedSeedLength = 0
    numRecipesToPrint = 0
    allAtOnce = ""
    while (True):
        numIngredients = getInteger("   Enter the desired number of ingredients per recipe (5-15 allowed): ")
        if (numIngredients<5 or numIngredients>15):
            print "\n   Invalid number of ingredients. Try again.\n"
            continue
        break
    while (True):
        endSeedSeedLength = getInteger("   Enter ingredient similarity within recipes (1-5 allowed, 5 = very similar): ")
        if (endSeedSeedLength<1 or endSeedSeedLength>5):
            print "\n   Invalid ingredient similarity. Try again.\n"
            continue
        break
    while (True):
        numRecipesToPrint = getInteger("   Enter the number of recipes you want (1-100 allowed): ")
        if (numRecipesToPrint<1 or numRecipesToPrint>100):
            print "\n   Invalid number of recipes. Try again.\n"
            continue
        break
    while (True):
        allAtOnce = getLine("   Do you want to print recipes one by one, or all at once?\n   (Enter either \"one\" or \"all\"): ")
        if (!(allAtOnce=="one") and !(allAtOnce=="all")):
            print "\n   Invalid input. Try again.\n"
            continue
        elif (allAtOnce=="one"):
            print "\n   Got it. Press Enter after each recipe prints to get the next one."
        break

    print "\n   ", "I'm going to generate your recipes now. This might take a minute...\n\n"

    allRecipes = []
    allText = getAllText(infile)
    fillRecipes(allRecipes, allText)
    splitRecipes(allRecipes, adjectives, endSeedLength)
    deleteOneIngredientRecipes(allRecipes)

    print "   ", "...Making progress..."
    allIngredients = []
    allIngredientsString = ""
    compileAllIngredients(allRecipes, allIngredients, allIngredientsString)

    reverseSeedMap = {}
    makeIngredientMarkov(allIngredients, allIngredientsString, reverseSeedMap, see dLength, endSeedLength)

    print "   ", "...Still working..."
    refineReverseSeedMapKeys(reverseSeedMap)


    endSeedMap = {}
    makeEndSeedMap(allRecipes, endSeedMap)

    print "   ", "...Can't be much longer now..."

    Lexicon singleEndSeeds
    for i in xrange(0, len(endSeedMap.keys())):
        key = endSeedMap.keys()[i]
        endWord = key[len(key)-1]
        if (endWord in singleEndSeeds) continue
        singleEndSeeds.append(endWord)

    allGoodSentences = []
    goodSentencesWithSeeds = []
    servingSentences = []
    servingSentencesWithoutSeeds = []
    for i in xrange(0, len(allRecipes)):
        myRecipe = allRecipes[i]
        myRecipe.fillInstructionSentenceTokens()
        goodInstructionSentences = myRecipe.getGoodInstructionSentences()
        servingInstructionSentences = myRecipe.getServingInstructionSentences()
        allGoodSentences += goodInstructionSentences
        servingSentences += servingInstructionSentences
        for instSent in goodInstructionSentences:
            if (len(instSent.order1EndSeedsInside) != 0):
                containsBadSeed = False
                for token in instSent.tokensInSentence:
                    if (!(token in instSent.order1EndSeedsInside) and token in singleEndSeeds) containsBadSeed = True
                if (!containsBadSeed) goodSentencesWithSeeds += instSent
        for instSent in servingInstructionSentences:
            if (len(instSent.order1EndSeedsInside) == 0):
                tokens = instSent.tokensInSentence
                hasSeed = False
                for token in tokens:
                    if (token in singleEndSeeds):
                        hasSeed = True
                        break
                if (!hasSeed) servingSentencesWithoutSeeds += instSent

    validEndsOfTitles = ["bread", "oil", "sausage", "cheese", "corn", "salad", "dressing",\
            "stock", "pepper", "bacon", "meat", "mustard", "butter", "water", "melon",\
            "kiwi", "lettuce", "yogurt", "sauce", "rice", "salt", "port", "vinegar"]

    badTitleWords = []
    badTitleWords += "halves", "thighs", "leaves", "stalks", "cloves", "half", "thigh", "leaf", "stalk", "clove", "extract"

    print "\n\n\n\n\n\n\n"


    metaTextToPrint = ""

    metaTextToPrint += "               Randomly Generated Recipe Booklet\n"
    metaTextToPrint += "            ----------------------------------------- \n\n"
    print metaTextToPrint
    markovIngredientsList = []
    shouldStop = False
    if (allAtOnce == "one") shouldStop = True
    for i in xrange(0, numRecipesToPrint):
        if (i>=1 and allAtOnce == "one" and shouldStop):
            continueString = getLine()
        markovIngredientsList = makeRandomIngredientsList(reverseSeedMap, endSeedMap, numIngredients, seedLength, endSeedLength, endSeedSeedLength)
        if (markovIngredientsList[0] == "ERROR"):
            i--
            shouldStop = False
            continue
        lastTokens = []
        for j in xrange(0, len(markovIngredientsList)):
            line = markovIngredientsList[j]
            TokenScanner scanner(line)
            lastToken = ""
            while (scanner.hasMoreTokens()):
                currentToken = scanner.nextToken()
                lastToken = currentToken
            lastTokens += lastToken

        r = randomInteger(0,len(properAdjectives)-1)
        startingWord = properAdjectives[r]
        recipeTitle = ""
        recipeTitle += startingWord + " "
        lastWordInTitle = ""
        lastWordInTitle2 = ""
        for token in lastTokens:
            if ((token in validEndsOfTitles) and !(token in badTitleWords)):
                lastWordInTitle = token
                break
        for token in lastTokens:
            if (token[len(token)-1] == 's' and !(token in badTitleWords)):
                lastWordInTitle = token
                break


        for token in lastTokens:
            if ((token in validEndsOfTitles) and token != lastWordInTitle and !(token in badTitleWords):
                lastWordInTitle2 = token
                break
        for token in lastTokens:
            if (token[len(token)-1] == 's' and token != lastWordInTitle and !(token in badTitleWords):
                lastWordInTitle2 = token
                break
        descriptorWord = ""
        for token in lastTokens:
            if (token[len(token)-1] != 's' and token != lastWordInTitle and token != lastWordInTitle2 and !(token in badTitleWords):
                descriptorWord = token
                break

        if (descriptorWord != ""):
        	recipeTitle += charToString(toupper(descriptorWord[0])) + descriptorWord[1] + " "
        if (lastWordInTitle != ""):
        	recipeTitle += charToString(toupper(lastWordInTitle[0])) + lastWordInTitle[0]
        if (lastWordInTitle != "" and lastWordInTitle2 != ""):
        	recipeTitle += " with "
        if (lastWordInTitle2 != ""):
        	recipeTitle += charToString(toupper(lastWordInTitle2[0])) + lastWordInTitle2[0]

        if (descriptorWord == "" and lastWordInTitle == "" and lastWordInTitle2 == ""):
        	recipeTitle += "Food"

        textToPrint = ""
        textToPrint += " " + recipeTitle

        #        print "Checkpoint 3"
        rand = randomInteger(0,len(allRecipes)-1)
        myRecipe = allRecipes[rand]
        numServings = myRecipe.getNumServings()
        if (numServings<=0):
        	numServings = randomInteger(1,9)
        textToPrint += " (SERVES " + integerToString(numServings) + ")\n"
        #        print "Checkpoint 4"

        textToPrint += "   Ingredients:\n"
        for ingredient in markovIngredientsList:
            if (ingredient[2]=='/'):
            	ingredient = charToString(ingredient[0]) + ingredient[:4]
            textToPrint += "      " + ingredient + "\n"
        textToPrint += "\n"

        #        print "Checkpoint 5"
        randomInstructions = makeRandomInstructions(goodSentencesWithSeeds, markovIngredientsList)
        if (randomInstructions[0] == "ERROR"):
            i -= 1
            shouldStop = False
            continue
        #        print "Checkpoint 6"
        instructionsToPrint = refineRandomInstructions(randomInstructions, servingSentencesWithoutSeeds)
        textToPrint += "   Instructions:\n"
        textToPrint += instructionsToPrint + "\n\n\n"
        #        print "Checkpoint 7"

        print textToPrint
        metaTextToPrint += textToPrint
        textToPrint.clear()
        markovIngredientsList.clear()
        if (allAtOnce == "one"):
        	shouldStop = True

    print "\n\n\n   I have saved your recipes in \"Random_Recipe_Book.txt\" in this application's folder.\n\n\n"

    ofstream outfile
    outfile.open("Random_Recipe_Book.txt")
    outfile, metaTextToPrint
    outfile.close()
    infile.close()        #Close the stream
    return 0



# Function Implementations */

def refineRandomInstructions(instructions, servingSentencesWithoutSeeds):
    serveSentence = ""
    startSentence = ""
    servingWords = ["Serve", "serve", "Served", "served"]
    startWords = ["Add", "Mix", "Combine", "In", "Prepare", "Preheat", "Blend", "Using", "Place", "Melt", "Slice", "Halve", "Heat"]
    servingSentenceExists = False
    for i in xrange(0, len(instructions)):
        sentence = instructions[i]

        for (word in servingWords):
            if (stringContains(sentence,word)):
                instructions[i] = instructions[len(instructions)-1]
                instructions[len(instructions)-1] = sentence
                servingSentenceExists = True

        for (word in startWords):
            if (startsWith(sentence, word)):
                instructions[i] = instructions[0]
                instructions[0] = sentence
    if (!servingSentenceExists):
        r = randomInteger(0, len(servingSentencesWithoutSeeds)-1)
        servingSentence = servingSentencesWithoutSeeds[r].sentence
        instructions += servingSentence
    returnString = ""
    counter = 1
    for (sentence in instructions):
        newSentence = ""
        charCounter = 0
        for (ch in sentence):
            if (charCounter>60 and ch==' '):
                charCounter = 0
                newSentence += " " + "\n" + "         "
                if (counter/10==1) newSentence += " "
            else newSentence += charToString(ch)
            charCounter += 1
        sentence = newSentence
        returnString += "      " + integerToString(counter) + ". " + sentence + "\n"
        counter += 1
    return returnString


def makeRandomInstructions(bigVec, ingredientsList):
    returnVec = []
    endSeeds = []
    for ingredient in ingredientsList:
        ingredientSplit = stringSplit(ingredient, " ")
        endSeed = ingredientSplit[len(ingredientSplit)-1]
        endSeeds += endSeed
    endSeedsUsed = []
    for j in xrange(0, len(endSeeds)):
        endSeedUsed = []
        endSeedUsed += endSeeds[j]
        endSeedUsed += "false"
        endSeedsUsed += endSeedUsed

    existUnusedSeeds = True
    emptiesUsed = 0
    iterationCounter1 = 0
    while (existUnusedSeeds):
        if (iterationCounter1>300):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        refinedBigVec = []
        unusedEndSeeds = []
        for j in xrange(0, len(endSeedsUsed)):
            endSeedUsed = endSeedsUsed[j]
            if (endSeedUsed[1]=="false"):
            	unusedEndSeeds += endSeedUsed[0]
        if (len(unusedEndSeeds)==0):
        	break
        for i in xrange(0, len(bigVec)):
            shouldAdd = True
            hasUnusedSeed = False
            for word in bigVec[i].order1EndSeedsInside:
                if (!(word in endSeeds):
                	shouldAdd = False
                if (word in unusedEndSeeds):
                	hasUnusedSeed = True
            if (shouldAdd and hasUnusedSeed):
                refinedBigVec += bigVec[i]
        r = 0
        sentence = ""
        instructionSentence randomInstructSent
        if (refinedBigVec.isEmpty()):
            r = randomInteger(0, len(bigVec)-1)
            randomInstructSent = bigVec[r]
            sentence += randomInstructSent.sentence
            endSeedsInvolved = randomInstructSent.order1EndSeedsInside
            TokenScanner scanner(sentence)
            newSentence = ""
            while (scanner.hasMoreTokens()):
                currentToken = scanner.nextToken()
                r = randomInteger(0, len(unusedEndSeeds)-1)
                if (currentToken in endSeedsInvolved):
                    if (len(unusedEndSeeds)==0):
                        errorVec = []
                        errorVec += "ERROR"
                        return errorVec
                    newSentence += unusedEndSeeds[r]
                    for i in xrange(0, len(endSeedsUsed)):
                        endSeedUsed = endSeedsUsed[i]
                        if (unusedEndSeeds[r]!=endSeedUsed[0]) continue
                        endSeedUsed[1] = "true"
                        endSeedsUsed[i] = endSeedUsed
                    unusedEndSeeds.remove(r)
                else newSentence += currentToken
            sentence = newSentence
        else:
            r = randomInteger(0, len(refinedBigVec)-1)
            randomInstructSent = refinedBigVec[r]
            sentence += randomInstructSent.sentence
        trueCounter = 0
        for i in xrange(0, len(endSeeds)):
            if (vectorContains(randomInstructSent.order1EndSeedsInside, endSeeds[i])):

                endSeedUsed = endSeedsUsed[i]
                endSeedUsed[1] = "true"
                endSeedsUsed[i] = endSeedUsed
            if (endSeedsUsed[i][1]=="true"):
            	trueCounter += 1
        if ((trueCounter+emptiesUsed) == len(endSeeds)):
        	existUnusedSeeds = False
        returnVec += sentence
        iterationCounter1 += 1
    return returnVec


def refineReverseSeedMapKeys(reverseSeedMap):
    for (key in reverseSeedMap.keys()):
        if ("$" in key or "%" in key):
        	reverseSeedMap.remove(key)


def makeRandomIngredientsList(reverseSeedMap, endSeedMap, numIngredients, seedLength, endSeedLength, endSeedSeedLength):
    outputTokens = []
    ingredientList = []

    allEndSeedKeys = endSeedMap.keys()
    #    const Vector<Vector<string>> &allRevSeedKeys = reverseSeedMap.keys()

    usedEndSeedKeys = []
    #    print "ck1\n"
    r = randomInteger(0, len(allEndSeedKeys)-1)
    firstEndSeedKey = allEndSeedKeys[r]
    usedEndSeedKeys += firstEndSeedKey
    firstIngredient = ""
    for (member in firstEndSeedKey):
        firstIngredient += member + " "
    firstIngredient = trimEnd(firstIngredient)
    #    print "ck2\n"
    newKey = []
    oldKey = []
    if (len(firstEndSeedKey)<seedLength) oldKey = firstEndSeedKey
    else oldKey += firstEndSeedKey.subList(0,seedLength)
    iterationCounter = 0
    while (True):
        if (iterationCounter>200):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        possiblePreviousTokens = reverseSeedMap[oldKey]
        numTokens = len(possiblePreviousTokens)
        r = randomInteger(0,numTokens-1)
        previousTokenToBeAdded = possiblePreviousTokens[r]
        if (previousTokenToBeAdded == "%") break
        newFirstIngredient = ""
        if (previousTokenToBeAdded=="/") newFirstIngredient = previousTokenToBeAdded + firstIngredient
        elif (firstIngredient[0]=='/') newFirstIngredient = previousTokenToBeAdded + firstIngredient
        else newFirstIngredient = previousTokenToBeAdded + " " + firstIngredient
        firstIngredient = newFirstIngredient
        newKey += previousTokenToBeAdded
        if (len(oldKey)<seedLength-1) newKey += oldKey
        else newKey += oldKey.subList(0,seedLength-1)
        oldKey = newKey
        newKey.clear()
        iterationCounter += 1
    #    print "ck3\n"
    ingredientList += firstIngredient

    newEndSeedKey = []
    lastEndSeedKey = []
    lastEndSeedKey += firstEndSeedKey
    iterationCounter2 = 0
    for i in xrange(0, numIngredients):
        if (iterationCounter2>200):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        #        print "ck4\n"
        possibleNextEndSeedKeys = []
        if (len(usedEndSeedKeys) >= endSeedSeedLength):
            for j in reversed(xrange(1, endSeedSeedLength+1)):
                seedKey = usedEndSeedKeys[len(usedEndSeedKeys)-j]
                possibleNextEndSeedKeys += endSeedMap[seedKey]
        else:
            for j in xrange(0,  len(usedEndSeedKeys)):
                seedKey = usedEndSeedKeys[j]
                possibleNextEndSeedKeys += endSeedMap[seedKey]
        #        print "ck5\n"
        if (len(possibleNextEndSeedKeys)==0):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        r = randomInteger(0, len(possibleNextEndSeedKeys)-1)
        if (vectorContains(usedEndSeedKeys,possibleNextEndSeedKeys[r])):
            i -= 1
            iterationCounter2 += 1
            continue
        #        print "ck6\n"
        if ("plus" in possibleNextEndSeedKeys[r] or "lengths" in possibleNextEndSeedKeys[r] or "inch" in possibleNextEndSeedKeys[r]):
            i -= 1
            iterationCounter2 += 1
            continue
        newEndSeedKey = possibleNextEndSeedKeys[r]
        usedEndSeedKeys += newEndSeedKey
        newIngredient = ""
        for (member in newEndSeedKey):
            newIngredient += member + " "
        newIngredient = trimEnd(newIngredient)
        newKey = []
        oldKey = []
        #        print "ck7\n"
        if (len(newEndSeedKey)<seedLength) oldKey = newEndSeedKey
        else oldKey += newEndSeedKey.subList(0,seedLength)
        iterationCounter = 0
        while (True):
            if (iterationCounter>200):
                errorVec = []
                errorVec += "ERROR"
                return errorVec
            #            print "ck8\n"
            possiblePreviousTokens = reverseSeedMap[oldKey]
            r = randomInteger(0, len(possiblePreviousTokens)-1)
            if (len(possiblePreviousTokens)==0):
                errorVec = []
                errorVec += "ERROR"
                return errorVec
            previousTokenToBeAdded = possiblePreviousTokens[r]
            #            print "ck9\n"
            if (previousTokenToBeAdded == "%") break
            tempNewIngredient = ""
            if (previousTokenToBeAdded=="/") tempNewIngredient = previousTokenToBeAdded + newIngredient
            elif (newIngredient[0]=='/') tempNewIngredient = previousTokenToBeAdded + newIngredient
            else tempNewIngredient = previousTokenToBeAdded + " " + newIngredient
            newIngredient = tempNewIngredient
            newKey += previousTokenToBeAdded
            if (len(oldKey)<seedLength-1) newKey += oldKey
            else newKey += oldKey.subList(0,seedLength-1)
            oldKey = newKey
            newKey.clear()
            iterationCounter += 1
            #            print "ck10\n"
        lastEndSeedKey = newEndSeedKey
        ingredientList += newIngredient
        iterationCounter2 += 1
        #        print "ck11\n"
    return ingredientList


def vectorContains(vec, word):
    for (member in vec):
        if (word == member) return True
    return False


def vectorContains(superVec, subVec):
    for (member in superVec):
        if (subVec == member) return True
    return False;


def compileAllIngredients(allRecipes, allIngredients, allIngredientsString):
    for i in xrange(0, len(allRecipes)):
        currentRecipe = allRecipes[i]
        recipeIngredients = currentRecipe.getIngredients()
        for (myIngredient in recipeIngredients):
            allIngredients += myIngredient
            line = ""
            if (myIngredient.amount=="NO_LEADING_NUMBER") line = "% "
            else line = "% " + myIngredient.amount + " "
            lastWord = ""
            for (word in myIngredient.wordsInIngredient):
                if (lastWord=="plus" and allRecipes[0].isUnit(word)) line += integerToString(randomInteger(1,10)) + " " + word + " "
                else line += word + " "
                lastWord = word
            line += "\n"
            allIngredientsString += line


def makeIngredientMarkov(allIngredients, allIngredientsString, reverseSeedMap, seedLength, endSeedLength, defaultSeedLength):
    TokenScanner scanner(allIngredientsString)
    scanner.ignoreWhitespace()
    scanner.appendWordCharacters("'")
    tokens = []
    for i in xrange(0, seedLength+1):
        myToken = ""
        tokens += myToken
    tokensEnd = []
    for i in xrange(0, endSeedLength+1):
        myToken = ""
        tokensEnd += myToken
    tokensDefault = []
    for i in xrange(0, defaultSeedLength+1):
        myToken = ""
        tokensDefault += myToken
    currentSeed = []
    currentSeedEnd = []
    currentSeedDefault = []
    while (scanner.hasMoreTokens()):
        for i in xrange(0, seedLength):
            tokens[i] = tokens[i+1]
        for i in xrange(0, endSeedLength):
            tokensEnd[i] = tokensEnd[i+1]
        for i in xrange(0, defaultSeedLength):
            tokensDefault[i] = tokensDefault[i+1]
        tokens[seedLength] = scanner.nextToken()
        tokensEnd[endSeedLength] = tokens[seedLength]
        tokensDefault[defaultSeedLength] = tokens[seedLength]
        currentSeed += tokens[seedLength]
        currentSeedEnd += tokensEnd[endSeedLength]
        currentSeedDefault += tokensDefault[defaultSeedLength]

        if (len(currentSeed) > seedLength):
            currentSeed = currentSeed.subList(1,seedLength)
            if (reverseSeedMap.containsKey(currentSeed)):
                currentVals = reverseSeedMap[currentSeed]
                currentVals += tokens[0]
                reverseSeedMap[currentSeed] = currentVals
            else:
                vals = []
                vals.append(tokens[0])
                reverseSeedMap.append(currentSeed,vals)
        if (len(currentSeedEnd) > endSeedLength):
            currentSeedEnd = currentSeedEnd.subList(1,endSeedLength)

            if (reverseSeedMap.containsKey(currentSeedEnd)):
                currentVals = reverseSeedMap[currentSeedEnd]
                currentVals += tokensEnd[0]
                reverseSeedMap[currentSeedEnd] = currentVals
            else:
                vals = []
                vals.append(tokensEnd[0])
                reverseSeedMap.append(currentSeedEnd,vals)
        if (len(currentSeedDefault) > defaultSeedLength):
            currentSeedDefault = currentSeedDefault.subList(1,defaultSeedLength)

            if (reverseSeedMap.containsKey(currentSeedDefault)):
                currentVals = reverseSeedMap[currentSeedDefault]
                currentVals += tokensDefault[0]
                reverseSeedMap[currentSeedDefault] = currentVals
            else:
                vals = []
                vals.append(tokensDefault[0])
                reverseSeedMap.append(currentSeedDefault,vals)

def makeEndSeedMap(allRecipes, endSeedMap):
    for i in xrange(0, len(allRecipes)):
        currentRecipe = allRecipes[i]
        endSeeds = currentRecipe.getEndSeeds()
        for j in xrange(0, len(endSeeds)):
            key = []
            key += endSeeds[j]
            vals = []
            for k in xrange(0, len(endSeeds):
                if (j==k) break
                else vals += endSeeds[k]
            if (!endSeedMap.containsKey(key)){
                endSeedMap.append(key,vals)
            else:
                currentVals = []
                currentVals = endSeedMap[key]
                vals += currentVals
                endSeedMap[key] = vals

def deleteOneIngredientRecipes(allRecipes):
    newAllRecipes = []
    for i in xrange(0, len(allRecipes)):
        currentRecipe = allRecipes[i]
        if (!(len(currentRecipe.getEndSeeds()) == 1 or len(currentRecipe.getEndSeeds()) == 0)):
            newAllRecipes += currentRecipe
    allRecipes.clear()
    allRecipes = newAllRecipes

def splitRecipes(allRecipes, adjectives, endSeedLength):
    for i in xrange(0, len(allRecipes)):
        #print i
        myRecipe = allRecipes[i]
        myRecipe.removeCaps()
        myRecipe.setName(myRecipe.findTitle())
        myRecipe.setNumServings(myRecipe.findNumServings())
        myRecipe.setAllIngredientsText(myRecipe.findAllIngredients())
        myRecipe.separateIngredients(adjectives)
        myRecipe.separateInstructions()
        myRecipe.findIngredientAmounts()
        myRecipe.findIngredientUnits()
        myRecipe.fillIngredientWords()
        myRecipe.fillEndSeeds(endSeedLength)
        myRecipe.divideInstructionSentences()
        myRecipe.findFinalIngredientWords()
        myRecipe.findSeedsInInstructionSentences()

        allRecipes[i] = myRecipe


def printListOfRecipesIngredients(allRecipes, startingIndex, numToPrint):
    for myRecipe in allRecipes[0:numToPrint]:
        print myRecipe.getName()
        print "-------------------------------"
        myRecipe.printIngredients()
        print "\n\n"



def printRecipeEndSeeds(allRecipes, startingIndex, numToPrint):
    if (startingIndex==-5):
    	startingIndex = 0
    if (numToPrint==-5):
    	numToPrint = len(allRecipes)
    for myRecipe in allRecipes[startingIndex:numToPrint]
        myRecipe.printEndSeeds()
        print "\n\n"



def getAllText(ifstream infile):
    returnText = ""
    chInt = 0
    while ((chInt = infile.get()) != EOF):
        ch = char(chInt)
        returnText += charToString(ch)
    return returnText


def fillRecipes(allRecipes, allText):
    index = 0
    recipeInd = 0
    newLinesSinceLastMakesServes = 100
    while (True):
        if (index == int(allText.length())):
            indEndLastRecipe = allText.length() - 1
            previousRecipe = allRecipes[recipeInd-1]
            lengthOfLastRecipe = indEndLastRecipe - previousRecipe.getIndStartRecipe()
            previousRecipe.setAllRecipeText(allText[previousRecipe.getIndStartRecipe() : lengthOfLastRecipe])
            allRecipes[recipeInd-1] = previousRecipe
            break
        makesOrServes = ""
        if (index < len(allText)-7):
            makesOrServes = allText[index : index + 6]
        if (newLinesSinceLastMakesServes > 5 and (makesOrServes == "MAKES " or makesOrServes == "SERVES")):
            newRecipe = Recipe()
            newLinesSinceLastMakesServes = 0
            indStartRecipe = findIndPreviousTitle(index, allText)
            newRecipe.setIndStartRecipe(indStartRecipe)
            allRecipes += newRecipe

            if (recipeInd != 0):
                indEndLastRecipe = findIndEndLastRecipe(indStartRecipe, allText)
                previousRecipe = allRecipes[recipeInd-1]
                lengthOfLastRecipe = indEndLastRecipe - previousRecipe.getIndStartRecipe()
                previousRecipe.setAllRecipeText(allText[previousRecipe.getIndStartRecipe() : previousRecipe.getIndStartRecipe() + lengthOfLastRecipe])
                previousRecipe.setRecipeCharLength(lengthOfLastRecipe)
                allRecipes[recipeInd-1] = previousRecipe
            recipeInd += 1
        if (allText[index] == '\n'):
        	newLinesSinceLastMakesServes += 1
        index += 1


def findIndEndLastRecipe(indStartRecipe, allText):
    indEndLastRecipe = 0
    currentIndex = indStartRecipe-1
    while (True):
        if (currentIndex == 0):
            indEndLastRecipe = -1
            break
        currentChar = allText[currentIndex]
        if (currentChar == '.'):
            indEndLastRecipe = currentIndex+1
            break
        currentIndex -= 1
    return indEndLastRecipe


def findIndPreviousTitle(index, allText):
    indTitle = 0
    currentIndex = index-1
    possibleIndTitle = -1
    while (True):
        if (currentIndex == 0):
            indTitle = 0
            break
        currentChar = allText[currentIndex]
        previousChar = allText[currentIndex-1]
        if (currentChar == '.' and possibleIndTitle != -1):
            indTitle = possibleIndTitle
            break
        elif (isalpha(currentChar) and islower(currentChar) and previousChar == '\n'):
            possibleIndTitle = currentIndex
        currentIndex -= 1
    return indTitle


def invertMap(map):
    returnMap = {}
    for (key in map.keys()):
        val = map[key]
        returnMap[val] = key
    return returnMap



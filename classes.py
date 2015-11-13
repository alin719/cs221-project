import collections, itertools, Queue
import numpy, scipy, math, random
import os, sys
import tokenize, re, string






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

    VALID_AFTER_WORDS = ["to", "in", "into", "on", "are", ".", ",", ";", "is"]
    VALID_BEFORE_WORDS = ["NUMBERS", "the", "and", "with"]
    NORMAL_UNITS = ["teaspoon", "tablespoon", "pound", "cup", "ounce", \
            "bunch", "strip", "clove", "stalk", "stick", "loaf", \
            "rind", "slice", "sprig", "head", "ear", "can", "pint", \
            "quart", "gallon", "sheet"]
    NORMAL_UNITS_PLURAL = ["teaspoons", "tablespoons", "pounds", "cups", "ounces", \
            "bunches", "strips", "cloves", "stalks", "sticks", "loaves", \
            "rinds", "slices", "sprigs", "heads", "ears", "cans", "pints", \
            "quarts", "gallons", "sheets"]
    ABNORMAL_UNITS = ["Pinch of", "Juice of", "Zest of"]
    DESCRIPTORS = ["large", "small", "whole", "thin", "coarse", "red", "green", \
            "rack", "hot", "medium", "baby", "fresh", "dried", "frozen", \
            "boneless", "skinless", "ripe", "pink", "coarsely chopped", "cold", \
            "minced", "grated", "finely grated", "ground", "hot", "freshly ground"]
    STANDALONES = ["Freshly ground pepper", "Coarse salt", \
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
    INSTRUCTION_VERBS = ["Fill", "Mix", "Place", "Stir", "In", "Process", "Heat", "Whisk", \
            "Combine", "With", "Puree", "Squeeze", "Bring", "Put", "Using", "Toss", "Melt", \
            "Prepare", "Pour", "Preheat", "Soak", "Halve", "Line", "Cut", "Add", "Pulse", \
            "Mash", "Blend", "Sprinkle", "Beat", "Arrange", "Set", "Fit", "Scoop", "Cover"]
    UNIT_TO_VOLUME = {}
    UNIT_TO_VOLUME["cup"] = 237
    UNIT_TO_VOLUME["teaspoon"] = 5
    UNIT_TO_VOLUME["tablespoon"] = 15
    UNIT_TO_VOLUME["pint"] = 473
    UNIT_TO_VOLUME["quart"] = 950
    UNIT_TO_VOLUME["gallon"] = 3800
    UNIT_TO_VOLUME["can"] = 474

    def __init__(self):
        self.name = ""
        self.numServings = 0
        self.numIngredients = 0
        self.numInstructions = 0
        self.instructionsAreNumbered = False
        self.allRecipeText = ""
        self.indStartRecipe = 0
        self.recipeCharLength = 0
        self.allIngredientsText = ""
        self.allInstructionsText = ""
        self.instructionSteps = []
        self.ingredients = []
        self.endSeeds = []
        self.finalIngredientWords = []
        self.goodInstructionSentences = []
        self.servingInstructionSentences = []

    ## Setters
    def setAllRecipeText(self, newAllRecipeText):
        self.allRecipeText = newAllRecipeText
    def setAllIngredientsText(self, newAllIngredientsText):
        self.allIngredientsText = newAllIngredientsText
    def setAllInstructionsText(self, newAllInstructionsText):
        self.allInstructionsText = newAllInstructionsText
    def setName(self, newName):
        self.name = newName
    def setNumServings(self, newNumServings):
        self.numServings = newNumServings
    def setNumInstructions(self, newNumInstructions):
        self.numInstructions = newNumInstructions
    def setNumIngredients(self, newNumIngredients):
        self.numIngredients = newNumIngredients
    def setIndStartRecipe(self, newIndStartRecipe):
        self.indStartRecipe = newIndStartRecipe
    def setRecipeCharLength(self, newRecipeCharLength):
        self.recipeCharLength = newRecipeCharLength
    def setIngredients(self, newIngredients):
        self.ingredients = newIngredients
    def setInstructions(self, newInstructions):
        self.instructions = newInstructions
    def setEndSeeds(self, newEndSeeds):
        self.endSeeds = newEndSeeds
    def setInstructionSteps(self, newInstructionSteps):
        self.instructionSteps = newInstructionSteps

    # Getters 
    def getAllRecipeText(self):
        return self.allRecipeText
    def getAllIngredientsText(self):
        return self.allIngredientsText
    def getAllInstructionsText(self):
        return self.allInstructionsText
    def getName(self):
        return self.name
    def getNumServings(self):
        return self.numServings
    def getNumInstructions(self):
        return self.numInstructions
    def getNumIngredients(self):
        return self.numIngredients
    def getIndStartRecipe(self):
        return self.indStartRecipe
    def getRecipeCharLength(self):
        return self.recipeCharLength
    def getIngredients(self):
        return self.ingredients
    def getInstructions(self):
        return self.instructions
    def getEndSeeds(self):
        return self.endSeeds
    def getInstructionSteps(self):
        return self.instructionSteps
    def getGoodInstructionSentences(self):
        return self.goodInstructionSentences
    def getServingInstructionSentences(self):
        return self.servingInstructionSentences

    # Other Function Implementations */
    def addInstructionStep(self, newInstructionStep):
        self.instructionSteps.append(newInstructionStep)
        return self.instructionSteps

    def fillInstructionSentenceTokens(self):
        for i in xrange(0, len(self.goodInstructionSentences)):
            myInstructionSentence = self.goodInstructionSentences[i]
            myInstructionSentence.tokensInSentence = myInstructionSentence.sentence.split()
            self.goodInstructionSentences[i] = myInstructionSentence

    def divideInstructionSentences(self):
        for i in xrange(0, len(self.instructionSteps)):
            myInstructionStep = self.instructionSteps[i]
            stepText = myInstructionStep.allText
            stepText = stepText.replace(". ", ". @ ")
            sentenceVec = stepText.split("@")
            for j in xrange(0, len(sentenceVec)):
                sentence = sentenceVec[j]
                sentence = sentence.strip()
                if (sentence==""):
                    continue
                newInstructionSentence = InstructionSentence()
                newInstructionSentence.sentence += sentence
                newInstructionSentence.tokensInSentence = newInstructionSentence.sentence.split()
                myInstructionStep.instructionSentences.append(newInstructionSentence)
                myInstructionStep.sentenceStringVec.append(sentence)
            self.instructionSteps[i] = myInstructionStep

    def findFinalIngredientWords(self):
        lastWords = []
        for i in xrange(0, len(self.endSeeds)):
            endSeed = self.endSeeds[i]
            lastWord = endSeed[len(endSeed)-1]
            lastWords += lastWord
            if (len(endSeed)==1):
                continue
            lastWords += endSeed[len(endSeed)-2]
        self.finalIngredientWords = lastWords

    def findSeedsInInstructionSentences(self):
        servingWords = []
        servingWords += "Serve", "serve", "Served", "served"
        for i in xrange(0, len(self.instructionSteps)):
            myInstructionStep = self.instructionSteps[i]
            for j in xrange(0, len(myInstructionStep.instructionSentences)):
                myInstructionSent = myInstructionStep.instructionSentences[j]
                sentence = myInstructionSent.sentence
                myInstructionSent.isServingSentence = False
                sentenceTokens = [t for t in re.split("([^a-zA-Z0-9_\''])", sentence) if t not in ['', ' ']]

                previousPreviousToken = ""
                previousToken = ""
                currentToken = ""
                for trigram in zip(sentenceTokens, sentenceTokens[1:], sentenceTokens[2:]):
                    previousPreviousToken, previousToken, currentToken = trigram
                    if (previousToken in self.finalIngredientWords and \
                            not (previousPreviousToken in self.VALID_BEFORE_WORDS and \
                              currentToken in self.VALID_AFTER_WORDS)):
                        myInstructionSent.isGoodSentence = False
                        break
                    elif (previousToken in self.finalIngredientWords):
                        myInstructionSent.order1EndSeedsInside += previousToken
                        myInstructionSent.isGoodSentence = True
                    else:
                        myInstructionSent.isGoodSentence = True
                    if (previousPreviousToken in servingWords or previousToken in servingWords or currentToken in servingWords):
                        myInstructionSent.isServingSentence = True
                myInstructionSent.sentence = myInstructionSent.sentence.replace("\n", "")
                if (myInstructionSent.isGoodSentence):
                    self.goodInstructionSentences.append(myInstructionSent)
                if (myInstructionSent.isServingSentence):
                    self.servingInstructionSentences.append(myInstructionSent)
                myInstructionStep.instructionSentences[j] = myInstructionSent
            self.instructionSteps[i] = myInstructionStep

    def printGoodSentences(self):
        print self.name
        print "-----------------------------------------"
        for i in xrange(0, len(self.goodInstructionSentences)):
            myInstructionSent = self.goodInstructionSentences[i]
            if (len(myInstructionSent.order1EndSeedsInside)==0):
                continue
            sentence = myInstructionSent.sentence
            sentence = sentence.replace("\n", "")
            print "   Sentence: ", sentence
            print "      Seeds: ", myInstructionSent.order1EndSeedsInside
        print "\n\n"

    def separateInstructions(self):
        myInstructionSteps = []
        if (self.instructionsAreNumbered):
            index = 1
            boundsOfSteps = []
            while (True):
                stepStart1 = ""
                stepStart2 = ""
                stepStart3 = ""
                stepStart4 = ""
                if (index == 1):
                    stepStart1 = "\n" + str(index) + ". "
                else:
                    stepStart1 = " \n" + str(index) + ". "
                    stepStart2 = " \n\n" + str(index) + ". "
                    stepStart3 = " \n\n\n" + str(index) + ". "
                    stepStart4 = " \n\n\n\n" + str(index) + ". "

                officialStepStart = ""
                indexOfStart = self.allInstructionsText.find(stepStart1)
                officialStepStart = stepStart1
                if (indexOfStart==-1):
                    indexOfStart = self.allInstructionsText.find(stepStart2)
                    officialStepStart = stepStart2
                if (indexOfStart==-1):
                    indexOfStart = self.allInstructionsText.find(stepStart3)
                    officialStepStart = stepStart3
                if (indexOfStart==-1):
                    indexOfStart = self.allInstructionsText.find(stepStart4)
                    officialStepStart = stepStart4

                if not len(boundsOfSteps) == 0:
                    boundsOfSteps[index-2].append(indexOfStart)
                if (indexOfStart != -1):
                    indexOfRealStart = indexOfStart + len(officialStepStart)
                    boundOfStep = []
                    boundOfStep.append(indexOfRealStart)
                    boundsOfSteps.append(boundOfStep)
                else:
                    boundsOfLastStep = boundsOfSteps[len(boundsOfSteps)-1]
                    boundsOfLastStep.append(len(self.allInstructionsText)-1)
                    break
                index += 1
            for i in xrange(0, len(boundsOfSteps)):
                boundsOfStep = boundsOfSteps[i]
                newInstructionStep = InstructionStep()
                newInstructionStep.stepNumber = i+1
                newInstructionStep.allText = self.allInstructionsText[boundsOfStep[0] : boundsOfStep[1]]
                newInstructionStep.allText = newInstructionStep.allText.strip()
                myInstructionSteps.append(newInstructionStep)
        else:
            newInstructionStep = InstructionStep()
            newInstructionStep.stepNumber = 0
            newInstructionStep.allText = self.allInstructionsText.strip()
            if newInstructionStep.allText.startswith("\n"):
                newInstructionStep.allText = newInstructionStep.allText[0]
            myInstructionSteps.append(newInstructionStep)
        self.instructionSteps = myInstructionSteps
        return myInstructionSteps

    def printAllInstructionText(self):
        print self.name
        print "------------------------------------------"
        print self.allInstructionsText, "\n\n"

    def printAllInstructionSteps(self):
        print self.name
        print "------------------------------------------"
        i=1
        for iStep in self.instructionSteps:
            print "   Step ", i, ": ", iStep.allText
            i += 1
        print "\n\n"

    # MODIFY THIS SO IT CAN HANDLE AN END SEED LENGTH OF 3
    def fillEndSeeds(self, endSeedLength):
        for i in xrange(0, len(self.ingredients)):
            myIngredient = ingredients[i]
            words = myIngredient.wordsInIngredient
            numWords = len(words)
            if (numWords == 1):
                myIngredient.endSeed += words[0]
            elif (numWords == 2):
                if (isUnit(words[0])):
                    myIngredient.endSeed += words[1]
                else:
                    for j in reversed(xrange(1, endSeedLength+1)):
                        myIngredient.endSeed += words[numWords-j]
            else:
                for j in reversed(xrange(1, endSeedLength+1)):
                    myIngredient.endSeed += words[numWords-j]
            ingredients[i] = myIngredient
            self.endSeeds.append(myIngredient.endSeed)

    def printEndSeeds(self):
        print self.name
        print "---------------------------------"
        for endSeed in self.endSeeds:
            print "   ", endSeed

    def printIngredients(self):
        for i in xrange(0, len(self.ingredients)):
            print "   ", ingredients[i].entireLine
            print "        Amount: ", ingredients[i].amount
            print "        Units: ", ingredients[i].units
            print "        Words: ", ingredients[i].wordsInIngredient
            print "        Non-Unit Words: ", ingredients[i].nonUnitWordsInIngredient
            print "        End Seed: ", ingredients[i].endSeed
        print "   End Seeds:"
        for endSeed in self.endSeeds:
            print "   ", endSeed

    def isUnit(self, word):
        for j in xrange(0, len(self.NORMAL_UNITS)):
            if (word == self.NORMAL_UNITS[j] or word == NORMAL_UNITS_PLURAL[j]):
                return True
        return False

    def vectorContains(self, vec, word):
        return word in vec

    def vectorContains(self, superVec, subVec):
        for member in superVec:
            if (subVec == member):
                return True
        return False

    def findIngredientAmounts(self):
        for i in xrange(0, len(self.ingredients)):
            myIngredient = self.ingredients[i]
            line = myIngredient.entireLine
            if line[0].isdigit():
                numString = ""
                for j in xrange(1, len(line)-3):
                    previousChar = line[j-1]
                    currentChar = line[j]
                    nextChar = line[j+1]
                    nextNextChar = line[j+2]
                    nextNextNextChar = line[j+3]
                    if (previousChar.isdigit() and not nextChar.isdigit() and \
                            currentChar==' ' and not (nextChar=='t' and nextNextChar=='o' and nextNextNextChar==' ')):
                        numString += previousChar
                        break
                    elif (previousChar.isdigit() and not nextChar.isdigit() and (currentChar=='-' or currentChar=='x')):
                        for k in reversed(xrange(0, len(numString))):
                            if (numString[k] == ' '):
                                numString = numString[:-1]   # Used .erase() before
                                break
                            else:
                                numString = numString[:-1]   # Used .erase() before
                        break
                    else:
                        numString += previousChar
                myIngredient.amount = numString
            else:
                myIngredient.amount = "NO_LEADING_NUMBER"
            ingredients[i] = myIngredient

    def findIngredientUnits(self):
        for i in xrange(0, len(self.ingredients)):
            myIngredient = ingredients[i]
            line = myIngredient.entireLine
            myVec = stringSplit(line, " ")
            theUnits = ""
            unitsFound = False
            for i in xrange(0, len(myVec)):
                if (isUnit(myVec[i])):
                    theUnits = myVec[i]
                    unitsFound = True
                    break
                if (unitsFound):
                    break
            myIngredient.units = theUnits
            ingredients[i] = myIngredient

    def fillIngredientWords(self):
        for i in xrange(0, len(self.ingredients)):
            myIngredient = ingredients[i]
            line = myIngredient.entireLine
            wordsInIngredient = stringSplit(line, " ")
            for i in xrange(0, len(wordsInIngredient)):
                word = wordsInIngredient[i]
                newWord = ""
                for ch in word:
                    if not ch.isalpha():
                        newWord += " "
                    else:
                        newWord += ch
                wordsInIngredient[i] = newWord

            ingredientWords = []
            validWord = True
            for i in xrange(0, len(wordsInIngredient)):
                currentWord = wordsInIngredient[i]
                for ch in currentWord:
                    if ch.isdigit():
                        validWord = False
                if validWord:
                    word = wordsInIngredient[i]
                    newWord = ""
                    for ch in word:
                        if (ch==','):
                            newWord += ""
                        elif (ch=='-'):
                            newWord += " "
                        elif not ch.isalpha():
                            newWord += " "
                        else:
                            newWord += ch
                    newWord = newWord.strip()
                    wordSplit = newWord.split(" ")
                    for newWord2 in wordSplit:
                        ingredientWords.append(newWord2)
                validWord = True

            nonUnitIngredientWords = []
            for word in ingredientWords:
                if not isUnit(word):
                    nonUnitIngredientWords += word
            myIngredient.wordsInIngredient = ingredientWords
            myIngredient.nonUnitWordsInIngredient = nonUnitIngredientWords
            ingredients[i] = myIngredient

    def separateIngredients(self, adjectives):
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

            if (previousChar.isalpha()):
                currentWord += previousChar
            elif (currentWord != ""):
                wordsInIngredient += 1
                currentWord = ""

            if (previousChar == '\n' and currentChar.isdigit() and not inParentheses):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (currentIndex==1 and previousChar.isdigit()):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (previousChar == '\n' and currentChar.isupper() and ingredientsStarted and not inParentheses):
                wordsInIngredient = 0
                payAttention = True
                pastComma = False
                ingredientsStarted = True
                newIngredient = Ingredient()
                myIngredients.append(newIngredient)
            elif (ingredientsStarted):
                if (currentChar == ',' and not inParentheses and not (currentWord in adjectives and wordsInIngredient < 2)):
                    payAttention = False
                    pastComma = True

                elif (currentChar == '('):
                    payAttention = False
                    inParentheses = True
                elif (currentChar == ')'):
                    inParentheses = False
                    if not pastComma:
                        payAttention = True

            if (payAttention):
                currentIngredient = myIngredients[len(myIngredients)-1]
                currentLine = currentIngredient.entireLine
                if (currentChar == ')' or (currentChar == ' ' and currentLine[len(currentLine)-1] == ' ')):
                    continue
                if (currentIndex==1 and previousChar.isdigit()):
                    currentLine += previousChar
                if (currentChar != '\n'):
                    currentLine += currentChar
                if (currentIndex==len(ingredientsText)-2 and nextChar.isalpha()):
                    currentLine += nextChar
                currentIngredient.entireLine = currentLine
                myIngredients[len(myIngredients)-1] = currentIngredient
        ingredients = myIngredients

    def removeCapsLinesWithIndices(self, recipeText, capsLineIndices):
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
                if (ind > 0):
                    previousChar = recipeText[ind-1]
                currentChar = recipeText[ind]
                if (ind < (len(recipeText)-2)):
                    nextChar = recipeText[ind+1]
                if (previousChar == '\n' or ind == 0):
                    previousSlashNIndex = ind
                    break
                ind -= 1

            ind = capsLineIndices[i]
            while (True):
                if (ind > 0):
                    previousChar = recipeText[ind-1]
                currentChar = recipeText[ind]
                if (ind < (len(recipeText)-2)):
                    nextChar = recipeText[ind+1]
                if (nextChar == '\n' or ind == len(recipeText)-1):
                    nextSlashNIndex = ind
                    break
                ind += 1

            lineLength = nextSlashNIndex - previousSlashNIndex + 1
            lineString = recipeText[previousSlashNIndex: previousSlashNIndex + lineLength]
            #print lineString
            newRecipeText.replace(lineString, "")
        return newRecipeText

    def removeCaps(self):
        recipeText = self.allRecipeText
        capsLineIndices = []
        inMakeServeLine = False
        belowMakeServeLine = False
        inHeaderLine = False
        for currentIndex in xrange(1, len(recipeText)-2):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            makesOrServes = ""
            if not belowMakeServeLine:
                makesOrServes = recipeText[currentIndex:currentIndex + 6]
                if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                    inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            if (inHeaderLine):
                if (currentChar == '\n'):
                    inHeaderLine = False
            elif (currentChar.isalpha() and nextChar.isalpha() and \
                     currentChar.isupper() and nextChar.isupper() and not inMakeServeLine):
                capsLineIndices.append(currentIndex)
                inHeaderLine = True

        newRecipeText = self.removeCapsLinesWithIndices(recipeText, capsLineIndices)
        self.allRecipeText = newRecipeText
        self.recipeCharLength = len(newRecipeText)

    def findNumServings(self):
        numServingsString = ""
        recipeText = self.allRecipeText
        inMakeServeLine = False
        belowMakeServeLine = False
        for currentIndex in xrange(0, len(recipeText)-7):
            currentChar = recipeText[currentIndex]
            nextChar = recipeText[currentIndex+1]
            makesOrServes = ""
            if (not belowMakeServeLine):
                makesOrServes = recipeText[currentIndex: currentIndex + 6]
                if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                    inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            if (inMakeServeLine):
                if (currentChar.isdigit()):
                    numServingsString += currentChar
                if (numServingsString != "" and not nextChar.isdigit()):
                    break
                if (nextChar == '\n'):
                    if (len(numServingsString) == 0):
                        numServingsString = "10"
                    break
        returnInt = -1
        if (numServingsString != ""):
            returnInt = int(numServingsString)
        return returnInt

    def findTitle(self):
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
                title += currentChar
            currentIndex += 1
        return title

    def findAllIngredients(self):
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
                makesOrServes = recipeText[currentIndex : currentIndex+6]
            if (makesOrServes == "MAKES " or makesOrServes == "SERVES"):
                haveSeenNumbers = False
                inMakeServeLine = True
            if (inMakeServeLine and currentChar == '\n'):
                inMakeServeLine = False
                belowMakeServeLine = True
            elif (belowMakeServeLine):
                if (currentChar.isdigit()):
                    haveSeenNumbers = True
                if (allIngredients == "" and currentChar == '\n'):
                    pass
                else:
                    if ((currentChar == '\n' and nextChar.isalpha() and haveSeenNumbers and \
                         (self.getWord(currentIndex+1, recipeText) in self.INSTRUCTION_VERBS)) or \
                            (currentChar == '\n' and nextChar.isdigit() and nextNextChar == '.')):
                        self.allInstructionsText = recipeText[currentIndex:]
                        self.instructionsAreNumbered = (currentChar == '\n' and nextChar.isdigit() and nextNextChar == '.')
                        break
                    else:
                        allIngredients += currentChar
        return allIngredients

    def getWord(self, currentIndex, recipeText):
        returnWord = ""
        while (True):
            currentChar = recipeText[currentIndex]
            if not currentChar.isalpha():
                break
            else:
                returnWord += currentChar
            currentIndex += 1
        return returnWord
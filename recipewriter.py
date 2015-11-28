"""
 Authors: Austin Ray, Bruno De Martino, Alex Lin
 File: randomwriter.py
 ---------------------
 This file includes all main code for the recipe writer.
"""

import collections, itertools, Queue
import numpy, scipy, math, random
import os, sys
import tokenize, re, string
from classes import *
#include "lexicon.h" ---- set()
#include "queue.h"   ----- Queue()
#include "tokenscanner.h"  ---- tokenize


"""Recipe-Related Function Prototypes

string getAllText(ifstream & infile)
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
void refineReverseSeedMapKeys(Map<Vector<string>,Vector<string>> & reverseSeedMap)
string refineRandomInstructions(Vector<string> & instructions, Vector<instructionSentence> & servingSentencesWithoutSeeds)
"""


# Main Program */
def main(argv):
    res_dirName = "res"
    validEndsOfTitles = ["bread", "oil", "sausage", "cheese", "corn", "salad", "dressing",\
            "stock", "pepper", "bacon", "meat", "mustard", "butter", "water", "melon",\
            "kiwi", "lettuce", "yogurt", "sauce", "rice", "salt", "port", "vinegar"]

    badTitleWords = ["halves", "thighs", "leaves", "stalks", "cloves", "half", "thigh", "leaf", "stalk", "clove", "extract"]

    # Seed length used for weighted-random-writing ingredient lines of
    # already-picked ingredients
    seedLength = 2

    # Seed length used for weighted-random-picking new ingredients
    endSeedLength = 2

    # Collect a set of adjectives from the ./res/adjectives.txt file
    adjectives = gatherAdjectives(res_dirName)
    
    # Splice out the proper adjectives from the adjectives list
    properAdjectives = [adj for adj in adjectives if adj[0].isupper()]

    # Give the user a quick welcome message
    greetUser()

    # Ask the user if they want the program explained
    # to them or not
    if getStartResponse(argv) == "explain":
        explainProgram()

    # Ask user:
    #   - How many ingredients per recipe?
    #   - How many past ingredients factor in to the next ingredient?
    #   - How many recipes should be made?
    #   - Do you want to print the recipes all at once or one by one?
    numIngredients = getNumIngredientsResponse(argv)
    endSeedSeedLength = getEndSeedLengthResponse(argv)
    numRecipesToPrint = getNumRecipesToPrintResponse(argv)
    allAtOnce = getAllAtOnceResponse(argv)

    # Update the user on program progress
    printUpdate(0)

    # Separate complete cookbook text into individual recipe chunks
    allRecipes = separateRawRecipeTexts(res_dirName)

    # Parse each individual recipe into its component parts
    splitRecipes(allRecipes, adjectives, endSeedLength)

    # Delete any recipes that only have one ingredient
    deleteOneIngredientRecipes(allRecipes)

    # Update the user on program progress
    printUpdate(1)
    
    # Add '% ' to beginning of lines, add numbers/amounts
    prepIngredientsForMaps(allRecipes)

    # Make a reverse n-gram map that will allow us to write backwards later
    reverseSeedMap = makeReverseBigramDict(allRecipes)
   
    # Update the user on program progress
    printUpdate(2)

    # refineReverseSeedMapKeys(reverseSeedMap)

    endSeedMap = makeEndSeedMap(allRecipes)

    printUpdate(3)

    singleEndSeeds = set([key[-1] for key in endSeedMap.keys()])

    allGoodSentences = []
    goodSentencesWithSeeds = []
    servingSentences = []
    servingSentencesWithoutSeeds = []
    for i, myRecipe in enumerate(allRecipes):
        myRecipe.fillInstructionSentenceTokens()
        allGoodSentences += myRecipe.goodInstructionSentences
        servingSentences += myRecipe.servingInstructionSentences
        for instSent in myRecipe.goodInstructionSentences:
            if len(instSent.order1EndSeedsInside) != 0:
                containsBadSeed = False
                for token in instSent.tokensInSentence:
                    if (token not in instSent.order1EndSeedsInside) and (token in singleEndSeeds):
                        containsBadSeed = True
                        break
                if not containsBadSeed:
                    goodSentencesWithSeeds.append(instSent)
        for instSent in myRecipe.servingInstructionSentences:
            if len(instSent.order1EndSeedsInside) == 0:
                tokens = instSent.tokensInSentence
                hasSeed = False
                for token in tokens:
                    if (token in singleEndSeeds):
                        hasSeed = True
                        break
                if not hasSeed:
                    servingSentencesWithoutSeeds.append(instSent)

    metaTextToPrint = "               Randomly Generated Recipe Booklet\n"
    metaTextToPrint += "            ----------------------------------------- \n\n"
    print "\n\n\n\n\n\n\n"
    print metaTextToPrint

    markovIngredientsList = []
    shouldStop = False
    if (allAtOnce == "one"):
        shouldStop = True
    for i in xrange(0, numRecipesToPrint):
        if (i>=1 and allAtOnce == "one" and shouldStop):
            continueString = getLine()
        markovIngredientsList = makeRandomIngredientsList(reverseSeedMap, endSeedMap, numIngredients, seedLength, endSeedLength, endSeedSeedLength)
        if (markovIngredientsList[0] == "ERROR"):
            i -= 1
            shouldStop = False
            continue
        lastTokens = []
        for line in markovIngredientsList:
            splitLine = line.split()
            lastTokens.append(splitLine[-1])

        r = randomInteger(0,len(properAdjectives)-1)
        startingWord = properAdjectives[r]
        recipeTitle = ""
        recipeTitle += startingWord + " "
        lastWordInTitle = ""
        lastWordInTitle2 = ""
        for token in lastTokens:
            if ((token in validEndsOfTitles) and not (token in badTitleWords)):
                lastWordInTitle = token
                break
        for token in lastTokens:
            if (token[len(token)-1] == 's' and not (token in badTitleWords)):
                lastWordInTitle = token
                break


        for token in lastTokens:
            if (token in validEndsOfTitles) and (token != lastWordInTitle) and (token not in badTitleWords):
                lastWordInTitle2 = token
                break
        for token in lastTokens:
            if token[len(token)-1] == 's' and token != lastWordInTitle and not (token in badTitleWords):
                lastWordInTitle2 = token
                break
        descriptorWord = ""
        for token in lastTokens:
            if token[len(token)-1] != 's' and token != lastWordInTitle and token != lastWordInTitle2 and not (token in badTitleWords):
                descriptorWord = token
                break

        if (descriptorWord != ""):
            recipeTitle += descriptorWord[0].toupper() + descriptorWord[1] + " "
        if (lastWordInTitle != ""):
            recipeTitle += lastWordInTitle[0].toupper() + lastWordInTitle[0]
        if (lastWordInTitle != "" and lastWordInTitle2 != ""):
            recipeTitle += " with "
        if (lastWordInTitle2 != ""):
            recipeTitle += lastWordInTitle2[0].toupper() + lastWordInTitle2[0]

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
        textToPrint += " (SERVES " + str(numServings) + ")\n"
        #        print "Checkpoint 4"

        textToPrint += "   Ingredients:\n"
        for ingredient in markovIngredientsList:
            if (ingredient[2]=='/'):
                ingredient = ingredient[0] + ingredient[:4]
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

    outfileName = os.path.join(res_dirName, "Random_Recipe_Book.txt")
    with open(outfileName, 'w') as outfile:
        outfile.write(metaTextToPrint)





### Function Implementations ###

##
# The following functions are used to separate the raw cookbook
# text into individual, raw recipe texts 
#    - separateRawRecipeTexts
##
def separateRawRecipeTexts(res_dirName):
    cookbook_fileName = os.path.join(res_dirName, "MarthaStewart-LivingCookbook.txt")
    allText = open(cookbook_fileName, 'r').read()

    # Remove any lines from allText that have any 
    # all-caps words in them that aren't MAKES or SERVES. These 
    # deleted lines are unimportant.
    allText = removeAllCapsLines(allText)

    allRecipes = []
    lines = allText.split('\n')
    numLines = len(lines)
    print "num lines in cookbook: ", len(lines)
    pastFirstRecipe = False
    recipeIndBounds = [0, None]
    for ind, line in enumerate(lines):
        lineWords = line.strip().split()
        if ind == numLines - 1:
            # This accounts for the last recipe
            newRecipe = Recipe()
            newRecipe.allRecipeText = "\n".join(lines[recipeIndBounds[0]:])
            newRecipe.recipeCharLength = len(newRecipe.allRecipeText)
            allRecipes.append(newRecipe)
        elif lineWords != [] and (lineWords[0] in ["MAKES", "SERVES"]):

            # Doesn't work on first iteration, so have to punt
            if pastFirstRecipe == False:
                pastFirstRecipe = True
                continue

            # Create new recipe for insertion into allRecipes list
            newRecipe = Recipe()

            # Find nearest previous non-blank line
            indFirstPrevNonBlank = ind - 1
            while True:
                if indFirstPrevNonBlank <= 0 or lines[indFirstPrevNonBlank] != '':
                    break
                indFirstPrevNonBlank -= 1

            # Find nearest previous blank line after nearest previous non-blank line
            indSecondPrevBlank = indFirstPrevNonBlank - 1
            while True:
                if indSecondPrevBlank <= 0 or lines[indSecondPrevBlank] == '':
                    break
                indSecondPrevBlank -= 1

            recipeIndBounds[1] = indSecondPrevBlank

            newRecipe.allRecipeText = "\n".join(lines[recipeIndBounds[0]:recipeIndBounds[1]])
            newRecipe.recipeCharLength = len(newRecipe.allRecipeText)
            allRecipes.append(newRecipe)

            recipeIndBounds[0] = recipeIndBounds[1]
    allRecipes = [recipe for recipe in allRecipes if recipe.allRecipeText != '']
    print "num recipes: ", len(allRecipes)
    return allRecipes

##
# Function: Recipe::removeAllCapsLines
# ------------------------------------
# Remove any lines from the text that don't have the all-caps words
# MAKES or SERVES. These deleted lines are unimportant.
##
def removeAllCapsLines(text):
    newText = []
    lines = [(line, line.strip().split(" ")) for line in text.split('\n')]
    for line, lineWords in lines:
        allCapsWords = [word for word in lineWords if word.isupper()]
        if allCapsWords == [] or lineWords[0] in ["MAKES", "SERVES"]:
            newText += [line]
    newText = "\n".join(newText)
    return newText

def splitRecipes(allRecipes, adjectives, endSeedLength):
    # for recipe in allRecipes[:3]:
    #     print len(recipe.allRecipeText)
    # sys.exit()
    for i, myRecipe in enumerate(allRecipes):

        # Find the title of this recipe in myRecipe.allRecipeText and set
        # myRecipe.name equal to that title.
        myRecipe.findAndSetTitle()

        # Find and set the number of servings this recipe makes.
        myRecipe.findAndSetNumServings()

        # Split myRecipe.allRecipeText into myRecipe.allIngredientsText
        # and myRecipe.allInstructionsText
        myRecipe.splitIngredientsInstructionText()

        # myRecipe.printAllInstructionText()
        # myRecipe.printAllIngredientsText()

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

# def makeIngredientMarkov(allIngredients, allIngredientsString, reverseSeedMap, seedLength, endSeedLength, defaultSeedLength=1):
#     allIngredientsStringTokens = [t for t in re.split("([^a-zA-Z0-9_\''])", allIngredientsString) if t not in ['', ' ']]

#     tokens = ["" for _ in xrange(0, seedLength+1)]

#     tokensEnd = ["" for _ in xrange(0, endSeedLength+1)]

#     tokensDefault = ["" for _ in xrange(0, defaultSeedLength+1)]

#     currentSeed = []
#     currentSeedEnd = []
#     currentSeedDefault = []
#     for token in allIngredientsStringTokens:
#         for i in xrange(0, seedLength):
#             tokens[i] = tokens[i+1]
#         for i in xrange(0, endSeedLength):
#             tokensEnd[i] = tokensEnd[i+1]
#         for i in xrange(0, defaultSeedLength):
#             tokensDefault[i] = tokensDefault[i+1]
#         tokens[seedLength] = token
#         tokensEnd[endSeedLength] = tokens[seedLength]
#         tokensDefault[defaultSeedLength] = tokens[seedLength]
#         currentSeed += tokens[seedLength]
#         currentSeedEnd += tokensEnd[endSeedLength]
#         currentSeedDefault += tokensDefault[defaultSeedLength]

#         if (len(currentSeed) > seedLength):
#             currentSeed = currentSeed.subList(1,seedLength)
#             if (reverseSeedMap.containsKey(currentSeed)):
#                 currentVals = reverseSeedMap[currentSeed]
#                 currentVals += tokens[0]
#                 reverseSeedMap[currentSeed] = currentVals
#             else:
#                 vals = []
#                 vals.append(tokens[0])
#                 reverseSeedMap[currentSeed] = vals

#         if (len(currentSeedEnd) > endSeedLength):
#             currentSeedEnd = currentSeedEnd.subList(1,endSeedLength)

#             if (reverseSeedMap.containsKey(currentSeedEnd)):
#                 currentVals = reverseSeedMap[currentSeedEnd]
#                 currentVals += tokensEnd[0]
#                 reverseSeedMap[currentSeedEnd] = currentVals
#             else:
#                 vals = []
#                 vals.append(tokensEnd[0])
#                 reverseSeedMap.append(currentSeedEnd,vals)

#         if (len(currentSeedDefault) > defaultSeedLength):
#             currentSeedDefault = currentSeedDefault.subList(1,defaultSeedLength)

#             if (reverseSeedMap.containsKey(currentSeedDefault)):
#                 currentVals = reverseSeedMap[currentSeedDefault]
#                 currentVals += tokensDefault[0]
#                 reverseSeedMap[currentSeedDefault] = currentVals
#             else:
#                 vals = []
#                 vals.append(tokensDefault[0])
#                 reverseSeedMap[currentSeedDefault] = vals

def makeReverseBigramDict(allRecipes):
    reverseBigramDict = {}
    for recipe in allRecipes:
        for ingredient in recipe.ingredients:
            ingWords = ingredient.cleanWordsInIngredient
            for word1, word2 in zip(ingWords[:], ingWords[1:]):
                reverseBigramDict[word2] = reverseBigramDict.get(word2, []) + [word1]

    return reverseBigramDict




# def refineReverseSeedMapKeys(reverseSeedMap):
#     for key in reverseSeedMap.keys():
#         if "$" in key or "%" in key:
#             reverseSeedMap.pop(key, None)


# Function: makeEndSeedMap
# ------------------------
# Makes a map from all end seeds to the other end seeds they've been seen with.
# Ex:
#  - endSeedMap originally is {}
#  - First recipe has large carrots, ground pepper, and grilled chicken as ingredients
#  - After processing first recipe, endSeedMap is:
#       - {("large", "carrots"): [("ground", "pepper"), ("grilled", "chicken")],
#          ("ground", "pepper"): [("large", "carrots"), ("grilled", "chicken")],
#          ("grilled", "chicken"): [("ground", "pepper"), ("large", "carrots")]
#          }
def makeEndSeedMap(allRecipes):
    endSeedMap = {}
    for recipe in allRecipes:
        endSeeds = recipe.endSeeds
        for endSeed in endSeeds:
            otherEndSeeds = [seed for seed in endSeeds if seed != endSeed]
            endSeedMap[endSeed] = endSeedMap.get(endSeed, []) + otherEndSeeds

    del endSeedMap[tuple()]

    return endSeedMap


## 
# Function: compileAllIngredients
# -------------------------------
# Do some adjustments to the ingredients, adding % signs
# to the beginning of the ingredient lines and adding in
# some numbers (amounts).
##
def prepIngredientsForMaps(allRecipes):
    for i, recipe in enumerate(allRecipes):
        for j, myIngredient in enumerate(recipe.ingredients):
            line = "% "
            if myIngredient.amount != "NO_LEADING_NUMBER":
                line += myIngredient.amount + " "

            lastWord = ""
            for word in myIngredient.wordsInIngredient:
                if lastWord == "plus" and allRecipes[0].isUnit(word):
                    line += str(random.randint(1,10)) + " "
                line += word + " "
                lastWord = word
            line += "\n"

            myIngredient.cleanWordsInIngredient = line.split(" ")
            myIngredient.cleanLine = line
            recipe.ingredients[j] = myIngredient
        allRecipes[i] = recipe

##
# Function: deleteOneIngredientRecipes
# ------------------------------------
# allRecipes will have no recipes with only 1 ingredient
# after this function is executed.
##
def deleteOneIngredientRecipes(allRecipes):
    for i in reversed(xrange(0, len(allRecipes))):
        currentRecipe = allRecipes[i]
        numEndSeeds = len(currentRecipe.getEndSeeds())
        if numEndSeeds == 1 or numEndSeeds == 0:
            allRecipes.pop(i)


def refineRandomInstructions(instructions, servingSentencesWithoutSeeds):
    serveSentence = ""
    startSentence = ""
    servingWords = ["Serve", "serve", "Served", "served"]
    startWords = ["Add", "Mix", "Combine", "In", "Prepare", "Preheat", "Blend", "Using", "Place", "Melt", "Slice", "Halve", "Heat"]
    servingSentenceExists = False
    for i in xrange(0, len(instructions)):
        sentence = instructions[i]

        for word in servingWords:
            if (stringContains(sentence,word)):
                instructions[i] = instructions[len(instructions)-1]
                instructions[len(instructions)-1] = sentence
                servingSentenceExists = True

        for word in startWords:
            if sentence.startswith(word):
                instructions[i] = instructions[0]
                instructions[0] = sentence
    if (not servingSentenceExists):
        r = randomInteger(0, len(servingSentencesWithoutSeeds)-1)
        servingSentence = servingSentencesWithoutSeeds[r].sentence
        instructions.append(servingSentence)
    returnString = ""
    counter = 1
    for sentence in instructions:
        newSentence = ""
        charCounter = 0
        for ch in sentence:
            if (charCounter>60 and ch==' '):
                charCounter = 0
                newSentence += " " + "\n" + "         "
                if (counter/10==1):
                    newSentence += " "
            else:
                newSentence += ch
            charCounter += 1
        sentence = newSentence
        returnString += "      " + str(counter) + ". " + sentence + "\n"
        counter += 1
    return returnString


def makeRandomInstructions(bigVec, ingredientsList):
    returnVec = []
    endSeeds = []
    for ingredient in ingredientsList:
        ingredientSplit = ingredient.split(" ")
        endSeed = ingredientSplit[-1]
        endSeeds.append(endSeed)
    endSeedsUsed = []
    for j in xrange(0, len(endSeeds)):
        endSeedUsed = []
        endSeedUsed.append(endSeeds[j])
        endSeedUsed.append("false")
        endSeedsUsed.append(endSeedUsed)

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
                unusedEndSeeds.append(endSeedUsed[0])
        if (len(unusedEndSeeds)==0):
            break
        for i in xrange(0, len(bigVec)):
            shouldAdd = True
            hasUnusedSeed = False
            for word in bigVec[i].order1EndSeedsInside:
                if word not in endSeeds:
                    shouldAdd = False
                if word in unusedEndSeeds:
                    hasUnusedSeed = True
            if shouldAdd and hasUnusedSeed:
                refinedBigVec.append(bigVec[i])
        r = 0
        sentence = ""
        randomInstructSent = InstructionSentence()
        if len(refinedBigVec) == 0:
            r = random.randint(0, len(bigVec)-1)
            randomInstructSent = bigVec[r]
            sentence += randomInstructSent.sentence
            endSeedsInvolved = randomInstructSent.order1EndSeedsInside
            splitSentence = sentence.split()
            while currentToken in splitSentence:
                r = randomInteger(0, len(unusedEndSeeds)-1)
                if (currentToken in endSeedsInvolved):
                    if (len(unusedEndSeeds)==0):
                        errorVec = []
                        errorVec += "ERROR"
                        return errorVec
                    newSentence += unusedEndSeeds[r]
                    for i in xrange(0, len(endSeedsUsed)):
                        endSeedUsed = endSeedsUsed[i]
                        if (unusedEndSeeds[r]!=endSeedUsed[0]):
                            continue
                        endSeedUsed[1] = "true"
                        endSeedsUsed[i] = endSeedUsed
                    unusedEndSeeds.remove(r)
                else:
                    newSentence += currentToken
            sentence = newSentence
        else:
            r = random.randint(0, len(refinedBigVec)-1)
            randomInstructSent = refinedBigVec[r]
            sentence += randomInstructSent.sentence
        trueCounter = 0
        for i in xrange(0, len(endSeeds)):
            if endSeeds[i] in randomInstructSent.order1EndSeedsInside:

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


def makeRandomIngredientsList(reverseSeedMap, endSeedMap, numIngredients, seedLength, endSeedLength, endSeedSeedLength):
    outputTokens = []
    ingredientList = []

    allEndSeedKeys = endSeedMap.keys()
    allRevSeedKeys = reverseSeedMap.keys()

    usedEndSeedKeys = []
    print "allEndSeedKeys length: ", len(allEndSeedKeys)
    r = random.randint(0, len(allEndSeedKeys)-1)
    firstEndSeedKey = allEndSeedKeys[r]
    usedEndSeedKeys.append(firstEndSeedKey)
    firstIngredient = ""
    for member in firstEndSeedKey:
        firstIngredient += member + " "
    firstIngredient = firstIngredient.rstrip()
    newKey = []
    oldKey = []
    if (len(firstEndSeedKey) < seedLength):
        oldKey = firstEndSeedKey
    else:
        oldKey.append(firstEndSeedKey.subList(0,seedLength))
    iterationCounter = 0
    while (True):
        if (iterationCounter>200):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        possiblePreviousTokens = reverseSeedMap[oldKey]
        numTokens = len(possiblePreviousTokens)
        r = random.randint(0, numTokens-1)
        previousTokenToBeAdded = possiblePreviousTokens[r]
        if (previousTokenToBeAdded == "%"):
            break
        newFirstIngredient = ""
        if (previousTokenToBeAdded=="/"):
            newFirstIngredient = previousTokenToBeAdded + firstIngredient
        elif (firstIngredient[0]=='/'):
            newFirstIngredient = previousTokenToBeAdded + firstIngredient
        else:
            newFirstIngredient = previousTokenToBeAdded + " " + firstIngredient
        firstIngredient = newFirstIngredient
        newKey.append(previousTokenToBeAdded)
        if (len(oldKey)<seedLength-1):
            newKey += oldKey
        else:
            newKey += oldKey.subList(0,seedLength-1)
        oldKey = newKey
        newKey.clear()
        iterationCounter += 1
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
        possibleNextEndSeedKeys = []
        if (len(usedEndSeedKeys) >= endSeedSeedLength):
            for j in reversed(xrange(1, endSeedSeedLength+1)):
                seedKey = usedEndSeedKeys[len(usedEndSeedKeys)-j]
                possibleNextEndSeedKeys += endSeedMap[seedKey]
        else:
            for j in xrange(0,  len(usedEndSeedKeys)):
                seedKey = usedEndSeedKeys[j]
                possibleNextEndSeedKeys += endSeedMap[seedKey]
        if (len(possibleNextEndSeedKeys)==0):
            errorVec = []
            errorVec += "ERROR"
            return errorVec
        r = random.randint(0, len(possibleNextEndSeedKeys)-1)
        if possibleNextEndSeedKeys[r] in usedEndSeedKeys:
            i -= 1
            iterationCounter2 += 1
            continue
        if ("plus" in possibleNextEndSeedKeys[r] or "lengths" in possibleNextEndSeedKeys[r] or "inch" in possibleNextEndSeedKeys[r]):
            i -= 1
            iterationCounter2 += 1
            continue
        newEndSeedKey = possibleNextEndSeedKeys[r]
        usedEndSeedKeys += newEndSeedKey
        newIngredient = ""
        for member in newEndSeedKey:
            newIngredient += member + " "
        newIngredient = trimEnd(newIngredient)
        newKey = []
        oldKey = []
        if (len(newEndSeedKey) < seedLength):
            oldKey = newEndSeedKey
        else:
            oldKey += newEndSeedKey.subList(0,seedLength)
        iterationCounter = 0
        while (True):
            if (iterationCounter>200):
                errorVec = []
                errorVec += "ERROR"
                return errorVec
            possiblePreviousTokens = reverseSeedMap[oldKey]
            r = random.randint(0, len(possiblePreviousTokens)-1)
            if len(possiblePreviousTokens) == 0:
                errorVec = []
                errorVec += "ERROR"
                return errorVec
            previousTokenToBeAdded = possiblePreviousTokens[r]
            if (previousTokenToBeAdded == "%"):
                break
            tempNewIngredient = ""
            if (previousTokenToBeAdded=="/"):
                tempNewIngredient = previousTokenToBeAdded + newIngredient
            elif (newIngredient[0]=='/'):
                tempNewIngredient = previousTokenToBeAdded + newIngredient
            else:
                tempNewIngredient = previousTokenToBeAdded + " " + newIngredient
            newIngredient = tempNewIngredient
            newKey += previousTokenToBeAdded
            if (len(oldKey) < seedLength-1):
                newKey += oldKey
            else:
                newKey += oldKey.subList(0,seedLength-1)
            oldKey = newKey
            newKey.clear()
            iterationCounter += 1
        lastEndSeedKey = newEndSeedKey
        ingredientList += newIngredient
        iterationCounter2 += 1
    return ingredientList




















##
# Functional Group: Utility
###########################
# List of functions:
#   - invertMap
##
def invertMap(map):
    returnMap = {}
    for key in map.keys():
        val = map[key]
        returnMap[val] = key
    return returnMap




##
# Functional Group: Reading and Writing to Files
################################################
# List of functions:
#   - gatherAdjectives
##
def gatherAdjectives(res_dirName):
    adjectives = set()
    adj_filename = os.path.join(res_dirName, "adjectives.txt")
    with open(adj_filename) as f:
        for adj in f:
            adjectives.add(adj)
    return adjectives




##
# Functional Group: User-Interaction
####################################
# List of functions:
#   - greetUser
#   - explainProgram
#   - printUpdate
#
#   - printListOfRecipesIngredients
#   - printRecipeEndSeeds
#   
#   - getNumIngredientsResponse
#   - getStartResponse
#   - getEndSeedLengthResponse
#   - getNumRecipesToPrintResponse
#   - getAllAtOnceResponse
##
def greetUser():
    greet = "            Random Recipe Writer | Austin Ray, Bruno De Martino, Alex Lin\n"
    greet += "   -----------------------------------------------------------------------------\n\n"
    greet += "   Hello there! I am a random recipe writer! Thanks for checking me out!\n"
    greet += "   I am able to create random recipes for you based on the recipes found in\n"
    greet += "   The Martha Stewart Living Cookbook\" by using Markov chains. If you want to\n"
    greet += "   know how I do this, enter \"explain\", otherwise enter \"start\" to begin: "
    print greet

def explainProgram():
    print "\n\n   -----------------------------Program Explanation-----------------------------\n"
    print "   ", "   The first thing I do is separate all of Martha's recipes into C++ objects."
    print "   ", "Next, I do some refinement on each recipe, separating ingredients from"
    print "   ", "instructions, separating ingredients from each other, etc. After that,"
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

def printUpdate(updateNum):
    if updateNum == 0:
        print "\n\n   -------------------------------Main Program----------------------------------\n"
        print "\n   ", "I'm going to generate your recipes now. This might take a minute...\n\n"
    elif updateNum == 1:
        print "   ", "...Making progress..."
    elif updateNum == 2:
        print "   ", "...Still working..."
    elif updateNum == 3:
        print "   ", "...Can't be much longer now..."

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
    for myRecipe in allRecipes[startingIndex:numToPrint]:
        myRecipe.printEndSeeds()
        print "\n\n"

def getNumIngredientsResponse(argv):
    numIngredients = 0
    if argv[1] in ["-d", "--default"]:
        numIngredients = 10
    elif len(argv) > 2:
        numIngredients = int(argv[2])
    else:
        while (True):
            numIngredients = int(raw_input("   Enter the desired number of ingredients per recipe (5-15 allowed): "))
            if (numIngredients<5 or numIngredients>15):
                print "\n   Invalid number of ingredients. Try again.\n"
                continue
            break
    return numIngredients

def getStartResponse(argv):
    start = ""
    if argv[1] in ["-d", "--default"]:
        start = "start"
    elif len(argv) > 1:
        start = argv[1]
    else:
        start = raw_input("")
    return start

def getEndSeedLengthResponse(argv):
    endSeedSeedLength = 0
    if argv[1] in ["-d", "--default"]:
        endSeedSeedLength = 3
    elif len(argv) > 3:
        endSeedSeedLength = int(argv[3])
    else:
        while (True):
            endSeedSeedLength = int(raw_input("   Enter ingredient similarity within recipes (1-5 allowed, 5 = very similar): "))
            if (endSeedSeedLength<1 or endSeedSeedLength>5):
                print "\n   Invalid ingredient similarity. Try again.\n"
                continue
            break
    return endSeedSeedLength

def getNumRecipesToPrintResponse(argv):
    numRecipesToPrint = 0
    if argv[1] in ["-d", "--default"]:
        numRecipesToPrint = 20
    elif len(argv) > 4:
        numRecipesToPrint = int(argv[4])
    else:
        while (True):
            numRecipesToPrint = int(raw_input("   Enter the number of recipes you want (1-100 allowed): "))
            if (numRecipesToPrint<1 or numRecipesToPrint>100):
                print "\n   Invalid number of recipes. Try again.\n"
                continue
            break
    return numRecipesToPrint

def getAllAtOnceResponse(argv):
    allAtOnce = ""
    if argv[1] in ["-d", "--default"]:
        allAtOnce = "all"
    elif len(argv) > 5:
        allAtOnce = argv[5]
    else:
        while (True):
            allAtOnce = raw_input("   Do you want to print recipes one by one, or all at once?\n   (Enter either \"one\" or \"all\"): ")
            if (not (allAtOnce=="one") and not (allAtOnce=="all")):
                print "\n   Invalid input. Try again.\n"
                continue
            elif (allAtOnce=="one"):
                print "\n   Got it. Press Enter after each recipe prints to get the next one."
            break






# If called from command line, call the main() function
if __name__ == "__main__":
    #main(sys.argv)
    main(sys.argv + ["-d"])

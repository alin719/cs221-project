/*
 * File: RandomWriter.cpp
 * ----------------------
 * Name: Austin Ray
 * Section: Thursday 2:15PM, Justin Salloum
 * This file is my (Austin Ray) submission for the Random
 * Writer Contest.
 *
 * THIS FILE IS NOT WELL COMMENTED OR CLEANED UP
 * However, if you run the application, I print out
 * a basic explanation of my methodology. So I recommend
 * just running the application.
 *
 * I can comment and clean up this code to turn in a
 * more approachable copy, but the functionality of
 * this submission is final - the program will
 * work the same.
 */

#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <vector>
#include "simpio.h"
#include "map.h"
#include "console.h"
#include "lexicon.h"
#include "queue.h"
#include "filelib.h"
#include "strlib.h"
#include "vector.h"
#include "random.h"
#include "tokenscanner.h"
using namespace std;

/* Data Structures */
struct ingredient {
    string amount;
    string units;
    string ingredientName;
    string entireLine; //Contains amount, units, and ingredient name
    string lineWithoutAmount;
    Vector<string> wordsInIngredient;
    Vector<string> nonUnitWordsInIngredient;
    Vector<string> endSeed;
};

struct instructionSentence {
    bool isGoodSentence;
    bool isServingSentence;
    string firstWord;
    string sentence;
    string sentenceSubbed;
    Vector<string> order1EndSeedsInside;
    Vector<Vector<string>> order2EndSeedsInside;
    Vector<string> nonUnitWordsInIngredient;
    Vector<string> endSeed;
    Vector<string> tokensInSentence;
};

struct instructionStep {
    int stepNumber;
    int numSentences;
    string allText;
    string allTextEdited;
    Vector<instructionSentence> instructionSentences;
    Vector<string> sentenceStringVec;
};


/* Class: Recipe
 * Usage: Recipe myRecipe;
 * ------------------------------------------------
 * Recipe contains the ingredients, name, serving size
 * and instructions for a recipe. It also implements
 * very useful functions for the whole program.
 * ------------------------------------------------
 */
class Recipe {
private:
    string name;
    string allRecipeText;
    string allIngredientsText;
    string allInstructionsText;
    string allInstructionsTextEdited;
    int numServings;
    int numInstructions;
    int numIngredients;
    int indStartRecipe;
    int recipeCharLength;
    bool instructionsAreNumbered;
    Vector<ingredient> ingredients;
    Vector<instructionStep> instructionSteps;
    Vector<Vector<string>> endSeeds;
    Vector<instructionSentence> goodInstructionSentences;
    Vector<instructionSentence> servingInstructionSentences;
    Vector<string> finalIngredientWords;
    Vector<string> instructions;
    Vector<string> NORMAL_UNITS;
    Vector<string> NORMAL_UNITS_PLURAL;
    Vector<string> ABNORMAL_UNITS;
    Vector<string> DESCRIPTORS;
    Vector<string> STANDALONES;
    Vector<string> INSTRUCTION_VERBS;
    Vector<string> VALID_AFTER_WORDS;
    Vector<string> VALID_BEFORE_WORDS;
    Map<string,int> UNIT_TO_VOLUME;    //Volume in milliliters (cc, cm^3)


public:
    Recipe() {
        name = "";
        numServings = 0;
        numIngredients = 0;
        numInstructions = 0;
        allRecipeText = "";
        indStartRecipe = 0;
        recipeCharLength = 0;
        allIngredientsText = "";
        allInstructionsText = "";
        VALID_AFTER_WORDS += "to", "in", "into", "on", "are", ".", ",", ";", "is";
        VALID_BEFORE_WORDS += "NUMBERS", "the", "and", "with";
        NORMAL_UNITS += "teaspoon", "tablespoon", "pound", "cup", "ounce",
                "bunch", "strip", "clove", "stalk", "stick", "loaf",
                "rind", "slice", "sprig", "head", "ear", "can", "pint",
                "quart", "gallon", "sheet";
        NORMAL_UNITS_PLURAL += "teaspoons", "tablespoons", "pounds", "cups", "ounces",
                "bunches", "strips", "cloves", "stalks", "sticks", "loaves",
                "rinds", "slices", "sprigs", "heads", "ears", "cans", "pints",
                "quarts", "gallons", "sheets";
        ABNORMAL_UNITS += "Pinch of", "Juice of", "Zest of";
        DESCRIPTORS += "large", "small", "whole", "thin", "coarse", "red", "green",
                "rack", "hot", "medium", "baby", "fresh", "dried", "frozen",
                "boneless", "skinless", "ripe", "pink", "coarsely chopped", "cold",
                "minced", "grated", "finely grated", "ground", "hot", "freshly ground";
        STANDALONES += "Freshly ground pepper", "Coarse salt",
                "Coarse salt and freshly ground pepper",
                "Fresh tarragon and tarragon flowers",
                "Creamy Tarragon Vinaigrette",
                "Freshly ground black pepper",
                "Canola oil",
                "Coarse salt and freshly ground black pepper",
                "Lime wedges",
                "Cooking spray",
                "Cold water"
                "Crushed Ice";
        INSTRUCTION_VERBS += "Fill", "Mix", "Place", "Stir", "In", "Process", "Heat", "Whisk",
                "Combine", "With", "Puree", "Squeeze", "Bring", "Put", "Using", "Toss", "Melt",
                "Prepare", "Pour", "Preheat", "Soak", "Halve", "Line", "Cut", "Add", "Pulse",
                "Mash", "Blend", "Sprinkle", "Beat", "Arrange", "Set", "Fit", "Scoop", "Cover";
        UNIT_TO_VOLUME["cup"] = 237;
        UNIT_TO_VOLUME["teaspoon"] = 5;
        UNIT_TO_VOLUME["tablespoon"] = 15;
        UNIT_TO_VOLUME["pint"] = 473;
        UNIT_TO_VOLUME["quart"] = 950;
        UNIT_TO_VOLUME["gallon"] = 3800;
        UNIT_TO_VOLUME["can"] = 474;
    }

    /* Setters */
    void setAllRecipeText(string newAllRecipeText) {
        allRecipeText = newAllRecipeText;
    }
    void setAllIngredientsText(string newAllIngredientsText) {
        allIngredientsText = newAllIngredientsText;
    }
    void setAllInstructionsText(string newAllInstructionsText) {
        allInstructionsText = newAllInstructionsText;
    }
    void setName(string newName) {
        name = newName;
    }
    void setNumServings(int newNumServings) {
        numServings = newNumServings;
    }
    void setNumInstructions(int newNumInstructions) {
        numInstructions = newNumInstructions;
    }
    void setNumIngredients(int newNumIngredients) {
        numIngredients = newNumIngredients;
    }
    void setIndStartRecipe(int newIndStartRecipe) {
        indStartRecipe = newIndStartRecipe;
    }
    void setRecipeCharLength(int newRecipeCharLength) {
        recipeCharLength = newRecipeCharLength;
    }
    void setIngredients(Vector<ingredient> & newIngredients) {
        ingredients = newIngredients;
    }
    void setInstructions(Vector<string> & newInstructions) {
        instructions = newInstructions;
    }
    void setEndSeeds(Vector<Vector<string>> & newEndSeeds) {
        endSeeds = newEndSeeds;
    }
    void setInstructionSteps(Vector<instructionStep> & newInstructionSteps) {
        instructionSteps = newInstructionSteps;
    }

    /* Getters */
    string getAllRecipeText() {
        return allRecipeText;
    }
    string getAllIngredientsText() {
        return allIngredientsText;
    }
    string getAllInstructionsText() {
        return allInstructionsText;
    }
    string getName() {
        return name;
    }
    int getNumServings() {
        return numServings;
    }
    int getNumInstructions() {
        return numInstructions;
    }
    int getNumIngredients() {
        return numIngredients;
    }
    int getIndStartRecipe() {
        return indStartRecipe;
    }
    int getRecipeCharLength() {
        return recipeCharLength;
    }
    Vector<ingredient> getIngredients() {
        return ingredients;
    }
    Vector<string> getInstructions() {
        return instructions;
    }
    Vector<Vector<string>> getEndSeeds() {
        return endSeeds;
    }
    Vector<instructionStep> getInstructionSteps() {
        return instructionSteps;
    }
    Vector<instructionSentence> getGoodInstructionSentences() {
        return goodInstructionSentences;
    }
    Vector<instructionSentence> getServingInstructionSentences() {
        return servingInstructionSentences;
    }

    /* Other Function Implementations */
    Vector<instructionStep> addInstructionStep(instructionStep newInstructionStep) {
        instructionSteps += newInstructionStep;
        return instructionSteps;
    }

    void fillInstructionSentenceTokens() {
        for (int i=0; i<goodInstructionSentences.size(); i++) {
            instructionSentence myInstructionSentence = goodInstructionSentences[i];
            TokenScanner scanner(myInstructionSentence.sentence);
            while (scanner.hasMoreTokens()) {
                string currentToken = scanner.nextToken();
                myInstructionSentence.tokensInSentence += currentToken;
            }
            goodInstructionSentences[i] = myInstructionSentence;
        }
    }

    void divideInstructionSentences() {
        for (int i=0; i<instructionSteps.size(); i++) {
            instructionStep myInstructionStep = instructionSteps[i];
            string stepText = myInstructionStep.allText;
            stepText = stringReplace(stepText, string(". "), string(". @ "));
            std::vector<std::string> sentenceVec = stringSplit(stepText, "@");
            for (int j=0; j<int(sentenceVec.size()); j++) {
                string sentence = sentenceVec[j];
                sentence = trim(sentence);
                if (sentence=="") continue;
                instructionSentence newInstructionSentence;
                newInstructionSentence.sentence += sentence;
                TokenScanner scanner(newInstructionSentence.sentence);
                while (scanner.hasMoreTokens()) {
                    string currentToken = scanner.nextToken();
                    newInstructionSentence.tokensInSentence += currentToken;
                }
                myInstructionStep.instructionSentences.add(newInstructionSentence);
                myInstructionStep.sentenceStringVec.add(sentence);
            }
            instructionSteps[i] = myInstructionStep;
        }
    }

    void findFinalIngredientWords() {
        Vector<string> lastWords;
        for (int i=0; i<endSeeds.size(); i++) {
            Vector<string> endSeed = endSeeds[i];
            string lastWord = endSeed[endSeed.size()-1];
            lastWords += lastWord;
            if (endSeed.size()==1) continue;
            lastWords += endSeed[endSeed.size()-2];
        }
        finalIngredientWords = lastWords;
    }

    void findSeedsInInstructionSentences() {
        Vector<string> servingWords;
        servingWords += "Serve", "serve", "Served", "served";
        for (int i=0; i<instructionSteps.size(); i++) {
            instructionStep myInstructionStep = instructionSteps[i];
            for (int j=0; j<myInstructionStep.instructionSentences.size(); j++) {
                instructionSentence myInstructionSent = myInstructionStep.instructionSentences[j];
                string sentence = myInstructionSent.sentence;
                myInstructionSent.isServingSentence = false;
                TokenScanner scanner(sentence);
                scanner.ignoreWhitespace();
                scanner.addWordCharacters("'");
                string previousPreviousToken;
                string previousToken;
                string currentToken;
                while (scanner.hasMoreTokens()) {
                    previousPreviousToken = previousToken;
                    previousToken = currentToken;
                    currentToken = scanner.nextToken();
                    if (previousPreviousToken == "") continue;
                    if (vectorContains(finalIngredientWords,previousToken) &&
                            !(vectorContains(VALID_BEFORE_WORDS, previousPreviousToken) &&
                              vectorContains(VALID_AFTER_WORDS, currentToken))) {
                        myInstructionSent.isGoodSentence = false;
                        break;
                    }
                    else if (vectorContains(finalIngredientWords,previousToken)) {
                        myInstructionSent.order1EndSeedsInside += previousToken;
                        myInstructionSent.isGoodSentence = true;
                    }
                    else {
                        myInstructionSent.isGoodSentence = true;
                    }
                    if (vectorContains(servingWords,previousPreviousToken) || vectorContains(servingWords,previousToken) || vectorContains(servingWords,currentToken)) {
                        myInstructionSent.isServingSentence = true;
                    }
                }
                myInstructionSent.sentence = stringReplace(myInstructionSent.sentence, "\n", "");
                if (myInstructionSent.isGoodSentence) goodInstructionSentences += myInstructionSent;
                if (myInstructionSent.isServingSentence) servingInstructionSentences += myInstructionSent;
                myInstructionStep.instructionSentences[j] = myInstructionSent;
            }
            instructionSteps[i] = myInstructionStep;
        }
    }

    void printGoodSentences() {
        cout << name << endl;
        cout << "-----------------------------------------" << endl;
        for (int i=0; i<goodInstructionSentences.size(); i++) {
            instructionSentence myInstructionSent = goodInstructionSentences[i];
            if (myInstructionSent.order1EndSeedsInside.size()==0) continue;
            string sentence = myInstructionSent.sentence;
            sentence = stringReplace(sentence, "\n", "");
            cout << "   Sentence: " << sentence << endl;
            cout << "      Seeds: " << myInstructionSent.order1EndSeedsInside << endl;
        }
        cout << endl << endl << endl;
    }

    Vector<instructionStep> separateInstructions() {
        Vector<instructionStep> myInstructionSteps;
        //cout << name << endl;
        if (instructionsAreNumbered) {
            int index = 1;
            Vector<Vector<int>> boundsOfSteps;
            while (true) {
                string stepStart1;
                string stepStart2;
                string stepStart3;
                string stepStart4;
                if (index == 1) stepStart1 = string("\n") + integerToString(index) + string(". ");
                else {
                    stepStart1 = string(" \n") + integerToString(index) + string(". ");
                    stepStart2 = string(" \n\n") + integerToString(index) + string(". ");
                    stepStart3 = string(" \n\n\n") + integerToString(index) + string(". ");
                    stepStart4 = string(" \n\n\n\n") + integerToString(index) + string(". ");
                }

                string officialStepStart;
                int indexOfStart = stringIndexOf(allInstructionsText, stepStart1);
                officialStepStart = stepStart1;
                if (indexOfStart==-1) {
                    indexOfStart = stringIndexOf(allInstructionsText, stepStart2);
                    officialStepStart = stepStart2;
                }
                if (indexOfStart==-1) {
                    indexOfStart = stringIndexOf(allInstructionsText, stepStart3);
                    officialStepStart = stepStart3;
                }
                if (indexOfStart==-1) {
                    indexOfStart = stringIndexOf(allInstructionsText, stepStart4);
                    officialStepStart = stepStart4;
                }

                if (!boundsOfSteps.isEmpty()) boundsOfSteps[index-2] += indexOfStart;
                if (indexOfStart != -1) {
                    int indexOfRealStart = indexOfStart + officialStepStart.size();
                    Vector<int> boundOfStep;
                    boundOfStep += indexOfRealStart;
                    boundsOfSteps += boundOfStep;
                }
                else {
                    Vector<int> boundsOfLastStep = boundsOfSteps.get(boundsOfSteps.size()-1);
                    boundsOfLastStep += allInstructionsText.size()-1;
                    break;
                }
                index++;
            }
            for (int i=0; i<boundsOfSteps.size(); i++) {
                Vector<int> boundsOfStep = boundsOfSteps[i];
                instructionStep newInstructionStep;
                newInstructionStep.stepNumber = i+1;
                newInstructionStep.allText = allInstructionsText.substr(boundsOfStep[0],boundsOfStep[1]-boundsOfStep[0]);
                newInstructionStep.allText = trim(newInstructionStep.allText);
                myInstructionSteps += newInstructionStep;
            }
        }
        else {
            instructionStep newInstructionStep;
            newInstructionStep.stepNumber = 0;
            newInstructionStep.allText = trim(allInstructionsText);
            if (startsWith(newInstructionStep.allText,"\n")) newInstructionStep.allText = newInstructionStep.allText.substr(1);
            myInstructionSteps += newInstructionStep;
        }
        //cout << myInstructionSteps[0].allText << endl;
        instructionSteps = myInstructionSteps;
        return myInstructionSteps;
    }

    void printAllInstructionText() {
        cout << name << endl;
        cout << "------------------------------------------" << endl;
        cout << allInstructionsText << endl << endl << endl;
    }

    void printAllInstructionSteps() {
        cout << name << endl;
        cout << "------------------------------------------" << endl;
        int i=1;
        for (instructionStep iStep : instructionSteps) {
            cout << "   Step " << i << ": " << iStep.allText << endl;
            i++;
        }
        cout << endl << endl << endl;
    }

    // MODIFY THIS SO IT CAN HANDLE AN END SEED LENGTH OF 3
    void fillEndSeeds(int endSeedLength) {
        for (int i=0; i<ingredients.size(); i++) {
            ingredient myIngredient = ingredients[i];
            Vector<string> words = myIngredient.wordsInIngredient;
            int numWords = words.size();
            if (numWords == 1) {
                myIngredient.endSeed += words[0];
            }
            else if (numWords == 2) {
                if (isUnit(words[0])) myIngredient.endSeed += words[1];
                else {
                    for (int j=endSeedLength; j>0; j--) {
                        myIngredient.endSeed += words[numWords-j];
                    }
                }
            }
            else {
                for (int j=endSeedLength; j>0; j--) {
                    myIngredient.endSeed += words[numWords-j];
                }
            }
            ingredients[i] = myIngredient;
            endSeeds.add(myIngredient.endSeed);
        }
    }

    void printEndSeeds() {
        cout << name << endl;
        cout << "---------------------------------" << endl;
        for (Vector<string> endSeed : endSeeds) {
            cout << "   " << endSeed << endl;
        }
    }

    void printIngredients() {
        for (int i=0; i<ingredients.size(); i++) {
            cout << "   " << ingredients[i].entireLine << endl;
            cout << "        Amount: " << ingredients[i].amount << endl;
            cout << "        Units: " << ingredients[i].units << endl;
            cout << "        Words: " << ingredients[i].wordsInIngredient << endl;
            cout << "        Non-Unit Words: " << ingredients[i].nonUnitWordsInIngredient << endl;
            cout << "        End Seed: " << ingredients[i].endSeed << endl;
        }
        cout << "   End Seeds:" << endl;
        for (Vector<string> endSeed : endSeeds) {
            cout << "   " << endSeed << endl;
        }
    }

    bool isUnit(string word) {
        for (int j=0; j<NORMAL_UNITS.size(); j++) {
            if (word == NORMAL_UNITS[j] || word == NORMAL_UNITS_PLURAL[j]) {
                return true;
            }
        }
        return false;
    }

    bool vectorContains(Vector<string> vec, string word) {
        for (string member : vec) {
            if (word == member) return true;
        }
        return false;
    }

    bool vectorContains(Vector<Vector<string>> superVec, Vector<string> subVec) {
        for (Vector<string> member : superVec) {
            if (subVec == member) return true;
        }
        return false;
    }

    void findIngredientAmounts() {
        for (int i=0; i<ingredients.size(); i++) {
            ingredient myIngredient = ingredients[i];
            string line = myIngredient.entireLine;
            if (isdigit(line[0])) {
                string numString = "";
                for (int j=1; j<int(line.size())-3; j++) {
                    char previousChar = line[j-1];
                    char currentChar = line[j];
                    char nextChar = line[j+1];
                    char nextNextChar = line[j+2];
                    char nextNextNextChar = line[j+3];
                    if (isdigit(previousChar) && !isdigit(nextChar) &&
                            currentChar==' ' && !(nextChar=='t' && nextNextChar=='o' && nextNextNextChar==' ')) {
                        numString += charToString(previousChar);
                        break;
                    }
                    else if (isdigit(previousChar) && !isdigit(nextChar) && (currentChar=='-' || currentChar=='x')) {
                        for (int k=numString.size()-1; k>=0; k--) {
                            if (numString[k] == ' ') {
                                numString.erase(numString.size()-1);
                                break;
                            }
                            else {
                                numString.erase(numString.size()-1);
                            }
                        }
                        break;
                    }
                    else {
                        numString += charToString(previousChar);
                    }
                }
                myIngredient.amount = numString;
            }
            else {
                myIngredient.amount = "NO_LEADING_NUMBER";
            }
            ingredients[i] = myIngredient;
        }
    }

    void findIngredientUnits() {
        for (int i=0; i<ingredients.size(); i++) {
            ingredient myIngredient = ingredients[i];
            string line = myIngredient.entireLine;
            std::vector<std::string> myVec = stringSplit(line, string(" "));
            string theUnits = "";
            bool unitsFound = false;
            for (int i=0; i<int(myVec.size()); i++) {
                if (isUnit(myVec[i])) {
                    theUnits = myVec[i];
                    unitsFound = true;
                    break;
                }
                if (unitsFound) break;
            }
            myIngredient.units = theUnits;
            ingredients[i] = myIngredient;
        }
    }

    void fillIngredientWords() {
        for (int i=0; i<ingredients.size(); i++) {
            ingredient myIngredient = ingredients[i];
            string line = myIngredient.entireLine;
            std::vector<std::string> wordsInIngredient = stringSplit(line, string(" "));
            for (int i=0; i<int(wordsInIngredient.size()); i++) {
                string word = wordsInIngredient[i];
                string newWord;
                for (char ch : word) {
                    if (!isalpha(ch)) newWord += " ";
                    else newWord += charToString(ch);
                }
                wordsInIngredient[i] = newWord;
            }

            Vector<string> ingredientWords;
            bool validWord = true;
            for (int i=0; i<int(wordsInIngredient.size()); i++) {
                string currentWord = wordsInIngredient[i];
                for (char ch : currentWord) {
                    if (isdigit(ch)) validWord = false;
                }
                if (validWord) {
                    string word = wordsInIngredient[i];
                    string newWord;
                    for (char ch : word) {
                        if (ch==',') newWord += "";
                        else if (ch=='-') newWord += " ";
                        else if (!isalpha(ch)) newWord += " ";
                        else newWord += charToString(ch);
                    }
                    newWord = trim(newWord);
                    std::vector<std::string> wordSplit = stringSplit(newWord, string(" "));
                    for (string newWord2 : wordSplit) {
                        ingredientWords.add(newWord2);
                    }
                }
                validWord = true;
            }

            Vector<string> nonUnitIngredientWords;
            for (string word : ingredientWords) {
                if (!isUnit(word)) nonUnitIngredientWords += word;
            }
            myIngredient.wordsInIngredient = ingredientWords;
            myIngredient.nonUnitWordsInIngredient = nonUnitIngredientWords;
            ingredients[i] = myIngredient;
        }
    }

    void separateIngredients(Lexicon & adjectives) {
        string ingredientsText = allIngredientsText;
        Vector<ingredient> myIngredients;
        bool payAttention = false;
        bool inParentheses = false;
        bool pastComma = false;
        bool ingredientsStarted = false;
        int wordsInIngredient = 0;
        string currentWord = "";

        for (int currentIndex=1; currentIndex<int(ingredientsText.size())-2; currentIndex++) {
            char previousChar = ingredientsText[currentIndex-1];
            char currentChar = ingredientsText[currentIndex];
            char nextChar = ingredientsText[currentIndex+1];

            if (isalpha(previousChar)) currentWord += charToString(previousChar);
            else if (currentWord != "") {
                wordsInIngredient++;
                currentWord = "";
            }

            if (previousChar == '\n' && isdigit(currentChar) && !inParentheses) {
                wordsInIngredient = 0;
                payAttention = true;
                pastComma = false;
                ingredientsStarted = true;
                ingredient newIngredient;
                myIngredients.add(newIngredient);
            }
            else if (currentIndex==1 && isdigit(previousChar)) {
                wordsInIngredient = 0;
                payAttention = true;
                pastComma = false;
                ingredientsStarted = true;
                ingredient newIngredient;
                myIngredients.add(newIngredient);
            }
            else if (previousChar == '\n' && isupper(currentChar) && ingredientsStarted && !inParentheses) {
                wordsInIngredient = 0;
                payAttention = true;
                pastComma = false;
                ingredientsStarted = true;
                ingredient newIngredient;
                myIngredients.add(newIngredient);
            }
            else if (ingredientsStarted) {
                if (currentChar == ',' && !inParentheses && !(adjectives.contains(currentWord) && wordsInIngredient < 2)) {
                    payAttention = false;
                    pastComma = true;
                }

                else if (currentChar == '(') {
                    payAttention = false;
                    inParentheses = true;
                }
                else if (currentChar == ')') {
                    inParentheses = false;
                    if (!pastComma) {
                        payAttention = true;
                    }
                }
            }

            if (payAttention) {
                ingredient currentIngredient = myIngredients.get(myIngredients.size()-1);
                string currentLine = currentIngredient.entireLine;
                if (currentChar == ')' || (currentChar == ' ' && currentLine[currentLine.size()-1] == ' ')) continue;
                if (currentIndex==1 && isdigit(previousChar)) currentLine += charToString(previousChar);
                if (currentChar != '\n') currentLine += charToString(currentChar);
                if (currentIndex==int(ingredientsText.size())-2 && isalpha(nextChar)) currentLine += charToString(nextChar);
                currentIngredient.entireLine = currentLine;
                myIngredients.set(myIngredients.size()-1, currentIngredient);
            }
        }
        ingredients = myIngredients;
    }

    void removeCaps() {
        string recipeText = allRecipeText;
        Vector<int> capsLineIndices;
        bool inMakeServeLine = false;
        bool belowMakeServeLine = false;
        bool inHeaderLine = false;
        for (int currentIndex=1; currentIndex<int(recipeText.size())-2; currentIndex++) {
            char currentChar = recipeText[currentIndex];
            char nextChar = recipeText[currentIndex+1];
            string makesOrServes;
            if (!belowMakeServeLine) {
                makesOrServes = recipeText.substr(currentIndex,6);
                if (makesOrServes == "MAKES " || makesOrServes == "SERVES") {
                    inMakeServeLine = true;
                }
            }
            if (inMakeServeLine && currentChar == '\n') {
                inMakeServeLine = false;
                belowMakeServeLine = true;
            }
            if (inHeaderLine) {
                if (currentChar == '\n') {
                    inHeaderLine = false;
                }
            }
            else if (isalpha(currentChar) && isalpha(nextChar) &&
                     isupper(currentChar) && isupper(nextChar) && !inMakeServeLine) {
                capsLineIndices.add(currentIndex);
                inHeaderLine = true;
            }
        }

        string newRecipeText = removeCapsLinesWithIndices(recipeText, capsLineIndices);
        allRecipeText = newRecipeText;
        recipeCharLength = newRecipeText.length();
    }

    string removeCapsLinesWithIndices(string & recipeText, Vector<int> capsLineIndices) {
        string newRecipeText = recipeText;
        for (int i=capsLineIndices.size()-1; i>=0; i--) {
            int previousSlashNIndex;
            int nextSlashNIndex;
            int ind;
            char previousChar;
            char currentChar;
            char nextChar;

            ind = capsLineIndices[i];
            while (true) {
                if (ind > 0) previousChar = recipeText[ind-1];
                currentChar = recipeText[ind];
                if (ind < (int(recipeText.length())-2)) nextChar = recipeText[ind+1];
                if (previousChar == '\n' || ind == 0) {
                    previousSlashNIndex = ind;
                    break;
                }
                ind--;
            }

            ind = capsLineIndices[i];
            while (true) {
                if (ind > 0) previousChar = recipeText[ind-1];
                currentChar = recipeText[ind];
                if (ind < (int(recipeText.length())-2)) {
                    nextChar = recipeText[ind+1];
                }
                if (nextChar == '\n' || ind == int(recipeText.length())-1) {
                    nextSlashNIndex = ind;
                    break;
                }\
                ind++;
            }

            int lineLength = nextSlashNIndex - previousSlashNIndex + 1;
            string lineString = recipeText.substr(previousSlashNIndex,lineLength);
            //cout << lineString << endl;
            stringReplaceInPlace(newRecipeText, lineString, string(""));
        }
        return newRecipeText;
    }

    int findNumServings() {
        string numServingsString = "";
        string recipeText = allRecipeText;
        bool inMakeServeLine = false;
        bool belowMakeServeLine = false;
        for (int currentIndex=0; currentIndex<int(recipeText.size())-7; currentIndex++) {
            char currentChar = recipeText[currentIndex];
            char nextChar = recipeText[currentIndex+1];
            string makesOrServes;
            if (!belowMakeServeLine) {
                makesOrServes = recipeText.substr(currentIndex,6);
                if (makesOrServes == "MAKES " || makesOrServes == "SERVES") {
                    inMakeServeLine = true;
                }
            }
            if (inMakeServeLine && currentChar == '\n') {
                inMakeServeLine = false;
                belowMakeServeLine = true;
            }
            if (inMakeServeLine) {
                if (isdigit(currentChar)) {
                    numServingsString += charToString(currentChar);
                }
                if (numServingsString != "" && !isdigit(nextChar)) break;
                if (nextChar == '\n') {
                    if (numServingsString.size() == 0) numServingsString = "10";
                    break;
                }
            }
        }
        int returnInt = -1;
        if (numServingsString != "") returnInt = stringToInteger(numServingsString);
        return returnInt;
    }

    string findTitle() {
        string title = "";
        string recipeText = allRecipeText;
        int currentIndex = 0;
        while (true) {
            char currentChar = recipeText[currentIndex];
            char nextChar = recipeText[currentIndex+1];
            char nextNextChar = recipeText[currentIndex+2];
            if (nextChar == '\n' && nextNextChar == '\n') {
                break;
            }
            else if (currentChar == '\n') {}
            else {
                title += charToString(currentChar);
            }
            currentIndex++;
        }
        return title;
    }

    string findAllIngredients() {
        string allIngredients = "\n";
        string recipeText = allRecipeText;
        bool inMakeServeLine = false;
        bool belowMakeServeLine = false;
        bool haveSeenNumbers = false;
        for (int currentIndex=0; currentIndex<int(recipeText.length())-3; currentIndex++) {
            char currentChar = recipeText[currentIndex];
            char nextChar = recipeText[currentIndex+1];
            char nextNextChar = recipeText[currentIndex+2];
            string makesOrServes;
            if (currentIndex < int(recipeText.size())-7) {
                makesOrServes = recipeText.substr(currentIndex,6);
            }
            if (makesOrServes == "MAKES " || makesOrServes == "SERVES") {
                haveSeenNumbers = false;
                inMakeServeLine = true;
            }
            if (inMakeServeLine && currentChar == '\n') {
                inMakeServeLine = false;
                belowMakeServeLine = true;
            }
            else if (belowMakeServeLine) {
                if (isdigit(currentChar)) haveSeenNumbers = true;
                if (allIngredients == "" && currentChar == '\n') {}
                else {
                    if ((currentChar == '\n' && isalpha(nextChar) && haveSeenNumbers &&
                         isIn(getWord(currentIndex+1, recipeText), INSTRUCTION_VERBS)) ||
                            (currentChar == '\n' && isdigit(nextChar) && nextNextChar == '.')) {
                        allInstructionsText = recipeText.substr(currentIndex,recipeText.size()-currentIndex);
                        instructionsAreNumbered = (currentChar == '\n' && isdigit(nextChar) && nextNextChar == '.');
                        break;
                    }
                    else {
                        allIngredients += charToString(currentChar);
                    }
                }
            }
        }
        return allIngredients;
    }

    string getWord(int currentIndex, string & recipeText) {
        string returnWord = "";
        while (true) {
            char currentChar = recipeText[currentIndex];
            if (!isalpha(currentChar)) break;
            else returnWord += charToString(currentChar);
            currentIndex++;
        }
        return returnWord;
    }

    bool isIn(string word, Vector<string> vec) {
        for (string member : vec) {
            if (word == member) return true;
        }
        return false;
    }
};



/* Recipe-Related Function Prototypes */
string getAllText(ifstream & infile);
int findIndEndLastRecipe(int indStartRecipe, string & allText);
int findIndPreviousTitle(int index, string & allText);
Map<string,string> invertMap(Map<string,string> map);
void fillRecipes(Vector<Recipe> & allRecipes, string & allText);
void splitRecipes(Vector<Recipe> & allRecipes, Lexicon & adjectives, int endSeedLength);
void printListOfRecipesIngredients(Vector<Recipe> & allRecipes, int startingIndex, int numToPrint);
void giveRecipesAdjectives(Vector<Recipe> & allRecipes, Lexicon & adjectives);
void makeListAllIngredients(Vector<Recipe> & allRecipes);
void printRecipeEndSeeds(Vector<Recipe> & allRecipes, int startingIndex=-5, int numToPrint=-5);
void makeEndSeedMap(Vector<Recipe> & allRecipes, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap);
void deleteOneIngredientRecipes(Vector<Recipe> & allRecipes);
void makeIngredientMarkov(Vector<ingredient> & allIngredients, string & allIngredientsString, Map<Vector<string>,Vector<string>> & reverseSeedMap,
                          int seedLength, int endSeedLength, int defaultSeedLength=1);
void compileAllIngredients(Vector<Recipe> & allRecipes, Vector<ingredient> & allIngredients, string & allIngredientsString);
Vector<string> makeRandomIngredientsList(Map<Vector<string>,Vector<string>> & reverseSeedMap, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap,
                                         int numIngredients, int seedLength, int endSeedLength, int endSeedSeedLength);
Vector<string> makeRandomInstructions(Vector<instructionSentence> & bigVec, Vector<string> ingredientsList);
bool vectorContains(Vector<string> vec, string word);
bool vectorContains(Vector<Vector<string>> superVec, Vector<string> subVec);
void refineReverseSeedMapKeys(Map<Vector<string>,Vector<string>> & reverseSeedMap);
string refineRandomInstructions(Vector<string> & instructions, Vector<instructionSentence> & servingSentencesWithoutSeeds);


/* Main Program */
int main() {
    ifstream adj_infile;
    string adj_filename = "adjectives.txt";
    if (!openFile(adj_infile, adj_filename)) {
        error("Can't open " + adj_filename);
    }
    Lexicon adjectives(adj_filename);
    adj_infile.close();

    ifstream adj_infile2;
    if (!openFile(adj_infile2, adj_filename)) {
        error("Can't open " + adj_filename);
    }
    Vector<string> properAdjectives;
    for (int i=0; i<int(adjectives.size()/2); i++) {
        string word;
        getLine(adj_infile2,word);
        if (isupper(word[0])) properAdjectives += word;
    }
    adj_infile2.close();

    ifstream infile;

    string fileName = "MarthaStewart-LivingCookbook.txt";
    infile.open(fileName.c_str());
    cout << "            Random Recipe Writer | CS 106B | Winter 2015 | Austin Ray" << endl;
    cout << "   -----------------------------------------------------------------------------" << endl << endl;

    string greet = "";
    greet += "   Hello there! I am a random recipe writer! Thanks for checking me out!\n";
    greet += "   I am able to create random recipes for you based on the recipes found in\n";
    greet += "   The Martha Stewart Living Cookbook\" by using Markov chains. If you want to\n";
    greet += "   know how I do this, enter \"explain\", otherwise enter \"start\" to begin: ";
    string start = getLine(greet);
    if (start=="explain") {
        cout << "\n\n   -----------------------------Program Explanation-----------------------------" << endl << endl;
        cout << "   " << "   The first thing I do is separate all of Martha's recipes into C++ objects." << endl;
        cout << "   " << "Next, I do some refinement on each recipe, separating ingredients from" << endl;
        cout << "   " << "instructions, separating ingredients from each other, etc. After that," <<endl;
        cout << "   " << "I realize that the last two words of each ingredient are the best" << endl;
        cout << "   " << "description of that ingredient. So I make a C++ map to associate" << endl;
        cout << "   " << "each \"end seed\" with other end seeds that they've been seen with in" << endl;
        cout << "   " << "recipes. This is the Markov chain that allows me to add new ingredients" << endl;
        cout << "   " << "to the recipe that go well with previous ingredients. Next, I create another" << endl;
        cout << "   " << "Markov chain to associate words in an ingredient with the words behind" << endl;
        cout << "   " << "(to the left of) them. This allows me to add a new ingredient just by its" << endl;
        cout << "   " << "end seed, then fill in the rest of the line from right to left, forming" << endl;
        cout << "   " << "a complete ingredient. In this way, I create my full ingredients list." << endl;
        cout << "   " << "Since it uses a Markov chain, more ingredients means less cohesiveness" << endl;
        cout << "   " << "between all of the ingredients. You've been Warned!" << endl;
        cout << "   " << "   Next, for the title, I examine the ingredients in my recipe, adding" << endl;
        cout << "   " << "good words for titles and ignoring the bad ones. Oh, and I also add" << endl;
        cout << "   " << "a special adjective at the beginning of the title to give each recipe" << endl;
        cout << "   " << "its own personal flair. Next, for the instructions, I first look at" << endl;
        cout << "   " << "all the instruction sentences I've seen in the cookbook. We can see" << endl;
        cout << "   " << "that certain sentences are too complicated to try to fit my freshly" << endl;
        cout << "   " << "picked ingredients into, while others are simple and allow me to work" << endl;
        cout << "   " << "my ingredients in just fine. Primarily, this includes sentences that" << endl;
        cout << "   " << "use small connector words like with, and, to, the, etc. around their" << endl;
        cout << "   " << "ingredients. This allows me to input my ingredients without creating" << endl;
        cout << "   " << "too crazy of a sentence - pretty cool, huh? Next, I associate each" << endl;
        cout << "   " << "sentence with the ingredients found in it. When I go to write the" << endl;
        cout << "   " << "instructions for my newly generated recipe, I look at my ingredients" << endl;
        cout << "   " << "and try to find simple sentences I've seen them in before. If I find" << endl;
        cout << "   " << "a good sentence with the ingredient in it, I put that sentence down" << endl;
        cout << "   " << "as an instruction step and move on to my other ingredients. If I can't" << endl;
        cout << "   " << "find a good sentence with an ingredient, I just take any old simple" << endl;
        cout << "   " << "sentence and insert my ingredient into it, replacing the one that was" << endl;
        cout << "   " << "there before. After I've written instructions that include all of my" << endl;
        cout << "   " << "ingredients, I then add a good ending sentence, if one isn't there" << endl;
        cout << "   " << "already. And voila! You have your scrumptious new randomly generated" << endl;
        cout << "   " << "recipe. Happy cooking!" << endl;
    }
    cout << "\n\n   -------------------------------Main Program----------------------------------" << endl << endl;
    int seedLength = 2;
    int endSeedLength = 2;
    int numIngredients;
    int endSeedSeedLength;
    int numRecipesToPrint;
    string allAtOnce;
    while (true) {
        numIngredients = getInteger("   Enter the desired number of ingredients per recipe (5-15 allowed): ");
        if (numIngredients<5 || numIngredients>15) {
            cout << "\n   Invalid number of ingredients. Try again." << endl << endl;
            continue;
        }
        break;
    }
    while (true) {
        endSeedSeedLength = getInteger("   Enter ingredient similarity within recipes (1-5 allowed, 5 = very similar): ");
        if (endSeedSeedLength<1 || endSeedSeedLength>5) {
            cout << "\n   Invalid ingredient similarity. Try again." << endl << endl;
            continue;
        }
        break;
    }
    while (true) {
        numRecipesToPrint = getInteger("   Enter the number of recipes you want (1-100 allowed): ");
        if (numRecipesToPrint<1 || numRecipesToPrint>100) {
            cout << "\n   Invalid number of recipes. Try again." << endl << endl;
            continue;
        }
        break;
    }
    while (true) {
        allAtOnce = getLine("   Do you want to print recipes one by one, or all at once?\n   (Enter either \"one\" or \"all\"): ");
        if (!(allAtOnce=="one") && !(allAtOnce=="all")) {
            cout << "\n   Invalid input. Try again." << endl << endl;
            continue;
        }
        else if (allAtOnce=="one") {
            cout << "\n   Got it. Press Enter after each recipe prints to get the next one." << endl;
        }
        break;
    }

    cout << "\n   " << "I'm going to generate your recipes now. This might take a minute..." << endl << endl << endl;

    Vector<Recipe> allRecipes;
    string allText = getAllText(infile);
    fillRecipes(allRecipes, allText);
    splitRecipes(allRecipes, adjectives, endSeedLength);
    deleteOneIngredientRecipes(allRecipes);

    cout << "   " << "...Making progress..." << endl;
    Vector<ingredient> allIngredients;
    string allIngredientsString;
    compileAllIngredients(allRecipes, allIngredients, allIngredientsString);

    Map<Vector<string>,Vector<string>> reverseSeedMap;
    makeIngredientMarkov(allIngredients, allIngredientsString, reverseSeedMap, seedLength, endSeedLength);

    cout << "   " << "...Still working..." << endl;
    refineReverseSeedMapKeys(reverseSeedMap);


    Map<Vector<string>,Vector<Vector<string>>> endSeedMap;
    makeEndSeedMap(allRecipes, endSeedMap);

    cout << "   " << "...Can't be much longer now..." << endl;

    Lexicon singleEndSeeds;
    for (int i=0; i<endSeedMap.keys().size(); i++) {
        Vector<string> key = endSeedMap.keys().get(i);
        string endWord = key[key.size()-1];
        if (singleEndSeeds.contains(endWord)) continue;
        singleEndSeeds.add(endWord);
    }

    Vector<instructionSentence> allGoodSentences;
    Vector<instructionSentence> goodSentencesWithSeeds;
    Vector<instructionSentence> servingSentences;
    Vector<instructionSentence> servingSentencesWithoutSeeds;
    for (int i=0; i<allRecipes.size(); i++) {
        Recipe myRecipe = allRecipes[i];
        myRecipe.fillInstructionSentenceTokens();
        Vector<instructionSentence> goodInstructionSentences = myRecipe.getGoodInstructionSentences();
        Vector<instructionSentence> servingInstructionSentences = myRecipe.getServingInstructionSentences();
        allGoodSentences += goodInstructionSentences;
        servingSentences += servingInstructionSentences;
        for (instructionSentence instSent : goodInstructionSentences) {
            if (instSent.order1EndSeedsInside.size() != 0) {
                bool containsBadSeed = false;
                for (string token : instSent.tokensInSentence) {
                    if (!vectorContains(instSent.order1EndSeedsInside,token) && singleEndSeeds.contains(token)) containsBadSeed = true;
                }
                if (!containsBadSeed) goodSentencesWithSeeds += instSent;
            }
        }
        for (instructionSentence instSent : servingInstructionSentences) {
            if (instSent.order1EndSeedsInside.size() == 0) {
                Vector<string> tokens = instSent.tokensInSentence;
                bool hasSeed = false;
                for (string token : tokens) {
                    if (singleEndSeeds.contains(token)) {
                        hasSeed = true;
                        break;
                    }
                }
                if (!hasSeed) servingSentencesWithoutSeeds += instSent;
            }
        }
    }

    Vector<string> validEndsOfTitles;
    validEndsOfTitles += "bread", "oil", "sausage", "cheese", "corn", "salad", "dressing",
            "stock", "pepper", "bacon", "meat", "mustard", "butter", "water", "melon",
            "kiwi", "lettuce", "yogurt", "sauce", "rice", "salt", "port", "vinegar";

    Vector<string> badTitleWords;
    badTitleWords += "halves", "thighs", "leaves", "stalks", "cloves", "half", "thigh", "leaf", "stalk", "clove", "extract";

    cout << endl << endl << endl << endl << endl << endl << endl << endl << endl;


    string metaTextToPrint;

    metaTextToPrint += string("               Randomly Generated Recipe Booklet\n");
    metaTextToPrint += string("            ----------------------------------------- \n\n");
    cout << metaTextToPrint << endl;
    Vector<string> markovIngredientsList;
    bool shouldStop = false;
    if (allAtOnce == "one") shouldStop = true;
    for (int i=0; i<numRecipesToPrint; i++) {
        if (i>=1 && allAtOnce=="one" && shouldStop) {
            string continueString = getLine();
        }
        markovIngredientsList = makeRandomIngredientsList(reverseSeedMap, endSeedMap, numIngredients, seedLength, endSeedLength, endSeedSeedLength);
        if (markovIngredientsList[0] == "ERROR") {
            i--;
            shouldStop = false;
            continue;
        }
        Vector<string> lastTokens;
        for (int j=0; j<markovIngredientsList.size(); j++) {
            string line = markovIngredientsList[j];
            TokenScanner scanner(line);
            string lastToken;
            while (scanner.hasMoreTokens()) {
                string currentToken = scanner.nextToken();
                lastToken = currentToken;
            }
            lastTokens += lastToken;
        }

        int r = randomInteger(0,properAdjectives.size()-1);
        string startingWord = properAdjectives.get(r);
        string recipeTitle;
        recipeTitle += startingWord + " ";
        string lastWordInTitle = "";
        string lastWordInTitle2 = "";
        for (string token : lastTokens) {
            if (vectorContains(validEndsOfTitles,token) && !vectorContains(badTitleWords,token)) {
                lastWordInTitle = token;
                break;
            }
        }
        for (string token : lastTokens) {
            if (token[token.size()-1] == 's' && !vectorContains(badTitleWords,token)) {
                lastWordInTitle = token;
                break;
            }
        }


        for (string token : lastTokens) {
            if (vectorContains(validEndsOfTitles,token) && token != lastWordInTitle && !vectorContains(badTitleWords,token)) {
                lastWordInTitle2 = token;
                break;
            }
        }
        for (string token : lastTokens) {
            if (token[token.size()-1] == 's' && token != lastWordInTitle && !vectorContains(badTitleWords,token)) {
                lastWordInTitle2 = token;
                break;
            }
        }
        string descriptorWord;
        for (string token : lastTokens) {
            if (token[token.size()-1] != 's' && token != lastWordInTitle && token != lastWordInTitle2 && !vectorContains(badTitleWords,token)) {
                descriptorWord = token;
                break;
            }
        }

        if (descriptorWord != "") recipeTitle += charToString(toupper(descriptorWord[0])) + descriptorWord.substr(1) + " ";
        if (lastWordInTitle != "") recipeTitle += charToString(toupper(lastWordInTitle[0])) + lastWordInTitle.substr(1);
        if (lastWordInTitle != "" && lastWordInTitle2 != "") recipeTitle += string(" with ");
        if (lastWordInTitle2 != "") recipeTitle += charToString(toupper(lastWordInTitle2[0])) + lastWordInTitle2.substr(1);

        if (descriptorWord == "" && lastWordInTitle == "" && lastWordInTitle2 == "") recipeTitle += "Food";

        string textToPrint;
        textToPrint += string(" ") + recipeTitle;

        //        cout << "Checkpoint 3" << endl;
        int rand = randomInteger(0,allRecipes.size()-1);
        Recipe myRecipe = allRecipes.get(rand);
        int numServings = myRecipe.getNumServings();
        if (numServings<=0) numServings = randomInteger(1,9);
        textToPrint += " (SERVES " + integerToString(numServings) + ")\n";
        //        cout << "Checkpoint 4" << endl;

        textToPrint += "   Ingredients:\n";
        for (string ingredient : markovIngredientsList) {
            if (ingredient[2]=='/') ingredient = charToString(ingredient[0]) + ingredient.substr(4);
            textToPrint += "      " + ingredient + "\n";
        }
        textToPrint += string("\n");

        //        cout << "Checkpoint 5" << endl;
        Vector<string> randomInstructions = makeRandomInstructions(goodSentencesWithSeeds, markovIngredientsList);
        if (randomInstructions[0] == "ERROR") {
            i--;
            shouldStop = false;
            continue;
        }
        //        cout << "Checkpoint 6" << endl;
        string instructionsToPrint = refineRandomInstructions(randomInstructions, servingSentencesWithoutSeeds);
        textToPrint += "   Instructions:\n";
        textToPrint += instructionsToPrint + "\n\n\n";
        //        cout << "Checkpoint 7" << endl;

        cout << textToPrint;
        metaTextToPrint += textToPrint;
        textToPrint.clear();
        markovIngredientsList.clear();
        if (allAtOnce == "one") shouldStop = true;
    }

    cout << "\n\n\n   I have saved your recipes in \"Random_Recipe_Book.txt\" in this application's folder.\n\n\n" << endl;

    ofstream outfile;
    outfile.open("Random_Recipe_Book.txt");
    outfile << metaTextToPrint;
    outfile.close();
    infile.close();        //Close the stream
    return 0;
}


/* Function Implementations */

string refineRandomInstructions(Vector<string> & instructions, Vector<instructionSentence> & servingSentencesWithoutSeeds) {
    string serveSentence;
    string startSentence;
    Vector<string> servingWords;
    servingWords += "Serve", "serve", "Served", "served";
    Vector<string> startWords;
    startWords += "Add", "Mix", "Combine", "In", "Prepare", "Preheat", "Blend", "Using", "Place", "Melt", "Slice", "Halve", "Heat";
    bool servingSentenceExists = false;
    for (int i=0; i<instructions.size(); i++) {
        string sentence = instructions[i];

        for (string word : servingWords) {
            if (stringContains(sentence,word)) {
                instructions[i] = instructions[instructions.size()-1];
                instructions[instructions.size()-1] = sentence;
                servingSentenceExists = true;
            }
        }

        for (string word : startWords) {
            if (startsWith(sentence, word)) {
                instructions[i] = instructions[0];
                instructions[0] = sentence;
            }
        }
    }
    if (!servingSentenceExists) {
        int r = randomInteger(0,servingSentencesWithoutSeeds.size()-1);
        string servingSentence = servingSentencesWithoutSeeds.get(r).sentence;
        instructions += servingSentence;
    }
    string returnString;
    int counter = 1;
    for (string sentence : instructions) {
        string newSentence;
        int charCounter = 0;
        for (char ch : sentence) {
            if (charCounter>60 && ch==' ') {
                charCounter = 0;
                newSentence += string(" ") + "\n" + "         ";
                if (counter/10==1) newSentence += " ";
            }
            else newSentence += charToString(ch);
            charCounter++;
        }
        sentence = newSentence;
        returnString += string("      ") + integerToString(counter) + ". " + sentence + "\n";
        counter++;
    }
    return returnString;
}

Vector<string> makeRandomInstructions(Vector<instructionSentence> & bigVec, Vector<string> ingredientsList) {
    Vector<string> returnVec;
    Vector<string> endSeeds;
    for (int i=0; i<ingredientsList.size(); i++) {
        string ingredient = ingredientsList[i];
        std::vector<std::string> ingredientSplit = stringSplit(ingredient," ");
        string endSeed = ingredientSplit[ingredientSplit.size()-1];
        endSeeds += endSeed;
    }
    Vector<Vector<string>> endSeedsUsed;
    for (int j=0; j<endSeeds.size(); j++) {
        Vector<string> endSeedUsed;
        endSeedUsed += endSeeds[j];
        endSeedUsed += string("false");
        endSeedsUsed += endSeedUsed;
    }

    bool existUnusedSeeds = true;
    int emptiesUsed = 0;
    int iterationCounter1 = 0;
    while (existUnusedSeeds) {
        if (iterationCounter1>300) {
            Vector<string> errorVec;
            errorVec += "ERROR";
            return errorVec;
        }
        Vector<instructionSentence> refinedBigVec;
        Vector<string> unusedEndSeeds;
        for (int j=0; j<endSeedsUsed.size(); j++) {
            Vector<string> endSeedUsed = endSeedsUsed.get(j);
            if (endSeedUsed.get(1)=="false") unusedEndSeeds += endSeedUsed.get(0);
        }
        if (unusedEndSeeds.size()==0) break;
        for (int i=0; i<bigVec.size(); i++) {
            bool shouldAdd = true;
            bool hasUnusedSeed = false;
            for (string word : bigVec.get(i).order1EndSeedsInside) {
                if (!vectorContains(endSeeds, word)) shouldAdd = false;
                if (vectorContains(unusedEndSeeds, word)) hasUnusedSeed = true;
            }
            if (shouldAdd && hasUnusedSeed) {
                refinedBigVec += bigVec.get(i);
            }
        }
        int r;
        string sentence;
        instructionSentence randomInstructSent;
        if (refinedBigVec.isEmpty()) {
            r = randomInteger(0,bigVec.size()-1);
            randomInstructSent = bigVec.get(r);
            sentence += randomInstructSent.sentence;
            Vector<string> endSeedsInvolved = randomInstructSent.order1EndSeedsInside;
            TokenScanner scanner(sentence);
            string newSentence;
            while (scanner.hasMoreTokens()) {
                string currentToken = scanner.nextToken();
                int r = randomInteger(0,unusedEndSeeds.size()-1);
                if (vectorContains(endSeedsInvolved,currentToken)) {
                    if (unusedEndSeeds.size()==0) {
                        Vector<string> errorVec;
                        errorVec += "ERROR";
                        return errorVec;
                    }
                    newSentence += unusedEndSeeds[r];
                    for (int i=0; i<endSeedsUsed.size(); i++) {
                        Vector<string> endSeedUsed = endSeedsUsed.get(i);
                        if (unusedEndSeeds[r]!=endSeedUsed[0]) continue;
                        endSeedUsed[1] = "true";
                        endSeedsUsed[i] = endSeedUsed;
                    }
                    unusedEndSeeds.remove(r);
                }
                else newSentence += currentToken;
            }
            sentence = newSentence;
        }
        else {
            r = randomInteger(0,refinedBigVec.size()-1);
            randomInstructSent = refinedBigVec.get(r);
            sentence += randomInstructSent.sentence;
        }
        int trueCounter = 0;
        for (int i=0; i<endSeeds.size(); i++) {
            if (vectorContains(randomInstructSent.order1EndSeedsInside, endSeeds[i])) {

                Vector<string> endSeedUsed = endSeedsUsed.get(i);
                endSeedUsed[1] = "true";
                endSeedsUsed[i] = endSeedUsed;
            }
            if (endSeedsUsed.get(i).get(1)=="true") trueCounter++;
        }
        if ((trueCounter+emptiesUsed)==endSeeds.size()) existUnusedSeeds = false;
        returnVec += sentence;
        iterationCounter1++;
    }
    return returnVec;
}

void refineReverseSeedMapKeys(Map<Vector<string>,Vector<string>> & reverseSeedMap) {
    for (Vector<string> key : reverseSeedMap.keys()) {
        if ((vectorContains(key,string("$")) || vectorContains(key,string("%")))) reverseSeedMap.remove(key);
    }
}

Vector<string> makeRandomIngredientsList(Map<Vector<string>,Vector<string>> & reverseSeedMap, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap, int numIngredients, int seedLength, int endSeedLength, int endSeedSeedLength) {
    Vector<string> outputTokens;
    Vector<string> ingredientList;

    const Vector<Vector<string>> &allEndSeedKeys = endSeedMap.keys();
    //    const Vector<Vector<string>> &allRevSeedKeys = reverseSeedMap.keys();

    Vector<Vector<string>> usedEndSeedKeys;
    //    cout << "ck1" << endl << endl;
    int r = randomInteger(0,allEndSeedKeys.size()-1);
    Vector<string> firstEndSeedKey = allEndSeedKeys.get(r);
    usedEndSeedKeys += firstEndSeedKey;
    string firstIngredient = "";
    for (string member : firstEndSeedKey) {
        firstIngredient += member + " ";
    }
    firstIngredient = trimEnd(firstIngredient);
    //    cout << "ck2" << endl << endl;
    Vector<string> newKey;
    Vector<string> oldKey;
    if (firstEndSeedKey.size()<seedLength) oldKey = firstEndSeedKey;
    else oldKey += firstEndSeedKey.subList(0,seedLength);
    int iterationCounter = 0;
    while (true) {
        if (iterationCounter>200) {
            Vector<string> errorVec;
            errorVec += "ERROR";
            return errorVec;
        }
        Vector<string> possiblePreviousTokens = reverseSeedMap.get(oldKey);
        int numTokens = possiblePreviousTokens.size();
        int r = randomInteger(0,numTokens-1);
        string previousTokenToBeAdded = possiblePreviousTokens[r];
        if (previousTokenToBeAdded == "%") break;
        string newFirstIngredient;
        if (previousTokenToBeAdded=="/") newFirstIngredient = previousTokenToBeAdded + firstIngredient;
        else if (firstIngredient[0]=='/') newFirstIngredient = previousTokenToBeAdded + firstIngredient;
        else newFirstIngredient = previousTokenToBeAdded + " " + firstIngredient;
        firstIngredient = newFirstIngredient;
        newKey += previousTokenToBeAdded;
        if (oldKey.size()<seedLength-1) newKey += oldKey;
        else newKey += oldKey.subList(0,seedLength-1);
        oldKey = newKey;
        newKey.clear();
        iterationCounter++;
    }
    //    cout << "ck3" << endl << endl;
    ingredientList += firstIngredient;

    Vector<string> newEndSeedKey;
    Vector<string> lastEndSeedKey;
    lastEndSeedKey += firstEndSeedKey;
    int iterationCounter2 = 0;
    for (int i=0; i<numIngredients; i++) {
        if (iterationCounter2>200) {
            Vector<string> errorVec;
            errorVec += "ERROR";
            return errorVec;
        }
        //        cout << "ck4" << endl << endl;
        Vector<Vector<string>> possibleNextEndSeedKeys;
        if (usedEndSeedKeys.size() >= endSeedSeedLength) {
            for (int j=endSeedSeedLength; j>0; j--) {
                Vector<string> seedKey = usedEndSeedKeys[usedEndSeedKeys.size()-j];
                possibleNextEndSeedKeys += endSeedMap.get(seedKey);
            }
        }
        else {
            for (int j=0; j<usedEndSeedKeys.size(); j++) {
                Vector<string> seedKey = usedEndSeedKeys[j];
                possibleNextEndSeedKeys += endSeedMap.get(seedKey);
            }
        }
        //        cout << "ck5" << endl << endl;
        if (possibleNextEndSeedKeys.size()==0) {
            Vector<string> errorVec;
            errorVec += "ERROR";
            return errorVec;
        }
        int r = randomInteger(0,possibleNextEndSeedKeys.size()-1);
        if (vectorContains(usedEndSeedKeys,possibleNextEndSeedKeys[r])) {
            i--;
            iterationCounter2++;
            continue;
        }
        //        cout << "ck6" << endl << endl;
        if (vectorContains(possibleNextEndSeedKeys[r],string("plus")) || vectorContains(possibleNextEndSeedKeys[r],string("lengths")) || vectorContains(possibleNextEndSeedKeys[r],string("inch"))) {
            i--;
            iterationCounter2++;
            continue;
        }
        newEndSeedKey = possibleNextEndSeedKeys[r];
        usedEndSeedKeys += newEndSeedKey;
        string newIngredient = "";
        for (string member : newEndSeedKey) {
            newIngredient += member + " ";
        }
        newIngredient = trimEnd(newIngredient);
        Vector<string> newKey;
        Vector<string> oldKey;
        //        cout << "ck7" << endl << endl;
        if (newEndSeedKey.size()<seedLength) oldKey = newEndSeedKey;
        else oldKey += newEndSeedKey.subList(0,seedLength);
        iterationCounter = 0;
        while (true) {
            if (iterationCounter>200) {
                Vector<string> errorVec;
                errorVec += "ERROR";
                return errorVec;
            }
            //            cout << "ck8" << endl << endl;
            Vector<string> possiblePreviousTokens = reverseSeedMap.get(oldKey);
            int r = randomInteger(0,possiblePreviousTokens.size()-1);
            if (possiblePreviousTokens.size()==0) {
                Vector<string> errorVec;
                errorVec += "ERROR";
                return errorVec;
            }
            string previousTokenToBeAdded = possiblePreviousTokens[r];
            //            cout << "ck9" << endl << endl;
            if (previousTokenToBeAdded == "%") break;
            string tempNewIngredient;
            if (previousTokenToBeAdded=="/") tempNewIngredient = previousTokenToBeAdded + newIngredient;
            else if (newIngredient[0]=='/') tempNewIngredient = previousTokenToBeAdded + newIngredient;
            else tempNewIngredient = previousTokenToBeAdded + " " + newIngredient;
            newIngredient = tempNewIngredient;
            newKey += previousTokenToBeAdded;
            if (oldKey.size()<seedLength-1) newKey += oldKey;
            else newKey += oldKey.subList(0,seedLength-1);
            oldKey = newKey;
            newKey.clear();
            iterationCounter++;
            //            cout << "ck10" << endl << endl;
        }
        lastEndSeedKey = newEndSeedKey;
        ingredientList += newIngredient;
        iterationCounter2++;
        //        cout << "ck11" << endl << endl;
    }
    return ingredientList;
}

bool vectorContains(Vector<string> vec, string word) {
    for (string member : vec) {
        if (word == member) return true;
    }
    return false;
}

bool vectorContains(Vector<Vector<string>> superVec, Vector<string> subVec) {
    for (Vector<string> member : superVec) {
        if (subVec == member) return true;
    }
    return false;
}

void compileAllIngredients(Vector<Recipe> & allRecipes, Vector<ingredient> & allIngredients, string & allIngredientsString) {
    for (int i=0; i<allRecipes.size(); i++) {
        Recipe currentRecipe = allRecipes[i];
        Vector<ingredient> recipeIngredients = currentRecipe.getIngredients();
        for (ingredient myIngredient : recipeIngredients) {
            allIngredients += myIngredient;
            string line;
            if (myIngredient.amount=="NO_LEADING_NUMBER") line = "% ";
            else line = "% " + myIngredient.amount + " ";
            string lastWord = "";
            for (string word : myIngredient.wordsInIngredient) {
                if (lastWord=="plus" && allRecipes[0].isUnit(word)) line += integerToString(randomInteger(1,10)) + " " + word + " ";
                else line += word + " ";
                lastWord = word;
            }
            line += "\n";
            allIngredientsString += line;
        }
    }
}

void makeIngredientMarkov(Vector<ingredient> & allIngredients, string & allIngredientsString, Map<Vector<string>,Vector<string>> & reverseSeedMap, int seedLength, int endSeedLength, int defaultSeedLength) {
    TokenScanner scanner(allIngredientsString);
    scanner.ignoreWhitespace();
    scanner.addWordCharacters("'");
    Vector<string> tokens;
    for (int i=0; i<seedLength+1; i++) {
        string myToken;
        tokens += myToken;
    }
    Vector<string> tokensEnd;
    for (int i=0; i<endSeedLength+1; i++) {
        string myToken;
        tokensEnd += myToken;
    }
    Vector<string> tokensDefault;
    for (int i=0; i<defaultSeedLength+1; i++) {
        string myToken;
        tokensDefault += myToken;
    }
    Vector<string> currentSeed;
    Vector<string> currentSeedEnd;
    Vector<string> currentSeedDefault;
    while (scanner.hasMoreTokens()) {
        for (int i=0; i<seedLength; i++) {
            tokens[i] = tokens[i+1];
        }
        for (int i=0; i<endSeedLength; i++) {
            tokensEnd[i] = tokensEnd[i+1];
        }
        for (int i=0; i<defaultSeedLength; i++) {
            tokensDefault[i] = tokensDefault[i+1];
        }
        tokens[seedLength] = scanner.nextToken();
        tokensEnd[endSeedLength] = tokens[seedLength];
        tokensDefault[defaultSeedLength] = tokens[seedLength];
        currentSeed += tokens[seedLength];
        currentSeedEnd += tokensEnd[endSeedLength];
        currentSeedDefault += tokensDefault[defaultSeedLength];

        if (currentSeed.size() > seedLength) {
            currentSeed = currentSeed.subList(1,seedLength);
            if (reverseSeedMap.containsKey(currentSeed)) {
                Vector<string> currentVals = reverseSeedMap.get(currentSeed);
                currentVals += tokens[0];
                reverseSeedMap.put(currentSeed,currentVals);
            }
            else {
                Vector<string> vals;
                vals.add(tokens[0]);
                reverseSeedMap.add(currentSeed,vals);
            }
        }
        if (currentSeedEnd.size() > endSeedLength) {
            currentSeedEnd = currentSeedEnd.subList(1,endSeedLength);

            if (reverseSeedMap.containsKey(currentSeedEnd)) {
                Vector<string> currentVals = reverseSeedMap.get(currentSeedEnd);
                currentVals += tokensEnd[0];
                reverseSeedMap.put(currentSeedEnd,currentVals);
            }
            else {
                Vector<string> vals;
                vals.add(tokensEnd[0]);
                reverseSeedMap.add(currentSeedEnd,vals);
            }
        }
        if (currentSeedDefault.size() > defaultSeedLength) {
            currentSeedDefault = currentSeedDefault.subList(1,defaultSeedLength);

            if (reverseSeedMap.containsKey(currentSeedDefault)) {
                Vector<string> currentVals = reverseSeedMap.get(currentSeedDefault);
                currentVals += tokensDefault[0];
                reverseSeedMap.put(currentSeedDefault,currentVals);
            }
            else {
                Vector<string> vals;
                vals.add(tokensDefault[0]);
                reverseSeedMap.add(currentSeedDefault,vals);
            }
        }
    }
}

void makeEndSeedMap(Vector<Recipe> & allRecipes, Map<Vector<string>,Vector<Vector<string>>> & endSeedMap) {
    for (int i=0; i<allRecipes.size(); i++) {
        Recipe currentRecipe = allRecipes[i];
        Vector<Vector<string>> endSeeds = currentRecipe.getEndSeeds();
        for (int j=0; j<endSeeds.size(); j++) {
            Vector<string> key;
            key += endSeeds[j];
            Vector<Vector<string>> vals;
            for (int k=0; k<endSeeds.size(); k++) {
                if (j==k) break;
                else vals += endSeeds[k];
            }
            if (!endSeedMap.containsKey(key)){
                endSeedMap.add(key,vals);
            }
            else {
                Vector<Vector<string>> currentVals;
                currentVals = endSeedMap.get(key);
                vals += currentVals;
                endSeedMap.put(key,vals);
            }
        }
    }
}

void deleteOneIngredientRecipes(Vector<Recipe> & allRecipes) {
    Vector<Recipe> newAllRecipes;
    for (int i=0; i<allRecipes.size(); i++) {
        Recipe currentRecipe = allRecipes[i];
        if (!(currentRecipe.getEndSeeds().size() == 1 || currentRecipe.getEndSeeds().size() == 0)) {
            newAllRecipes += currentRecipe;
        }
    }
    allRecipes.clear();
    allRecipes = newAllRecipes;
}

void splitRecipes(Vector<Recipe> & allRecipes, Lexicon & adjectives, int endSeedLength) {
    for (int i=0; i<allRecipes.size(); i++) {
        //cout << i << endl;
        Recipe myRecipe = allRecipes[i];
        myRecipe.removeCaps();
        myRecipe.setName(myRecipe.findTitle());
        myRecipe.setNumServings(myRecipe.findNumServings());
        myRecipe.setAllIngredientsText(myRecipe.findAllIngredients());
        myRecipe.separateIngredients(adjectives);
        myRecipe.separateInstructions();
        myRecipe.findIngredientAmounts();
        myRecipe.findIngredientUnits();
        myRecipe.fillIngredientWords();
        myRecipe.fillEndSeeds(endSeedLength);
        myRecipe.divideInstructionSentences();
        myRecipe.findFinalIngredientWords();
        myRecipe.findSeedsInInstructionSentences();

        allRecipes[i] = myRecipe;
    }
}

void printListOfRecipesIngredients(Vector<Recipe> & allRecipes, int startingIndex, int numToPrint) {
    for (int i=startingIndex; i<startingIndex+numToPrint; i++) {
        Recipe myRecipe = allRecipes[i];
        cout << myRecipe.getName() << endl;
        cout << "-------------------------------" << endl;
        myRecipe.printIngredients();
        cout << endl << endl << endl;

    }
}

void printRecipeEndSeeds(Vector<Recipe> & allRecipes, int startingIndex, int numToPrint) {
    if (startingIndex==-5) startingIndex = 0;
    if (numToPrint==-5) numToPrint = allRecipes.size();
    for (int i=startingIndex; i<startingIndex+numToPrint; i++) {
        Recipe myRecipe = allRecipes[i];
        myRecipe.printEndSeeds();
        cout << endl << endl << endl;

    }
}

string getAllText(ifstream & infile) {
    string returnText = "";
    int chInt;
    while ((chInt = infile.get()) != EOF) {
        char ch = char(chInt);
        returnText += charToString(ch);
    }
    return returnText;
}

void fillRecipes(Vector<Recipe> & allRecipes, string & allText) {
    int index = 0;
    int recipeInd = 0;
    int newLinesSinceLastMakesServes = 100;
    while (true) {
        if (index == int(allText.length())) {
            int indEndLastRecipe = allText.length() - 1;
            Recipe previousRecipe = allRecipes[recipeInd-1];
            int lengthOfLastRecipe = indEndLastRecipe - previousRecipe.getIndStartRecipe();
            previousRecipe.setAllRecipeText(allText.substr(previousRecipe.getIndStartRecipe(), lengthOfLastRecipe));
            allRecipes[recipeInd-1] = previousRecipe;
            break;
        }
        string makesOrServes;
        if (index < int(allText.size())-7) {
            makesOrServes = allText.substr(index,6);
        }
        if (newLinesSinceLastMakesServes > 5 && (makesOrServes == "MAKES " || makesOrServes == "SERVES")) {
            Recipe newRecipe;
            newLinesSinceLastMakesServes = 0;
            int indStartRecipe = findIndPreviousTitle(index, allText);
            newRecipe.setIndStartRecipe(indStartRecipe);
            allRecipes += newRecipe;

            if (recipeInd != 0) {
                int indEndLastRecipe = findIndEndLastRecipe(indStartRecipe, allText);
                Recipe previousRecipe = allRecipes[recipeInd-1];
                int lengthOfLastRecipe = indEndLastRecipe - previousRecipe.getIndStartRecipe();
                previousRecipe.setAllRecipeText(allText.substr(previousRecipe.getIndStartRecipe(), lengthOfLastRecipe));
                previousRecipe.setRecipeCharLength(lengthOfLastRecipe);
                allRecipes[recipeInd-1] = previousRecipe;
            }
            recipeInd++;
        }
        if (allText[index] == '\n') newLinesSinceLastMakesServes++;
        index++;
    }
}

int findIndEndLastRecipe(int indStartRecipe, string & allText) {
    int indEndLastRecipe;
    int currentIndex = indStartRecipe-1;
    while (true) {
        if (currentIndex == 0) {
            indEndLastRecipe = -1;
            break;
        }
        char currentChar = allText[currentIndex];
        if (currentChar == '.') {
            indEndLastRecipe = currentIndex+1;
            break;
        }
        currentIndex--;
    }
    return indEndLastRecipe;
}

int findIndPreviousTitle(int index, string & allText) {
    int indTitle;
    int currentIndex = index-1;
    int possibleIndTitle = -1;
    while (true) {
        if (currentIndex == 0) {
            indTitle = 0;
            break;
        }
        char currentChar = allText[currentIndex];
        char previousChar = allText[currentIndex-1];
        if (currentChar == '.' && possibleIndTitle != -1) {
            indTitle = possibleIndTitle;
            break;
        }
        else if (isalpha(currentChar) && islower(currentChar) && previousChar == '\n') {
            possibleIndTitle = currentIndex;
        }
        currentIndex--;
    }
    return indTitle;
}

Map<string,string> invertMap(Map<string,string> map) {
    Map<string,string> returnMap;
    for (string key : map.keys()) {
        string val = map[key];
        returnMap.put(val,key);
    }
    return returnMap;
}


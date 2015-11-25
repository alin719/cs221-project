'''
Random Recipe CS 221 Final Project
Austin Ray, Bruno De Martino, Alex Lin
'''

import math, random, collections, database

database.createDatabases('allRecipes.json', 'allNutritional.json', 110)
database.printMissedIngredients()
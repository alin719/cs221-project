'''
Random Recipe CS 221 Final Project
Austin Ray, Bruno De Martino, Alex Lin
'''

import math, random, collections, requests, json

def createRecipeDatabase(filename, maxResults):
	apiString = "http://api.yummly.com/v1/api/recipes?_app_id=4d1d7424&_app_key=419a5ef2649eb3b6e359b7a9de93e905&q=&maxResult=%d" % maxResults
	request = requests.get(apiString)
	print request.headers
	assert request.status_code == 200
	allRecipesFile = open(filename, 'w+')
	allRecipesFile.write(request.content)
	allRecipesFile.close()

def testDatabase():
	filename = 'allRecipes.json'
	createRecipeDatabase(filename, 100)
	readFile = open(filename)
	allRecipes = json.loads(readFile.read())

	matches = allRecipes["matches"]
	count = 0
	for recipe in matches:
		print "********** %d *********" % count
		ingredients = recipe["ingredients"]
		for ingredient in ingredients:
			print ingredient
		print "********** %d *********" % count
		count += 1

testDatabase()
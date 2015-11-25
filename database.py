'''
Random Recipe CS 221 Final Project
Austin Ray, Bruno De Martino, Alex Lin
Database file

This file is responsible for constructing the Recipe and the Nutritional Databases
'''

# -------------------- NOTES --------------------
# 1) More printing messages.
# 2) Add cuisine shit now

import collections, requests, json, time

# Yummly API constants
YUM_APP_ID = "4d1d7424"
YUM_APP_KEY = "419a5ef2649eb3b6e359b7a9de93e905"
YUM_STEP = 100
YUM_ALLOWED_COURSE = "course^course-Main Dishes"

# Goverment Nutritional Database API constants
GOV_NUT_API_KEY = "5YbfzajkZSaGWi7hibcD4Nq1EXSGHRtZP5Pvlkvv"
SLEEP_THRESHOLD = 1
PRINT_REMAINING_CALLS = True
PRINT_MISSED_INGREDIENTS = True

# Global variables
allIngredientIds = {}
missedIngredients = []
foundItems = 0
missedItems = 0

# Function: printMissedIngredients
# ---------------------
# Prints each ingredient in the @missedIngredients global list
def printMissedIngredients():
	print "These are the ingredients that do not exist in the government Nutritional Database:"
	for ingredient in missedIngredients:
		print ingredient

# Function: nutritionalSearch
# ---------------------
# Makes search request on Nutritional API. Then, if the status is not 200
# (i.e. the request did not go through), it gets the remaining requests
# we have left for the hour (@remaining) and, checks whether remaining is
# larger than SLEEP_THRESHOLD.
#
# If it is, then the reason why the request did not go through
# was because the ingredient was not found in the ingredient database, so we
# return False and the @searchRequest.
#
# Otherwise, it means that we have exceeded the gov 1K API requests/hour, and
# thus we sleep for 10 min and keep trying until we can make API requests again.
def nutritionalSearch(ingredient):
	apiSearchString = "http://api.nal.usda.gov/ndb/search/?format=json&q=%s&max=1&api_key=%s" % (ingredient, GOV_NUT_API_KEY)
	searchRequest = requests.get(apiSearchString)

	if PRINT_REMAINING_CALLS: print "Gov Nutrional Database Requests remaining: %d" % int(searchRequest.headers['X-RateLimit-Remaining'])

	if searchRequest.status_code != 200:
		remaining = int(searchRequest.headers['X-RateLimit-Remaining'])
		if remaining > SLEEP_THRESHOLD:
			if PRINT_MISSED_INGREDIENTS: print "Could not find ingredient %s" % ingredient
			return False, searchRequest

		while remaining < SLEEP_THRESHOLD:
			print "Request failed because exceeded Gov 1K API requests/hour"
			print "... Sleeping for 10 min ..."
			time.sleep(60*10)
			searchRequest = requests.get(apiSearchString)
			remaining = int(searchRequest.headers['X-RateLimit-Remaining'])
			print "Gov Nutrional Database Requests remaining: %d" % remaining
	return True, searchRequest


# Function: addIngredientToNutritionalList
# ---------------------
# Takes in a list of ingredients (@ingredients). For each ingredient, we search
# for it in the Nutritional Database. If we find it, we add it to our dictionary
# of ingredient -> ingredientIds (@allIngredientIds). Otherwise, we add it to
# out missedIngredients list
def addIngredientToNutritionalList(ingredients):
	global foundItems
	global missedItems

	for ingredient in ingredients:
		foundIngredient, searchRequest = nutritionalSearch(ingredient)

		if foundIngredient:
			# Adding ingredient to allIngredientIds dict
			nutritionalResults = json.loads(searchRequest.content)
			ingredientId = nutritionalResults["list"]["item"][0]["ndbno"]
			if ingredient not in allIngredientIds:
				allIngredientIds[ingredient] = ingredientId
				foundItems += 1

		else:
			# Adding ingredient to missedIngredients list
			if ingredient not in missedIngredients:
				missedIngredients.append(ingredient)
				missedItems += 1

# Function: getNutritionalRequest
# ---------------------
# Makes get request on Nutritional API. Then, if the status is not 200
# (i.e. the request did not go through), it gets the remaining requests
# we have left for the hour (@remaining) and, checks whether remaining is
# larger than SLEEP_THRESHOLD.
#
# If it is, then the reason why the request did not go through
# for a unknown reason, and we return
#
# Otherwise, it means that we have exceeded the gov 1K API requests/hour, and
# thus we sleep for 10 min and keep trying until we can make API requests again.
def getNutritionalRequest(apiGetString):
	getRequest = requests.get(apiGetString)
	if PRINT_REMAINING_CALLS: print "Gov Nutrional Database Requests remaining: %d" % int(searchRequest.headers['X-RateLimit-Remaining'])
	while getRequest.status_code != 200:
		print
		print "[BROKE REQUEST] Status code != 200"

		remaining = int(getRequest.headers['X-RateLimit-Remaining'])
		print "Gov Nutrional Database Requests remaining: %d" % remaining

		if remaining > SLEEP_THRESHOLD:
			return

		while remaining < SLEEP_THRESHOLD:
			print "Request failed because exceeded Gov 1K API requests/hour"
			print "... Sleeping for 10 min ..."
			time.sleep(60*10)
			getRequest = requests.get(apiGetString)
			remaining = int(getRequest.headers['X-RateLimit-Remaining'])
			print "Gov Nutrional Database Requests remaining: %d" % remaining
	return getRequest

# Function: buildNutritionalDatabase
# ---------------------
# Goes through all ingredients in the @ingredientNameIdMap, makes a get request
# for their ingredientId on the Nutritional Database, and creates a ingredientObj
# for it, which is then mapped to the ingredient in the @nutritionalDatabase.
#
# A ingredientObj has: ingredientName, ingredientId, and foodCalories.
# A foodCalories object has: the default value and units in 100g, and the measures,
# which consists of translated values for other common units of the ingredient.
#
# Once we have looped through all ingredients, we store the nutritionalDatabase in
# json format on the file with the filename.
def buildNutritionalDatabase(ingredientNameIdMap, filename):
	numIngredients = len(ingredientNameIdMap)
	print "... Creating Nutritional Database with %d items ..." % numIngredients

	nutritionalDatabase = {}

	for ingredientName, ingredientId in ingredientNameIdMap.iteritems():
		apiGetString = "http://api.nal.usda.gov/ndb/reports/?ndbno={0}&type=b&format=json&api_key={1}".format(ingredientId, GOV_NUT_API_KEY)

		getRequest = getNutritionalRequest(apiGetString)

		getFood = json.loads(getRequest.content)
		foodCalories = getFood['report']['food']['nutrients'][1]

		ingredientObj = {'ingredientName': ingredientName,
						 'ingredientId': ingredientId,
						 'foodCalories': (foodCalories['value'], foodCalories['unit'], foodCalories['measures'])}

		nutritionalDatabase[ingredientName] = ingredientObj

	jsonNutritionalDatabase = json.dumps(nutritionalDatabase, sort_keys=True, indent=4)
	allNutritionalFile = open(filename, 'w+')
	allNutritionalFile.write(jsonNutritionalDatabase)
	allNutritionalFile.close()
	print "... Done creating Nutritional Database with %d items ..." % numIngredients

	print "... Out of all %d ingredient in our recipe, we found %d of them, and missed %d of them ..." % (foundItems + missedItems, foundItems, missedItems)

# Function: buildRecipeEntry
# ---------------------
# For a given Yummly recipe, we extract the field we want in our version
# of a recipe object. Then, we make a Yummly API get request to get more
# information on the recipe, so we can have access to the ingredientList of
# the recipe, which tells us the quantities per ingredient.
#
# Then, we create a recipeObj that has: recipeName, recipeId, ingredients,
# ingredientLines, attributes (which has: cuisine and/or course),
# totalTimesInSeconds, flavors, and return it.
def buildRecipeEntry(recipe):
	recipeName = recipe['recipeName']
	recipeId= recipe['id']
	ingredients = recipe['ingredients']
	addIngredientToNutritionalList(ingredients)
	brokeRequest = True

	while brokeRequest:
		apiGetString = "http://api.yummly.com/v1/api/recipe/%s?_app_id=4d1d7424&_app_key=419a5ef2649eb3b6e359b7a9de93e905" % recipeId
		getRequest = requests.get(apiGetString)
		brokeRequest = not (getRequest.status_code == 200)

	getRecipe = json.loads(getRequest.content)
	ingredientLines = getRecipe["ingredientLines"]

	recipeObj = {'recipeName': recipeName,
				 'recipeId': recipeId,
				 'ingredients': ingredients,
				 'ingredientLines': ingredientLines,
				 'attributes': recipe['attributes'],
				 'totalTimeInSeconds': recipe['totalTimeInSeconds'],
				 'flavors': recipe['flavors']}

	return recipeName, recipeObj

# Function: getNumSteps
# ---------------------
# Quick calculations to return the number of steps given totalResults
# and YUM_STEP.
def getNumSteps(totalResults):
	numSteps = totalResults/YUM_STEP
	if totalResults % YUM_STEP != 0:
		numSteps += 1
	return numSteps

# Function: getStartAndMaxResults
# ---------------------
# Quick calculations to return the start number and the
# maxResults number given the iteration we are in and the
# totalResults.
def getStartAndMaxResults(i, numSteps, totalResults):
	start = YUM_STEP * i
	maxResults = YUM_STEP
	if i == numSteps - 1:
		maxResults = totalResults - start
	if totalResults < YUM_STEP:
		maxResults = totalResults
	return start, maxResults

# Function: buildRecipeDatabase
# ---------------------
# Since the Yummly Search API only returns ~150 items at a time successfuly, we
# break down our totalResults number into smaller chunks of YUM_STEP, and loop
# through the necessary number of chunks, where at each iteration we make a API
# search request and add the recipe to the @recipeDatabase. Finally, once we get all
# totalResults recipe, we store the recipeDatabase in json format in the file with
# filename.
def buildRecipeDatabase(recipeFilename, totalResults):
	print "... Creating Recipe Database with %d recipes ..." % totalResults

	numSteps = getNumSteps(totalResults)
	recipeDatabase = {}
	brokeRequest = True

	for i in range(numSteps):
		start, maxResults = getStartAndMaxResults(i, numSteps, totalResults)
		print "... Processing recipes: %d to %d ..." % (start + 1, start + maxResults)

		while brokeRequest:
			apiSearchString = "http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=&allowedCourse[]=%s&maxResult=%d&start=%d" % (YUM_APP_ID, YUM_APP_KEY, YUM_ALLOWED_COURSE, maxResults, start)
			searchRequest = requests.get(apiSearchString)
			brokeRequest = not (searchRequest.status_code == 200)

		allRecipes = json.loads(searchRequest.content)
		matches = allRecipes["matches"]
		for recipe in matches:
			recipeName, recipeObj = buildRecipeEntry(recipe)
			recipeDatabase[recipeName] = recipeObj

	jsonRecipeDatabase = json.dumps(recipeDatabase, sort_keys=True, indent=4)
	allRecipesFile = open(recipeFilename, 'w+')
	allRecipesFile.write(jsonRecipeDatabase)
	allRecipesFile.close()

	print "... Done creating Recipe Database with %d recipes ..." % totalResults

# Function: createDatabases
# ---------------------
# Creates the Recipe and the Nutritional Databases and store them in the
# respective files in json format.
def createDatabases(recipeFilename, nutritionalFileName, numRecipes):
	buildRecipeDatabase(recipeFilename, numRecipes)
	print
	buildNutritionalDatabase(allIngredientIds, nutritionalFileName)
	print
	print "The recipe and nutritional databases are ready to go! Access them at %s and %s, respectively" % (recipeFilename, nutritionalFileName)
	print

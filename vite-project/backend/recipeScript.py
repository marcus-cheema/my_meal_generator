import pandas as pd 
from keybert import KeyBERT 
import numpy as np 
import time
import csv
import os
from fuzzywuzzy import fuzz

userBMR = 2000 # Global Default

# === Return Top Matching Recipes Based on User Input === #
def getTopRecipeMatches(mergedDF: pd.DataFrame, tasteProfile: str, caloriesPerMeal: int, nRecipes: int) -> list:
    
    acceptedError = .3 # alter value... (should be < 1)
    caloricDeviation = caloriesPerMeal * acceptedError
    minCaloriesPerMeal, maxCaloriesPerMeal = caloriesPerMeal - caloricDeviation, caloriesPerMeal + caloricDeviation

    # Only include recipes within a Valid Caloric Range (based on User BMR)
    validCaloricRecipes = mergedDF[(mergedDF['calories'] >= minCaloriesPerMeal) & (mergedDF['calories'] <= maxCaloriesPerMeal)]
    
    if len(validCaloricRecipes) < nRecipes:
        raise ValueError(f'There are not nRecipes in selected_recipes_df. Choose value lower than {len(selected_recipes_df)}')

    print(f'# of Selected Recipes: {len(validCaloricRecipes)}')
    similarityScores = []
    tasteKeyWords = KeyBERT().extract_keywords(tasteProfile) # use keyBert to get the keywords? 
    tasteKeyWords = [word for word, _ in tasteKeyWords]
    denom = len(tasteKeyWords)
    if denom == 0:
        raise ValueError("No KeyWords extracted from the User's Taste Profile!")
    
    start = time.time()
    keyWordColumns = [str(i) for i in range(5)]
    for i, row in validCaloricRecipes.iterrows():
        
        currKeyWords = row[keyWordColumns].tolist()
        try: currKeyWords = [word.split(',')[0].strip('("\'') for word in currKeyWords]
        except AttributeError as e: continue
            
        score = 0
        for word in tasteKeyWords: # Go through user preferences
            score += fuzz.partial_ratio(word, currKeyWords) / denom
            similarityScores.append([i, score])
    
    print(f'Fuzzy Algorithm Time: {round(time.time() - start, 3)} seconds')
    
    similarityScores.sort(key=lambda x: x[1], reverse=True) # sort by highest mean
    topIndices = [i for i, _ in similarityScores] # return indices
    topNIndices = topIndices[:nRecipes]
    topRecipes = [mergedDF.iloc[index] for index in topNIndices]
    topRecipesName = [mergedDF['name'][index] for index in topNIndices]
    # print(topRecipesName)
    
    return topRecipes

# === Use Harris-Benedict equation for BMR calculation, w/ Activity Level Multipliers === #
def calculateBMR(sex: int, age: int, weight: int, height: int, activityLevel):
    print(sex, age, weight, height, activityLevel)
    activityMultipliers = {
        0: 1.2,
        1: 1.375,
        2: 1.55,
        3: 1.725,
        4: 1.9
    }

    weightKG = weight * 0.453592
    heightCM = height * 2.54
    bmr = 0
    
    if sex == 0: # Male
        bmr = 88.362 + (13.397 * weightKG) + (4.799 * heightCM) - (5.677 * age)
    else: # Female
        bmr = 447.593 + (9.247 * weightKG) + (3.098 * heightCM) - (4.330 * age)

    bmr = bmr * activityMultipliers.get(activityLevel, 1.2) # default 1.2
    print(round(bmr))
    setUserBMR(round(bmr)) # Whenever this function is called, update the user's BMR
    return round(bmr)

def setUserBMR(bmr):
    global userBMR
    userBMR = bmr

def main():
    caloriesPerDay = round(userBMR * 0.34)
    print(caloriesPerDay)
    tasteProfile = "I want to know how to make a chicken fettucini alfredo with broccoli"
    nRecipes = 5
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def loadData(): # cache data loads
        embeddedPath = os.path.join(BASE_DIR, '.venv', 'dat', 'embedded_recipes.csv') 
        recipePath =  os.path.join(BASE_DIR, '.venv', 'dat', 'all_recipes_scraped.csv')
        return pd.read_csv(recipePath), pd.read_csv(embeddedPath)
    
    def preprocessData(recipes, recipeKeyWords): # Merge once at startup
        mergedDF = pd.merge(recipes, recipeKeyWords, left_index=True, right_index=True)
        mergedDF['calories'] = pd.to_numeric(mergedDF['calories'], errors='coerce')
        return mergedDF
    
    recipes, recipeKeyWords = loadData()
    mergedDF = preprocessData(recipes, recipeKeyWords)
    topNRecipes = getTopRecipeMatches(mergedDF, tasteProfile, caloriesPerMeal, nRecipes)
    # print(topNRecipes)

# This block checks if the script is being run directly, not imported as a module
if __name__ == "__main__":
    main()
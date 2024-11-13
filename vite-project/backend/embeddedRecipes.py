import os
from keybert import KeyBERT 
import pandas as pd 
import time
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def selectRecipes(recipes: pd.DataFrame, n: int) -> pd.DataFrame: # For Processing Efficiency in Testing
    if n > len(recipes): raise ValueError("Choose smaller n")
    selectedRecipes = recipes.head(n)
    return selectedRecipes

def makeRecipeKeyWords(sampleRecipes: pd.DataFrame) -> pd.DataFrame:
    start = time.time()
    keybertModel = KeyBERT() # dont repeat instances
    recipeKeyWords = [] 
    for _, recipe in sampleRecipes.iterrows():
        summary           = recipe['summary']
        title             = recipe['name']
        titleAndSummary = title + " " + summary
        currKeyWords = keybertModel.extract_keywords(titleAndSummary)
        recipeKeyWords.append(currKeyWords)

    end = time.time()
    print(f'Time to Embed {len(recipeKeyWords)} Recipes: {(end - start) / 60} minutes')  

    recipeKeyWords = pd.DataFrame(recipeKeyWords)
    return recipeKeyWords

filePath = os.path.join(BASE_DIR, '.venv', 'dat', 'all_recipes_scraped.csv')

recipeCount = 2000
allRecipes = pd.read_csv(filePath)
sampleRecipes = selectRecipes(allRecipes, recipeCount)

embeddedRecipes = makeRecipeKeyWords(sampleRecipes)
embeddedPath = os.path.join(BASE_DIR, '.venv', 'dat', 'embedded_recipes.csv')
embeddedRecipes.to_csv(embeddedPath, index=False)
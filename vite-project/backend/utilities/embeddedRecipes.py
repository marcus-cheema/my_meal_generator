import os
from keybert import KeyBERT 
import pandas as pd 
import time
import csv

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


def main():
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dat") # Escape, go to Dat
    BASE_DIR = os.path.abspath(BASE_DIR) # Make path Absolute
    
    recipePath   = os.path.join(BASE_DIR, 'dat', 'all_recipes_scraped.csv')
    embeddedPath = os.path.join(BASE_DIR, 'dat', 'embedded_recipes.csv')

    n = 2000
    allRecipes = pd.read_csv(recipePath)
    sampleRecipes = selectRecipes(allRecipes, n) # Select n Recipes

    embeddedRecipes = makeRecipeKeyWords(sampleRecipes)
    embeddedRecipes.to_csv(embeddedPath, index=False)

if __name__ == "__main__":
    main()
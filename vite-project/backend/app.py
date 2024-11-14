import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from dotenv import load_dotenv
from utilities.allRecipeMethods import getTopRecipeMatches, calculateBMR, isRecipeRequest
from utilities.allRecipeMethods import userBMR

app = Flask(__name__)
cors = CORS(app, origins='*') # cross origin resource sharing

load_dotenv() # Fetch API Key
API_KEY=os.getenv("API_KEY")
openai.api_key = API_KEY

def setUserBMR(bmr): # To update Global myBMR
    global userBMR
    userBMR = bmr

# === Verifies if Prompt is On Topic, then Corrects Spelling === #
def correctUserPrompt(prompt: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": ("You are a spell-checking assistant for recipe and food-related prompts ONLY. "
                          "First, verify if the input is related to recipes, cooking, food, ingredient substitutes, "
                          "or general health/nutrition. If the input is OFF-TOPIC, respond EXACTLY with: "
                          "'I can only assist with recipe, cooking, and nutrition-related questions.' "
                          "If the input IS relevant, your ONLY task is to correct misspelled words. Do not make "
                          "any other changes. Do not add punctuation, do not rephrase, do not add or remove words, "
                          "do not change grammar, and do not provide any additional commentary.")
            },
            {
                "role": "user",
                "content": "Example off-topic: 'How do I tie my shoes'"
            },
            {
                "role": "assistant",
                "content": "I can only assist with recipe, cooking, and nutrition-related questions."
            },
            {
                "role": "user",
                "content": "Example on-topic: 'How to make choclate chip cookeis'"
            },
            {
                "role": "assistant",
                "content": "How to make chocolate chip cookies"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

# Handle General Prompts
def handlePrompt(prompt: str) -> str:
    try:
        correctedPrompt = correctUserPrompt(prompt)
        print("CORRECTED PROMPT:", correctedPrompt)
        if isRecipeRequest(correctedPrompt):
            print(userBMR)
            recipes = getTopRecipeMatches(prompt, userBMR, 3) # tasteProfile, BMR, and recipes to return (1 default)
            print(recipes)
            return recipes
        else:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": ("You are an assistant that should only respond to questions regarding recipes, "
                        "ingredient subsitutes, and general health.")
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        return str(e)

user_messages, bot_responses = {}, {} # global

@app.route("/api/bot_response", methods=['GET']) # GET data from the backend server -> Frontend
def bot_response():
    latest_message_id = max(bot_responses.keys(), default=None)
    bot_response = bot_responses.get(latest_message_id, "")
    return jsonify({"response": bot_response})

@app.route("/api/send_message", methods=['POST']) # POST data from the frontend -> backend
def send_message():
    data = request.json
    user_message = data.get("message")
    
    user_message_ID = len(user_messages) + 1
    user_messages[user_message_ID] = user_message
    print(user_messages)

    bot_response_ID = len(bot_responses) + 1

    bot_responses[bot_response_ID] = handlePrompt(user_message)
    print(bot_responses)
    return jsonify({"response": user_message})

@app.route("/api/calculate_bmr", methods=['POST'])
def calculate_bmr():
    data = request.json
    sex, age, weight, height, activityLevel = data['sex'], data['age'], data['weight'], data['height'], data['activityLevel']
    
    # Transform parameters
    intSex    = 0 if sex == "male" else 1
    intAge    = int(age)
    intWeight = int(weight)
    intHeight = int(height)
    intActivityLevel = 0 # Assume 0 if not given.
    if   activityLevel == "sedentary": intActivityLevel = 0
    elif activityLevel == "light":     intActivityLevel = 1
    elif activityLevel == "moderate":  intActivityLevel = 2
    elif activityLevel == "very":      intActivityLevel = 3
    elif activityLevel == "extra":     intActivityLevel = 4

    currBMR = calculateBMR(intSex, intAge, intWeight, intHeight, intActivityLevel) # don't change types of given vars
    setUserBMR(currBMR) # update BMR globally
    print(userBMR)
    return jsonify({"response": currBMR})

if __name__ == "__main__":
    app.run(debug=True, port=8080) # arbitrary port

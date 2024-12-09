import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from dotenv import load_dotenv

from utilities.allRecipeMethods import getTopRecipeMatches, calculateBMR, isRecipeRequest, userBMR

app = Flask(__name__)
cors = CORS(app, origins='*') # cross origin resource sharing

load_dotenv() # Fetch API Key
API_KEY=os.getenv("API_KEY")
openai.api_key = API_KEY

def setUserBMR(bmr): # To update Global myBMR
    global userBMR
    userBMR = bmr

# === Embed User Prompt and Extract <= 5 KeyWords === #
def embedUserPrompt(prompt: str) -> list:
    corrected_prompt = correctUserPrompt(prompt)
    
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts the five most important or relevant words from a given text."
            },
            {
                "role": "user",
                "content": f"Extract the 5 most important words from the following text: {corrected_prompt}"
            }
        ]
    )
    
    response = completion.choices[0].message.content.strip()
    # print(len(completion.choices))
    importantWords = response.split(',')  # Assuming OpenAI will return comma-separated words
    # print(importantWords)
    return [word.strip() for word in importantWords[:5]]

# === Verifies if Prompt is On Topic, then Corrects Spelling === #
def isRecipeRequest(prompt: str) -> str:
    print("HEREEE")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": ("You are responsible for determining whether an input is related to recipe and correcting the prompt if needed. "
                            "First, verify if the input is related to recipes, cooking, food, ingredient subsitutes"
                            "If the input is OFF-TOPIC, respond with a 0 for classification and an empty string for the correction."
                            "If the input is ON-TOPIC, but NOT requesting a recipe, respond with 0 for classification and an empty string for the correction"
                            "If the input is ON-TOPIC and requesting a recipe, respond with a 1 for classification and their corrected prompt for the recipe."
                            "Format your response as a JSON object with keys 'classification' and 'correction'.")
            },
            {
                "role": "user",
                "content": "Example off-topic: 'I want a recipe that has a car tire, and can tie my shoe'"
            },
            {
                "role": "assistant",
                "content": '{"classification": 0, "correction": ""}'
            },
            {
                "role": "user",
                "content": "Example on-topic: 'How to mayke chocltee chp cookies?'"
            },
            {
                "role": "assistant",
                "content": '{"classification": 1, "correction": "How to make chocolate chip cookies?"}'
            },
            {
                "role": "user",
                "content": "Example on-topic, but not requesting: 'I want to know if I should use olive oil instead of mustard oil?'"
            },
            {
                "role": "assistant",
                "content": '{"classification": 0, "correction": ""}'
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    response = completion.choices[0].message.content
    try:
        result = eval(response)
        return result
    except (SyntaxError, ValueError):
        return {"classification": 0, "correction": ""}

# === Handle General Prompts === #
def handlePrompt(prompt: str) -> str:
    try:
        response = isRecipeRequest(prompt)
        classification = response["classification"]
        correctedPrompt = response["correction"]
        
        # User is requesting a recipe
        if classification == 1: 
            embeddedProfile = embedUserPrompt(correctedPrompt)
            recipes = getTopRecipeMatches(embeddedProfile, userBMR, 3) # tasteprofile, bmr, and recipes to return (1 default)
            return recipes
        
        # Not requesting a recipe or off-topic. 
        else: 
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": ("You are an assistant that should only respond to questions regarding recipes, "
                                    "ingredient subsitutes, and general health. If a user greets you or says something " 
                                    "casual like 'hi' or 'hello,' respond warmly and do not apologize. Let them know they "
                                    "can ask questions about recipes or health topics.")
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

userMessages, botResponses = {}, {} # global

@app.route("/api/bot_response", methods=['GET']) # GET data from the backend server -> Frontend
def bot_response():
    latestMessageId = max(botResponses.keys(), default=None)
    botResponse = botResponses.get(latestMessageId, "")
    return jsonify({"response": botResponse})

@app.route("/api/send_message", methods=['POST']) # POST data from the frontend -> backend
def send_message():
    data = request.json
    userMessage = data.get("message")
    
    userMessageId = len(userMessages) + 1
    userMessages[userMessageId] = userMessage

    botResponseId = len(botResponses) + 1

    botResponses[botResponseId] = handlePrompt(userMessage)
    # botResponses[botResponseId] = isRecipeRequest(userMessage)
    print(botResponses[botResponseId])

    return jsonify({"response": botResponses[botResponseId]})

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
    return jsonify({"response": currBMR})

def main():
    print(embedUserPrompt("I want a recipe with bananas, coconuts, beans, and rice"))
if __name__ == "__main__":
    app.run(debug=True, port=8080) # arbitrary port

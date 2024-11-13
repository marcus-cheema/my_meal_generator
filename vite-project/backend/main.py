import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from openai import OpenAI
from dotenv import load_dotenv
from recipeScript import getTopRecipeMatches

app = Flask(__name__)
cors = CORS(app, origins='*') # cross origin resource sharing

load_dotenv() # Fetch API Key
API_KEY=os.getenv("API_KEY")
openai.api_key = API_KEY

def handlePrompt(prompt: str) -> str:
    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that should only respond to questions regarding recipes, ingredient subsitutes, and general health."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return str(e)

# Use Harris-Benedict equation for BMR calculation, w/ Activity Level Multipliers.
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
    userBMR = round(bmr)
    return round(bmr)
     
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
    # bot_responses[bot_response_ID] = "I am the diet bot, DESTROYER of macros"

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
    
    bmr = calculateBMR(intSex, intAge, intWeight, intHeight, intActivityLevel) # don't change types of given vars
    print(bmr)
    return jsonify({"response": bmr})

if __name__ == "__main__":
    app.run(debug=True, port=8080) # arbitrary port

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from dotenv import load_dotenv
from utilities.allRecipeMethods import calculateBMR, getTopRecipeMatches

app = Flask(__name__)
cors = CORS(app, origins='*') # cross origin resource sharing

load_dotenv() # Fetch API Key
API_KEY=os.getenv("API_KEY")
openai.api_key = API_KEY

def correctUserPrompt(prompt: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4"
        messages=[
            {
                "role":"system",
                "content": ("You are a helpful assistant. Your task is to correct and clarify user input, "
                        "focusing on making it clear, with recipe creation in mind. Do not change the meaning"
                        "of the text")
            },
            {
                "role":"user"
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content # return corrected prompt
# Handle General Prompts
def handlePrompt(prompt: str) -> str:
    try:
        if isRecipeRequest(prompt):
            recipes = getTopRecipeMatches(prompt, bmr) # MODIFY LATER
            return recipes # WILL NEED TO FORMAT
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
    
    bmr = calculateBMR(intSex, intAge, intWeight, intHeight, intActivityLevel) # don't change types of given vars
    print(bmr)
    return jsonify({"response": bmr})

if __name__ == "__main__":
    app.run(debug=True, port=8080) # arbitrary port

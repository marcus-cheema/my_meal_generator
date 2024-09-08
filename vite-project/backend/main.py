import os
from flask import Flask, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
from dotenv import load_dotenv


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

@app.route("/api/users", methods=['GET'])
def users():
    prompt = "I was wondering what ingredients I would need for a tomato soup?"
    agentResponse = handlePrompt(prompt)
    print(agentResponse)
    return jsonify({"response": agentResponse})

if __name__ == "__main__":
    app.run(debug=True, port=8080) # arbitrary port

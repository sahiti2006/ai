from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("Api_key")
)

from mongo import (
    candidates_collection,
    questions_collection,
    evaluations_collection
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return jsonify({
        "message": "AI Interview Assistant Running"
    })

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    result = candidates_collection.insert_one({
        "name": data.get("name"),
        "email": data.get("email"),
        "role": data.get("role")
    })

    return jsonify({
        "message": "Registration Successful",
        "id": str(result.inserted_id)
    })
@app.route("/questions", methods=["GET"])
def questions():

    role = request.args.get("role", "Frontend Developer"),
    role = request.args.get("role", "Backend Developer")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Generate ONE technical interview question for a {role}.

        Return only the question.
        """
    )

    question_text = response.text

    questions_collection.insert_one({
        "role": role,
        "question": question_text
    })

    return jsonify({
        "role": role,
        "question": question_text
    })


@app.route("/evaluation", methods=["POST"])
def evaluation():

    data = request.get_json()

    question = data.get("question", "")
    answer = data.get("answer", "")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are an expert technical interviewer.

        Question:
        {question}

        Candidate Answer:
        {answer}

        Evaluate the answer and provide:

        1. Technical Score (0-10)
        2. Communication Score (0-10)
        3. Overall Score (0-10)
        4. Strengths
        5. Areas for Improvement

        Return the evaluation in a clear format.
        """
    )

    evaluation_text = response.text

    evaluations_collection.insert_one({
        "question": question,
        "answer": answer,
        "evaluation": evaluation_text
    })

    return jsonify({
        "question": question,
        "answer": answer,
        "evaluation": evaluation_text
    })


if __name__ == "__main__":
    app.run(debug=True)
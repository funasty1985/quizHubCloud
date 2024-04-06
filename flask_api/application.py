from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
import dill as pickle
app = Flask(__name__)

def generate_quiz_prompt(quiz_id):
    prompts = ["What is 2+2?", "What is the capital of France?", "What color is the sky on a clear day?"]
    options = [
        ["1", "2", "3", "4"],
        ["Paris", "London", "Berlin", "Madrid"],
        ["Blue", "Green", "Red", "Yellow"]
    ]
    answers = [3, 0, 0] 

    index = random.randint(0, len(prompts)-1)
    return {
        "quizId": ObjectId(quiz_id),
        "prompt": prompts[index],
        "options": options[index],
        "answer": answers[index],
    }


client = MongoClient('mongodb+srv://portfolioApp:Fu2017fu@cluster0.ykgbhqe.mongodb.net/project1?retryWrites=true&w=majority')
db = client.project1
quizzes = db.Quiz
questions = db.Question


# POST to http://127.0.0.1:5000/generate_quiz
# SAMPLE BODY REQUEST
# {
#     "title": "Admin Second Quiz",
#     "description": "admin test2",
#     "author": "admin"
# }
@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():


    quiz_metadata = request.json
    quiz_result = quizzes.insert_one(quiz_metadata)
    quiz_id = quiz_result.inserted_id


    quiz_data = generate_quiz_prompt(quiz_id)
    quiz_data["quizId"] = ObjectId(quiz_id)

    question_result = questions.insert_one(quiz_data)
    
    return jsonify({"success": True, "quiz_id": str(quiz_id), "question_id": str(question_result.inserted_id)})


@app.route('/')
def hello():
    return 'Hello!'

if __name__ == '__main__':
    app.run(debug=True)

from pymongo import MongoClient
import random
from bson.objectid import ObjectId
from pprint import pprint

class DbService:

    def __init__(self, connection_str):
        self.client = MongoClient(connection_str)
        self.db = self.client.project1
        self.quizzes = self.db.Quiz
        self.questions = self.db.Question
        self.user = "admin"

    def generate_quiz_prompt(self, quiz_id):
        prompts = ["What is 2+2?", "What is the capital of France?", "What color is the sky on a clear day?"]
        options = [
            ["1", "2", "3", "4"],
            ["Paris", "London", "Berlin", "Madrid"],
            ["Blue", "Green", "Red", "Yellow"]
        ]
        answers = [3, 0, 0]

        index = random.randint(0, len(prompts) - 1)
        return {
            "quizId": ObjectId(quiz_id),
            "prompt": prompts[index],
            "options": options[index],
            "answer": answers[index],
        }

    def create_quiz(self, title, description, user):
        quiz_data = dict(
            title=title,
            description=description,
            author=user
        )

        quiz_result = self.quizzes.insert_one(quiz_data)
        return quiz_result.inserted_id

    def upload_questions_by_quiz_id(self, questions, quiz_id):
        questions = [{**q, "quizId": quiz_id} for q in questions]
        result = self.questions.insert_many(questions)
        return result

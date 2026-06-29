from flask import Flask
from pymongo import MongoClient
app = Flask(__name__)

client_db = MongoClient("mongodb://localhost:27017/")


db = client_db["ai_interview"]

candidates_collection = db["candidates"]
questions_collection = db["questions"]
evaluations_collection = db["evaluations"]
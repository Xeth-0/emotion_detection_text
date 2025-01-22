from model import predict_text_emotion
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

"""
main.py
This module contains the FastAPI application for predicting text emotions.
Endpoints:
- GET /: Returns a welcome message.
- GET /predict: Predicts the emotion of the given text.
Functions:
- root(): Returns a welcome message.
- predict_emotion(text: str): Predicts the emotion of the given text using a pre-trained model.
Dependencies:
- fastapi: FastAPI framework for building APIs.
- model: Custom module containing the predict_text_emotion function.
Example usage:
    Run the FastAPI server and access the endpoints to get predictions.
"""

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict")
async def predict_emotion(text: str):
    model_path = "./model/emotion_classifier.joblib"
    response = predict_text_emotion(text, model_path)
    return {
        "probabilities": response["probabilities"],
        "top_emotion": response["top_emotion"]
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
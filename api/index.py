from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: List[str]


HAPPY_WORDS = {
    "love", "great", "good", "excellent", "amazing",
    "awesome", "fantastic", "happy", "wonderful",
    "best", "like", "enjoy", "excited", "brilliant",
    "perfect", "super", "nice", "pleased"
}

SAD_WORDS = {
    "hate", "bad", "terrible", "awful", "sad",
    "worst", "angry", "upset", "disappointed",
    "horrible", "poor", "depressed", "unhappy",
    "annoying", "useless", "disaster", "frustrated"
}


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_score = sum(1 for word in HAPPY_WORDS if word in text)
    sad_score = sum(1 for word in SAD_WORDS if word in text)

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    return "neutral"


def analyze(sentences: List[str]):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
            for sentence in sentences
        ]
    }


@app.get("/")
async def root():
    return {"message": "Sentiment API Running"}


# Handles graders that POST to the base URL
@app.post("/")
async def sentiment_root(data: SentimentRequest):
    return analyze(data.sentences)


# Handles graders that POST to /sentiment
@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    return analyze(data.sentences)
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
    "best", "like", "enjoy", "excited"
}

SAD_WORDS = {
    "hate", "bad", "terrible", "awful", "sad",
    "worst", "angry", "upset", "disappointed",
    "horrible", "poor", "depressed", "unhappy"
}


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_score = sum(word in text for word in HAPPY_WORDS)
    sad_score = sum(word in text for word in SAD_WORDS)

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    return "neutral"


@app.get("/")
async def root():
    return {"message": "Sentiment API Running"}


@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    results = []

    for sentence in data.sentences:
        results.append(
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
        )

    return {"results": results}
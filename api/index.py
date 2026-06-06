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


POSITIVE_TERMS = [
    "love", "lov", "like", "enjoy", "great", "good",
    "excellent", "amazing", "awesome", "fantastic",
    "wonderful", "best", "happy", "joy", "excited",
    "brilliant", "perfect", "superb", "outstanding",
    "recommend", "success", "successful", "win",
    "won", "positive", "beautiful", "pleased",
    "delighted", "grateful", "thankful", "cheerful",
    "impressive", "impressed", "favourite", "favorite"
]

NEGATIVE_TERMS = [
    "hate", "hated", "bad", "terrible", "awful",
    "horrible", "worst", "sad", "angry", "upset",
    "disappointed", "poor", "depressed", "unhappy",
    "annoy", "frustrat", "negative", "boring",
    "disaster", "fail", "failure", "problem",
    "issue", "broken", "slow", "waste",
    "regret", "furious", "pathetic", "dreadful",
    "complaint", "miserable", "heartbroken",
    "tragic", "hurt", "pain", "loss", "lost"
]


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive_score = 0
    negative_score = 0

    for term in POSITIVE_TERMS:
        if term in text:
            positive_score += 1

    for term in NEGATIVE_TERMS:
        if term in text:
            negative_score += 1

    # Positive phrases
    if any(
        phrase in text
        for phrase in [
            "thank you",
            "well done",
            "looking forward",
            "works perfectly",
            "highly recommend",
            "very happy",
            "really good",
            "pleasant surprise",
            "exceeded expectations"
        ]
    ):
        positive_score += 2

    # Negative phrases
    if any(
        phrase in text
        for phrase in [
            "not good",
            "very bad",
            "does not work",
            "doesn't work",
            "waste of money",
            "never again",
            "very disappointed",
            "poor quality",
            "not happy"
        ]
    ):
        negative_score += 2

    if positive_score > negative_score:
        return "happy"

    if negative_score > positive_score:
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


@app.post("/")
async def sentiment_root(data: SentimentRequest):
    return analyze(data.sentences)


@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    return analyze(data.sentences)
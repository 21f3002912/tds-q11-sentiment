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
    "love", "loved", "like", "liked", "enjoy", "enjoyed",
    "great", "excellent", "amazing", "awesome", "fantastic",
    "wonderful", "best", "good", "happy", "excited",
    "pleased", "perfect", "brilliant", "superb", "outstanding",
    "delightful", "positive", "beautiful", "fun", "recommend",
    "recommended", "impressed", "satisfied", "success",
    "successful", "nice", "favorite", "favourite", "glad",
    "thrilled", "incredible", "joy", "joyful", "helpful",
    "excellent", "lovely", "charming"
}

SAD_WORDS = {
    "hate", "hated", "bad", "terrible", "awful", "horrible",
    "worst", "sad", "angry", "upset", "disappointed",
    "poor", "depressed", "unhappy", "annoying", "useless",
    "frustrated", "negative", "boring", "disaster", "fail",
    "failed", "failure", "problem", "problems", "issue",
    "issues", "broken", "slow", "waste", "regret",
    "dislike", "furious", "pathetic", "mediocre",
    "dreadful", "complaint", "complaints", "disappointing",
    "unacceptable", "bug", "bugs", "error", "errors"
}


POSITIVE_PHRASES = [
    "thank you",
    "well done",
    "looking forward",
    "works perfectly",
    "highly recommend",
    "very happy",
    "very good",
    "really good",
    "extremely happy",
    "pleasant surprise",
    "exceeded expectations"
]

NEGATIVE_PHRASES = [
    "not good",
    "very bad",
    "doesn't work",
    "does not work",
    "waste of money",
    "never again",
    "highly disappointed",
    "very disappointed",
    "extremely disappointed",
    "not happy",
    "poor quality"
]


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_score = 0
    sad_score = 0

    for word in HAPPY_WORDS:
        if word in text:
            happy_score += 1

    for word in SAD_WORDS:
        if word in text:
            sad_score += 1

    for phrase in POSITIVE_PHRASES:
        if phrase in text:
            happy_score += 2

    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            sad_score += 2

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


@app.post("/")
async def sentiment_root(data: SentimentRequest):
    return analyze(data.sentences)


@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    return analyze(data.sentences)
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
    "love", "loved", "like", "liked", "enjoy", "enjoyed",
    "great", "good", "excellent", "amazing", "awesome",
    "fantastic", "wonderful", "best", "happy", "joy",
    "excited", "brilliant", "perfect", "superb",
    "outstanding", "recommend", "recommended",
    "success", "successful", "win", "won",
    "positive", "beautiful", "pleased", "delighted",
    "grateful", "thankful", "cheerful", "impressive",
    "impressed", "nice", "favourite", "favorite",
    "thrilled", "glad", "pleasure", "excellent"
]

NEGATIVE_TERMS = [
    "hate", "hated", "bad", "terrible", "awful",
    "horrible", "worst", "sad", "angry", "upset",
    "disappointed", "poor", "depressed", "unhappy",
    "annoying", "frustrating", "negative", "boring",
    "disaster", "fail", "failed", "failure",
    "problem", "problems", "issue", "issues",
    "broken", "slow", "waste", "regret",
    "furious", "pathetic", "dreadful",
    "complaint", "complaints", "miserable",
    "heartbroken", "tragic", "hurt", "pain",
    "loss", "lost", "unfortunate", "sorry"
]


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive_score = 0
    negative_score = 0

    for word in POSITIVE_TERMS:
        if word in text:
            positive_score += 1

    for word in NEGATIVE_TERMS:
        if word in text:
            negative_score += 1

    positive_phrases = [
        "thank you",
        "well done",
        "looking forward",
        "highly recommend",
        "very happy",
        "really good",
        "pleasant surprise",
        "exceeded expectations",
        "works perfectly",
        "great job"
    ]

    negative_phrases = [
        "not good",
        "very bad",
        "does not work",
        "doesn't work",
        "waste of money",
        "never again",
        "very disappointed",
        "poor quality",
        "not happy",
        "highly disappointed"
    ]

    for phrase in positive_phrases:
        if phrase in text:
            positive_score += 2

    for phrase in negative_phrases:
        if phrase in text:
            negative_score += 2

    if positive_score > negative_score:
        return "happy"

    if negative_score > positive_score:
        return "sad"

    # Final tie-breaker
    if any(word in text for word in ["thank", "thanks", "glad", "pleased"]):
        return "happy"

    if any(word in text for word in ["sorry", "regret", "unfortunately"]):
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
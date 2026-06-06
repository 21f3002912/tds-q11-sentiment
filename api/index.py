from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: List[str]


def classify_sentiment(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)["compound"]

    if score >= 0.2:
        return "happy"
    elif score <= -0.2:
        return "sad"
    else:
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
import os
import pickle
from collections import Counter

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="listen-ai-nlp")

# 載入訓練好的模型
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)
    vectorizer = artifacts["vectorizer"]
    model = artifacts["model"]


def classify_text(text: str) -> tuple[str, float]:
    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    prob = model.predict_proba(vec).max()
    return label, round(float(prob), 4)


class SentimentRequest(BaseModel):
    texts: list[str]


class SentimentItem(BaseModel):
    text: str
    label: str
    score: float


class SentimentResponse(BaseModel):
    sentiment_percentage: dict[str, float]
    classifications: list[SentimentItem]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "nlp", "port": os.getenv("NLP_PORT", "8001")}


@app.post("/sentiment", response_model=SentimentResponse)
def sentiment(req: SentimentRequest) -> SentimentResponse:
    results: list[SentimentItem] = []
    counts: Counter = Counter({"positive": 0, "neutral": 0, "negative": 0})

    for text in req.texts:
        label, score = classify_text(text)
        counts[label] += 1
        results.append(SentimentItem(text=text, label=label, score=score))

    total = max(1, len(req.texts))
    sentiment_percentage = {
        "positive": round((counts["positive"] / total) * 100, 2),
        "neutral": round((counts["neutral"] / total) * 100, 2),
        "negative": round((counts["negative"] / total) * 100, 2),
    }

    return SentimentResponse(
        sentiment_percentage=sentiment_percentage,
        classifications=results,
    )
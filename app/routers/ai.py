from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.portfoliotable import Portfolio
from app.database import get_db
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

class QuestionRequest(BaseModel):
    question: str

# Helper function
def call_gemini(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("GEMINI RESPONSE:", result)

    if "error" in result:
        raise Exception(result["error"]["message"])

    return result["candidates"][0]["content"]["parts"][0]["text"]

# GET AVAILABLE MODELS
@router.get("/models")
def get_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    response = requests.get(url)
    result = response.json()
    models = [m["name"] for m in result.get("models", [])]
    return {"available_models": models}

# FEATURE 1 - Stock Advice
@router.post("/advice")
def get_stock_advice(
    request: QuestionRequest,
    current_user = Depends(get_current_user)
):
    try:
        prompt = f"""
        You are a helpful stock market assistant.
        User: {current_user.username}
        Question: {request.question}
        Give short helpful advice in 2-3 sentences.
        Mention this is not professional financial advice.
        """
        advice = call_gemini(prompt)
        return {
            "question": request.question,
            "advice": advice,
            "disclaimer": "AI generated advice only."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# FEATURE 2 - Portfolio Analysis
@router.post("/analyze-portfolio")
def analyze_portfolio(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        portfolio = db.query(Portfolio).filter(
            Portfolio.user_id == current_user.id
        ).all()

        if not portfolio:
            return {"analysis": "No portfolio found. Start buying stocks!"}

        portfolio_summary = ""
        for item in portfolio:
            portfolio_summary += f"""
            Stock: {item.stock_symbol}
            Quantity: {item.quantity}
            Average Price: {item.avg_price}
            """

        prompt = f"""
        You are a stock portfolio advisor.
        User: {current_user.username}
        Their portfolio:
        {portfolio_summary}
        Analyze and give advice on:
        1. Diversification
        2. Risk level
        3. Suggestions
        Keep it short. Max 5 sentences.
        """

        analysis = call_gemini(prompt)
        return {
            "portfolio_summary": [
                {
                    "stock": item.stock_symbol,
                    "quantity": item.quantity,
                    "avg_price": item.avg_price
                }
                for item in portfolio
            ],
            "analysis": analysis,
            "disclaimer": "AI generated advice only"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 
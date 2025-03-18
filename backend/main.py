from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import ChatHistory
from .crud import save_chat, get_chat_history
from transformers import pipeline

app = FastAPI()

try:
    chat_pipeline = pipeline("text-generation", model="facebook/opt-1.3b", device=-1)
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print("Lightweight models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat/")
def chat(user_input: str, db: Session = Depends(get_db)):
    try:
        if not user_input.strip():
            raise HTTPException(status_code=400, detail="User input cannot be empty")

        response = chat_pipeline(user_input, max_length=100, temperature=0.3, top_p=0.3, do_sample=True)
        bot_response = response[0]['generated_text'].strip()

        sentiment_result = sentiment_pipeline(user_input)[0]['label']

        save_chat(db, user_input, bot_response, sentiment_result)

        return {"response": bot_response, "sentiment": sentiment_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/")
def chat_history(db: Session = Depends(get_db)):
    try:
        chats = get_chat_history(db)
        return [
            {
                "user": chat.user_message,
                "bot": chat.bot_response,
                "sentiment": chat.sentiment,
                "timestamp": chat.timestamp
            }
            for chat in chats
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

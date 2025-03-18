from sqlalchemy.orm import Session
from .models import ChatHistory

def save_chat(session: Session, user_message: str, bot_response: str, sentiment: str):
    chat_entry = ChatHistory(user_message=user_message, bot_response=bot_response, sentiment=sentiment)
    session.add(chat_entry)
    session.commit()
    return chat_entry

def get_chat_history(session: Session, limit=10):
    return session.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(limit).all()

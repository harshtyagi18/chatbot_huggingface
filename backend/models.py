from sqlalchemy import Column, Integer, String, Text, DateTime
from .db import Base
import datetime

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

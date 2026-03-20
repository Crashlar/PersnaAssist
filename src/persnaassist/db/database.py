from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pathlib import Path

# ==============================
# DATABASE SETUP
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_DIR}/assistant.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ==============================
# TABLE DEFINITION
# ==============================

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ==============================
# CREATE TABLES
# ==============================

def init_db():
    Base.metadata.create_all(bind=engine)

# ==============================
# DATABASE OPERATIONS
# ==============================

class DatabaseManager:
    def __init__(self):
        self.session = SessionLocal()

    def save_conversation(self, user_input: str, assistant_response: str):
        """
        Save conversation to database
        """
        conversation = Conversation(
            user_input=user_input,
            assistant_response=assistant_response
        )
        self.session.add(conversation)
        self.session.commit()

    def get_last_conversations(self, limit=5):
        """
        Fetch last N conversations
        """
        return (
            self.session.query(Conversation)
            .order_by(Conversation.timestamp.desc())
            .limit(limit)
            .all()
        )

    def close(self):
        """
        Close database session
        """
        self.session.close()
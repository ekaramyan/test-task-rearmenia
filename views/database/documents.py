from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from database import Base


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    contracts = relationship("Contract", back_populates="owner")
    messages = relationship("ChatMessage", back_populates="user")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    type = Column(String)
    file_path = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")
    risk_score = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)
    summary = Column(Text, nullable=True)

    owner = relationship("User", back_populates="contracts")
    analysis = relationship("Analysis", back_populates="contract", uselist=False)
    deadlines = relationship("Deadline", back_populates="contract")
    chat_messages = relationship("ChatMessage", back_populates="contract")
    report = relationship("Report", back_populates="contract", uselist=False)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    summary = Column(Text)
    risk_score = Column(Float)
    risk_level = Column(String)
    risk_categories = Column(Text) # JSON string
    important_clauses = Column(Text) # JSON string
    obligations = Column(Text) # JSON string
    important_dates = Column(Text) # JSON string
    missing_clauses = Column(Text) # JSON string
    recommendations = Column(Text) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    contract = relationship("Contract", back_populates="analysis")


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    date_type = Column(String)
    deadline_date = Column(DateTime)
    description = Column(String)
    status = Column(String)

    contract = relationship("Contract", back_populates="deadlines")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    role = Column(String) # user or ai
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    contract = relationship("Contract", back_populates="chat_messages")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    report_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    contract = relationship("Contract", back_populates="report")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, ChatMessage, Contract
from backend.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.get("/{contract_id}")
def get_chat_history(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    messages = db.query(ChatMessage).filter(ChatMessage.contract_id == contract_id).all()
    return messages

@router.post("/{contract_id}")
def send_message(contract_id: int, request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    user_message = ChatMessage(
        user_id=current_user.id,
        contract_id=contract.id,
        role="user",
        message=request.message
    )
    db.add(user_message)
    
    ai_message = ChatMessage(
        user_id=current_user.id,
        contract_id=contract.id,
        role="ai",
        message=f"Mock AI response to: {request.message}"
    )
    db.add(ai_message)
    
    db.commit()
    db.refresh(ai_message)
    return {"user_message": user_message, "ai_message": ai_message}

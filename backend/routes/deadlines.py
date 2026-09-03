from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Deadline, Contract
from backend.auth import get_current_user

router = APIRouter(prefix="/deadlines", tags=["deadlines"])

@router.get("/")
def get_all_deadlines(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contracts = db.query(Contract).filter(Contract.user_id == current_user.id).all()
    contract_ids = [c.id for c in contracts]
    
    deadlines = db.query(Deadline).filter(Deadline.contract_id.in_(contract_ids)).all()
    return deadlines

@router.get("/{contract_id}")
def get_contract_deadlines(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    deadlines = db.query(Deadline).filter(Deadline.contract_id == contract_id).all()
    return deadlines

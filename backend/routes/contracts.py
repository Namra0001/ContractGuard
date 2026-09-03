from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Contract
from backend.auth import get_current_user
import os

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.get("/")
def get_contracts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contracts = db.query(Contract).filter(Contract.user_id == current_user.id).all()
    return contracts

@router.post("/")
def upload_contract(name: str, type: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    file_path = f"uploads/{file.filename}"
    # Ensure directory exists
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    new_contract = Contract(
        user_id=current_user.id,
        name=name,
        type=type,
        file_path=file_path
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract

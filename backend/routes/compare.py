from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Contract
from backend.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/compare", tags=["compare"])

class CompareRequest(BaseModel):
    contract_id_1: int
    contract_id_2: int

@router.post("/")
def compare_contracts(request: CompareRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    c1 = db.query(Contract).filter(Contract.id == request.contract_id_1, Contract.user_id == current_user.id).first()
    c2 = db.query(Contract).filter(Contract.id == request.contract_id_2, Contract.user_id == current_user.id).first()
    
    if not c1 or not c2:
        raise HTTPException(status_code=404, detail="One or both contracts not found")
    
    return {
        "comparison_result": "Mock comparison results between the two contracts.",
        "contract_1": c1.name,
        "contract_2": c2.name
    }

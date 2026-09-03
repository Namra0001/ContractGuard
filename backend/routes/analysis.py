from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Contract, Analysis
from backend.auth import get_current_user

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/{contract_id}")
def get_analysis(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    analysis = db.query(Analysis).filter(Analysis.contract_id == contract_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis

@router.post("/{contract_id}")
def run_analysis(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Mock analysis generation
    new_analysis = Analysis(
        contract_id=contract.id,
        summary="This is a mock summary of the contract.",
        risk_score=4.5,
        risk_level="Medium",
        risk_categories="{}",
        important_clauses="{}",
        obligations="{}",
        important_dates="{}",
        missing_clauses="{}",
        recommendations="{}"
    )
    db.add(new_analysis)
    
    contract.status = "Analyzed"
    contract.risk_score = 4.5
    contract.risk_level = "Medium"
    contract.summary = new_analysis.summary
    
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

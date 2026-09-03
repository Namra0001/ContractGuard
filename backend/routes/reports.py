from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Report, Contract
from backend.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/{contract_id}")
def get_report(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    report = db.query(Report).filter(Report.contract_id == contract_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return report

@router.post("/{contract_id}")
def generate_report(contract_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id, Contract.user_id == current_user.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    new_report = Report(
        contract_id=contract_id,
        report_path=f"reports/report_{contract_id}.pdf"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

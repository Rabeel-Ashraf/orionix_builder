from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User
from app.models.credit import CreditTransaction
from app.services.credit_service import credit_service

router = APIRouter()

@router.get("/credits/balance")
async def get_credit_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get current credit balance"""
    balance = credit_service.get_credit_balance(db, current_user.id)
    return {"balance": balance, "user_id": current_user.id}

@router.post("/credits/use")
async def use_credits(
    amount: int,
    service: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Use credits for a service"""
    success = credit_service.deduct_credits(db, current_user.id, amount, service)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    new_balance = credit_service.get_credit_balance(db, current_user.id)
    return {
        "success": True,
        "amount_used": amount,
        "new_balance": new_balance,
        "service": service
    }

@router.get("/credits/transactions")
async def get_transaction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
    limit: int = 50
):
    """Get credit transaction history"""
    transactions = credit_service.get_transaction_history(db, current_user.id, limit)
    return {
        "transactions": transactions,
        "count": len(transactions)
    }

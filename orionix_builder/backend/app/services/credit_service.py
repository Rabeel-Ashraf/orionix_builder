from sqlalchemy.orm import Session
from sqlmodel import select
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.models.credit import CreditTransaction
from app.models.user import User

logger = logging.getLogger(__name__)

class CreditService:
    def get_credit_balance(self, db: Session, user_id: str) -> int:
        """Get current credit balance for user"""
        statement = select(CreditTransaction).where(CreditTransaction.user_id == user_id)
        transactions = db.exec(statement).all()
        return sum(t.amount for t in transactions)
    
    def has_sufficient_credits(self, db: Session, user_id: str, amount: int) -> bool:
        """Check if user has sufficient credits"""
        balance = self.get_credit_balance(db, user_id)
        return balance >= amount
    
    def deduct_credits(self, db: Session, user_id: str, amount: int, service: str) -> bool:
        """Deduct credits from user account"""
        if not self.has_sufficient_credits(db, user_id, amount):
            return False
        
        transaction = CreditTransaction(
            user_id=user_id,
            amount=-amount,
            type=f"usage_{service}",
            description=f"Credits used for {service}"
        )
        db.add(transaction)
        db.commit()
        
        logger.info(f"Deducted {amount} credits from user {user_id} for {service}")
        return True
    
    def add_credits(self, db: Session, user_id: str, amount: int, reason: str, description: str = ""):
        """Add credits to user account"""
        transaction = CreditTransaction(
            user_id=user_id,
            amount=amount,
            type=reason,
            description=description
        )
        db.add(transaction)
        db.commit()
        
        logger.info(f"Added {amount} credits to user {user_id} for {reason}")
    
    def refill_free_credits(self, db: Session):
        """Refill free credits for all free plan users (called 2x per month)"""
        free_users = db.query(User).filter(User.plan == "free").all()
        refilled_count = 0
        
        for user in free_users:
            current_balance = self.get_credit_balance(db, user.id)
            if current_balance < 50:
                credits_to_add = 50 - current_balance
                self.add_credits(
                    db=db,
                    user_id=user.id,
                    amount=credits_to_add,
                    reason="monthly_refill",
                    description="Monthly free credit refill"
                )
                refilled_count += 1
        
        logger.info(f"Refilled credits for {refilled_count} free users")
        return refilled_count
    
    def get_transaction_history(self, db: Session, user_id: str, limit: int = 50) -> List[CreditTransaction]:
        """Get credit transaction history for user"""
        statement = (select(CreditTransaction)
                    .where(CreditTransaction.user_id == user_id)
                    .order_by(CreditTransaction.created_at.desc())
                    .limit(limit))
        return db.exec(statement).all()

# Global instance
credit_service = CreditService()

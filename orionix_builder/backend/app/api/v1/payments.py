from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlmodel import Session
import stripe
import json

from app.services.stripe_service import stripe_service
from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User

router = APIRouter()

@router.post("/payments/create-checkout-session")
async def create_checkout_session(
    price_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create Stripe checkout session for subscription"""
    success_url = "http://localhost:3000/dashboard?success=true"
    cancel_url = "http://localhost:3000/pricing?canceled=true"
    
    session = stripe_service.create_checkout_session(
        user=current_user,
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    if not session:
        raise HTTPException(status_code=400, detail="Could not create checkout session")
    
    return {"checkout_url": session.url, "session_id": session.id}

@router.post("/payments/create-credit-session")
async def create_credit_purchase_session(
    credit_package: str,
    amount: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create Stripe checkout session for credit purchase"""
    success_url = "http://localhost:3000/dashboard?credits_added=true"
    cancel_url = "http://localhost:3000/dashboard?credits_canceled=true"
    
    session = stripe_service.create_credit_purchase_session(
        user=current_user,
        credit_package=credit_package,
        amount=amount,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    if not session:
        raise HTTPException(status_code=400, detail="Could not create credit purchase session")
    
    return {"checkout_url": session.url, "session_id": session.id}

@router.post("/payments/webhook")
async def stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session)
):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        result = stripe_service.handle_webhook(payload, sig_header)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payments/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    plans = stripe_service.get_subscription_plans()
    return {"plans": plans}

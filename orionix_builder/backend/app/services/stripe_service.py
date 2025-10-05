import stripe
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from app.core.config import settings
from app.models.user import User
from app.services.credit_service import credit_service

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    def __init__(self):
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    def create_checkout_session(
        self, 
        user: User, 
        price_id: str, 
        success_url: str, 
        cancel_url: str
    ) -> Optional[stripe.checkout.Session]:
        """Create Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                customer_email=user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user.id,
                    'user_email': user.email
                },
                subscription_data={
                    'metadata': {
                        'user_id': user.id,
                        'user_email': user.email
                    }
                }
            )
            return session
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            return None
    
    def create_credit_purchase_session(
        self,
        user: User,
        credit_package: str,
        amount: int,
        success_url: str,
        cancel_url: str
    ) -> Optional[stripe.checkout.Session]:
        """Create session for purchasing credits"""
        try:
            # Map credit packages to prices
            price_map = {
                "100_credits": "price_credits_100",
                "500_credits": "price_credits_500", 
                "1000_credits": "price_credits_1000"
            }
            
            session = stripe.checkout.Session.create(
                customer_email=user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_map.get(credit_package, "price_credits_100"),
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user.id,
                    'credit_package': credit_package,
                    'credit_amount': amount
                }
            )
            return session
        except Exception as e:
            logger.error(f"Error creating credit purchase session: {str(e)}")
            return None
    
    def handle_webhook(self, payload: bytes, sig_header: str) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            
            # Handle different event types
            if event['type'] == 'checkout.session.completed':
                return self._handle_checkout_completed(event)
            elif event['type'] == 'customer.subscription.updated':
                return self._handle_subscription_updated(event)
            elif event['type'] == 'customer.subscription.deleted':
                return self._handle_subscription_deleted(event)
            elif event['type'] == 'invoice.payment_succeeded':
                return self._handle_invoice_payment_succeeded(event)
            else:
                return {"status": "ignored", "event_type": event['type']}
                
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            raise e
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            raise e
    
    def _handle_checkout_completed(self, event: stripe.Event) -> Dict[str, Any]:
        """Handle checkout.session.completed event"""
        session = event['data']['object']
        user_id = session['metadata'].get('user_id')
        credit_package = session['metadata'].get('credit_package')
        
        # This would typically update user plan in database
        # For now, we'll just log it
        logger.info(f"Checkout completed for user {user_id}, package: {credit_package}")
        
        return {"status": "processed", "event": "checkout_completed"}
    
    def get_subscription_plans(self) -> list:
        """Get available subscription plans"""
        try:
            prices = stripe.Price.list(active=True, limit=10)
            plans = []
            
            for price in prices.auto_paging_iter():
                product = stripe.Product.retrieve(price.product)
                plans.append({
                    'price_id': price.id,
                    'product_name': product.name,
                    'amount': price.unit_amount / 100 if price.unit_amount else 0,
                    'currency': price.currency,
                    'interval': price.recurring.interval if price.recurring else 'one_time',
                    'metadata': product.metadata
                })
            
            return plans
        except Exception as e:
            logger.error(f"Error fetching subscription plans: {str(e)}")
            return []

# Global instance
stripe_service = StripeService()

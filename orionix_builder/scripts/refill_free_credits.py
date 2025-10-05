#!/usr/bin/env python3
"""
Script to manually refill free credits for testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.database import get_session
from backend.app.services.credit_service import CreditService

def main():
    """Manually refill free credits"""
    credit_service = CreditService()
    
    with next(get_session()) as db:
        refilled_count = credit_service.refill_free_credits(db)
        print(f"✅ Successfully refilled credits for {refilled_count} free users")

if __name__ == "__main__":
    main()

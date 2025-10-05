from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime

from app.services.llm_service import llm_service, LLMProvider
from app.services.credit_service import CreditService
from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    preferred_model: Optional[LLMProvider] = None

class GenerateResponse(BaseModel):
    content: str
    model_used: str
    credits_used: int

@router.post("/generate")
async def generate_content(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_session)
):
    """Generate content using AI with streaming"""
    
    credit_service = CreditService()
    
    # Check if user has enough credits (estimate 1 credit per 100 characters)
    estimated_credits = max(1, len(request.prompt) // 100)
    if not credit_service.has_sufficient_credits(db, current_user.id, estimated_credits):
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    async def generate():
        content = ""
        model_used = None
        
        try:
            async for chunk in llm_service.generate_stream(
                prompt=request.prompt,
                user_plan=current_user.plan,
                preferred_model=request.preferred_model
            ):
                content += chunk
                # Send as SSE
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Deduct credits after successful generation
            actual_credits = max(1, len(content) // 100)
            credit_service.deduct_credits(db, current_user.id, actual_credits, "ai_generation")
            
            # Send completion signal
            yield f"data: {json.dumps({'complete': True, 'credits_used': actual_credits})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

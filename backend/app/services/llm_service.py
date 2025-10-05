import os
import asyncio
from enum import Enum
from typing import AsyncGenerator, Optional, List
import aiohttp
import openai
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    QWEN = "qwen"

class LLMService:
    def __init__(self):
        self.clients = {
            LLMProvider.DEEPSEEK: AsyncOpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1"
            ) if os.getenv("DEEPSEEK_API_KEY") else None,
            LLMProvider.OPENAI: AsyncOpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            ) if os.getenv("OPENAI_API_KEY") else None,
            LLMProvider.QWEN: AsyncOpenAI(
                api_key=os.getenv("QWEN_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            ) if os.getenv("QWEN_API_KEY") else None,
        }
    
    async def generate_stream(
        self,
        prompt: str,
        user_plan: str = "free",
        preferred_model: Optional[LLMProvider] = None
    ) -> AsyncGenerator[str, None]:
        """Generate stream with failover logic"""
        
        model_priority = self._get_model_priority(user_plan, preferred_model)
        last_error = None
        
        for model in model_priority:
            client = self.clients.get(model)
            if not client:
                logger.warning(f"Model {model} not configured, skipping")
                continue
                
            try:
                logger.info(f"Attempting generation with {model}")
                async for chunk in self._call_model_stream(client, model, prompt):
                    yield chunk
                logger.info(f"Successfully completed generation with {model}")
                return
                
            except Exception as e:
                last_error = e
                logger.error(f"Model {model} failed: {str(e)}")
                continue
        
        raise Exception(f"All LLM providers failed. Last error: {str(last_error)}")
    
    def _get_model_priority(self, user_plan: str, preferred_model: Optional[LLMProvider]) -> List[LLMProvider]:
        """Determine model priority based on user plan and preferences"""
        if preferred_model:
            return [preferred_model] + self._get_fallback_models(preferred_model)
        
        if user_plan == "enterprise":
            return [LLMProvider.OPENAI, LLMProvider.DEEPSEEK, LLMProvider.QWEN]
        elif user_plan == "pro":
            return [LLMProvider.DEEPSEEK, LLMProvider.OPENAI, LLMProvider.QWEN]
        else:  # free
            return [LLMProvider.DEEPSEEK, LLMProvider.QWEN]
    
    def _get_fallback_models(self, preferred: LLMProvider) -> List[LLMProvider]:
        """Get fallback models for a preferred model"""
        fallbacks = {
            LLMProvider.DEEPSEEK: [LLMProvider.OPENAI, LLMProvider.QWEN],
            LLMProvider.OPENAI: [LLMProvider.DEEPSEEK, LLMProvider.QWEN],
            LLMProvider.QWEN: [LLMProvider.DEEPSEEK, LLMProvider.OPENAI],
        }
        return fallbacks.get(preferred, [LLMProvider.DEEPSEEK, LLMProvider.OPENAI])
    
    async def _call_model_stream(self, client: AsyncOpenAI, model: LLMProvider, prompt: str) -> AsyncGenerator[str, None]:
        """Make actual LLM calls with streaming"""
        
        model_map = {
            LLMProvider.DEEPSEEK: "deepseek-chat",
            LLMProvider.OPENAI: "gpt-4",
            LLMProvider.QWEN: "qwen-plus",
        }
        
        model_name = model_map.get(model, "deepseek-chat")
        
        try:
            stream = await client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                max_tokens=4000,
                temperature=0.7
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error in model {model} stream: {str(e)}")
            raise e

# Global instance
llm_service = LLMService()

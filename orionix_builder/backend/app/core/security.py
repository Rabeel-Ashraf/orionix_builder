import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_secure_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def verify_token(plain_token: str, hashed_token: str) -> bool:
    return pwd_context.verify(plain_token, hashed_token)

def get_token_hash(token: str) -> str:
    return pwd_context.hash(token)

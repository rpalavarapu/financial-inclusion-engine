import jwt
import time
import os
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from pydantic import BaseModel
from typing import Optional

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "financial_inclusion_engine_secure_jwt_secret_2026")
ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 3600 * 24 # 24 hours

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Demo API Key for machine-to-machine integrations
VALID_API_KEYS = {
    os.getenv("UNDERWRITING_API_KEY", "fie_live_demo_api_key_850")
}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = TOKEN_EXPIRE_SECONDS

def create_access_token(subject: str, role: str = "underwriter") -> str:
    payload = {
        "sub": subject,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRE_SECONDS
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme), api_key: Optional[str] = Depends(api_key_header)) -> dict:
    """
    Verifies either a valid Bearer JWT Token or an X-API-Key header.
    In demo mode, unauthenticated public dashboard requests are assigned a guest principal.
    """
    if api_key and api_key in VALID_API_KEYS:
        return {"sub": "api_client", "role": "machine", "auth_method": "api_key"}

    if credentials and credentials.credentials:
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            return {"sub": payload.get("sub"), "role": payload.get("role"), "auth_method": "jwt"}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Guest Underwriter session
    return {"sub": "guest_underwriter", "role": "underwriter", "auth_method": "guest_demo"}

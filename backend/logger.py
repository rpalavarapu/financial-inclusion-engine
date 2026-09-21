import time
import json
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.security import SecuritySanitizer

logger = logging.getLogger("CloudWatchAuditLogger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

class CloudWatchLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that records structured CloudWatch JSON audit entries for every request.
    Includes request ID, duration (ms), HTTP method, path, status, and PII masking.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "trace_id": request_id,
            "method": request.method,
            "path": SecuritySanitizer.mask_pii_string(str(request.url.path)),
            "status_code": response.status_code,
            "latency_ms": duration_ms,
            "client_ip": request.client.host if request.client else "unknown"
        }
        
        logger.info(json.dumps(log_entry))
        response.headers["X-Trace-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

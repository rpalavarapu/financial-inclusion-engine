import hashlib
import re
from typing import Dict, Any

class SecuritySanitizer:
    """
    Security & Responsible Data Handling engine.
    Ensures PII redaction, secret protection, and cryptographic integrity hashes.
    """
    
    @staticmethod
    def mask_pii_string(text: str) -> str:
        """Masks sensitive entities like emails, phone numbers, and SSNs/National IDs."""
        if not text:
            return ""
        # Mask emails (e.g., j***e@domain.com)
        text = re.sub(r'([a-zA-Z0-9_.+-])[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r'\1***@\2', text)
        # Mask phone numbers
        text = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', r'***-***-****', text)
        # Mask SSN / National Identifiers
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', r'XXX-XX-XXXX', text)
        return text

    @staticmethod
    def sanitize_dictionary(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively scrubs secrets or tokens if accidentally injected into payloads."""
        sanitized = {}
        forbidden_keys = {"aws_secret_access_key", "aws_bearer_token_bedrock", "secret_key", "password", "token"}
        
        for k, v in data.items():
            if k.lower() in forbidden_keys:
                sanitized[k] = "[REDACTED_SECRET]"
            elif isinstance(v, dict):
                sanitized[k] = SecuritySanitizer.sanitize_dictionary(v)
            elif isinstance(v, str):
                sanitized[k] = SecuritySanitizer.mask_pii_string(v)
            else:
                sanitized[k] = v
        return sanitized

    @staticmethod
    def generate_audit_hash(data: Dict[str, Any]) -> str:
        """Generates SHA-256 cryptographic proof hash for compliance audit records."""
        raw = str(sorted(data.items())).encode('utf-8')
        return hashlib.sha256(raw).hexdigest()

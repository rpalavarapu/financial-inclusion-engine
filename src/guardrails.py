import re
from typing import Dict, Any, List, Tuple

class PromptGuardrails:
    """
    AI Safety & Guardrails engine.
    Detects adversarial prompt injections and enforces responsible AI constraints.
    """
    
    INJECTION_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"system prompt",
        r"bypass (ecoa|fcra|fairness|underwriting)",
        r"jailbreak",
        r"override credit score",
        r"force approval"
    ]

    @staticmethod
    def validate_prompt_safety(prompt: str) -> Tuple[bool, str]:
        """Validates if prompt contains adversarial injection patterns."""
        if not prompt:
            return True, "Safe"
        
        prompt_lower = prompt.lower()
        for pattern in PromptGuardrails.INJECTION_PATTERNS:
            if re.search(pattern, prompt_lower):
                return False, f"Guardrail Violation: Adversarial pattern detected ({pattern})"
        
        return True, "Safe"

    @staticmethod
    def validate_signal_ranges(signals: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Validates numerical signal boundaries (0.00 to 1.00)."""
        errors = []
        for key, val in signals.items():
            if not isinstance(val, (int, float)):
                errors.append(f"Signal '{key}' must be numeric.")
            elif val < 0.0 or val > 1.0:
                errors.append(f"Signal '{key}' value {val} out of bounds [0.0, 1.0].")
        return len(errors) == 0, errors

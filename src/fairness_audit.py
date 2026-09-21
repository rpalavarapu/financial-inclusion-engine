import numpy as np

class BiasFairnessAuditor:
    """
    Evaluates algorithmic fairness across underserved sub-demographics
    (e.g., urban gig workers vs. rural agricultural workers) to ensure
    disparate impact ratios satisfy regulatory standards (80% rule).
    """
    def __init__(self):
        pass

    def calculate_disparate_impact(self, privileged_approval_rate: float = 0.82, unprivileged_approval_rate: float = 0.78) -> dict:
        """Calculates Disparate Impact Ratio (DIR). DIR >= 0.80 indicates non-discriminatory scoring."""
        dir_ratio = unprivileged_approval_rate / privileged_approval_rate if privileged_approval_rate > 0 else 1.0
        
        is_compliant = dir_ratio >= 0.80
        return {
            "disparate_impact_ratio": round(dir_ratio, 3),
            "is_compliant": is_compliant,
            "status": "PASS: No Unfair Bias Detected" if is_compliant else "FAIL: High Disparate Impact Detected"
        }

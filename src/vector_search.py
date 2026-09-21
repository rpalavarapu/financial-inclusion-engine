import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticApplicantMatcher:
    """
    Simulates pgvector / Vector DB semantic retrieval.
    Matches current applicant's qualitative cashflow profile against historical records.
    """
    def __init__(self):
        # Simulated vector database embeddings for past approved/rejected applicants
        self.historical_db = [
            {"id": "HIST_001", "vector": np.array([0.8, 0.9, 0.7, 0.85]), "outcome": "Approved", "note": "Consistent gig income & zero bill defaults."},
            {"id": "HIST_002", "vector": np.array([0.3, 0.2, 0.4, 0.10]), "outcome": "Rejected", "note": "High recharge volatility & frequent overdrafts."},
            {"id": "HIST_003", "vector": np.array([0.9, 0.85, 0.8, 0.92]), "outcome": "Approved", "note": "High utility payment consistency."},
        ]

    def find_similar_profiles(self, applicant_vector: np.ndarray, top_k: int = 2):
        results = []
        for record in self.historical_db:
            sim = cosine_similarity([applicant_vector], [record["vector"]])[0][0]
            results.append({
                "id": record["id"],
                "similarity": round(float(sim), 4),
                "outcome": record["outcome"],
                "note": record["note"]
            })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

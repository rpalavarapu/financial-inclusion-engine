import pandas as pd
import numpy as np
import lightgbm as lgb
import shap

class DynamicRiskEngine:
    """
    Evaluates risk for thin-file / unbanked applicants using alternative data signals.
    Calculates dynamic credit scores and derives SHAP explainability factors.
    """
    def __init__(self):
        self.feature_names = [
            "utility_payment_consistency",
            "monthly_recharge_frequency",
            "wallet_cash_inflow_stability",
            "gig_platform_payout_regularity"
        ]
        self.model = self._train_baseline_model()

    def _train_baseline_model(self) -> lgb.Booster:
        """Trains a baseline LightGBM model on synthetic alternative data."""
        np.random.seed(42)
        X_train = pd.DataFrame(np.random.rand(100, 4), columns=self.feature_names)
        # Target: 0 (Good Standing), 1 (Default Risk)
        y_train = (X_train['utility_payment_consistency'] * 0.5 + X_train['gig_platform_payout_regularity'] * 0.5 < 0.5).astype(int)
        
        train_data = lgb.Dataset(X_train, label=y_train)
        params = {"objective": "binary", "metric": "binary_logloss", "verbosity": -1, "seed": 42}
        return lgb.train(params, train_data, num_boost_round=20)

    def evaluate_applicant(self, applicant_df: pd.DataFrame) -> dict:
        """Calculates probability of default, dynamic credit score, and SHAP factors."""
        pd_proba = float(self.model.predict(applicant_df)[0])
        credit_score = int(850 - (pd_proba * 550)) # Scale 300 - 850

        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(applicant_df)
        
        positive_signals = []
        risk_signals = []

        for idx, val in enumerate(shap_values[0]):
            feature = self.feature_names[idx]
            if val < 0:
                positive_signals.append((feature, round(abs(val), 4)))
            else:
                risk_signals.append((feature, round(val, 4)))

        return {
            "credit_score": credit_score,
            "probability_of_default": round(pd_proba, 4),
            "positive_signals": sorted(positive_signals, key=lambda x: x[1], reverse=True)[:3],
            "risk_signals": sorted(risk_signals, key=lambda x: x[1], reverse=True)[:3]
        }

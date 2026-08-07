import pandas as pd
from pathlib import Path


DATA_PATH = Path("data")


def load_employee_data():

    return pd.read_csv(
        DATA_PATH / "employee_risk_scores.csv"
    )


def load_alert_data():

    return pd.read_csv(
        DATA_PATH / "final_explainable_alerts.csv"
    )


def load_lead_time():

    return pd.read_csv(
        DATA_PATH / "lead_time_results.csv"
    )


def load_risk_distribution():

    return pd.read_csv(
        DATA_PATH / "risk_distribution.csv"
    )
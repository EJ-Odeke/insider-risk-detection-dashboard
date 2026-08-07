

# ============================================================
# INSIDERGUARD AI SECURITY THEME
# ============================================================


RISK_COLORS = {

    "Low": "#27AE60",

    "Medium": "#F1C40F",

    "High": "#E67E22",

    "Critical": "#C0392B"

}



PRIORITY_COLORS = {

    "Low": "#27AE60",

    "Medium": "#F1C40F",

    "High": "#E67E22",

    "Critical": "#C0392B"

}



SEVERITY_COLORS = {

    "Low": "#27AE60",

    "Medium": "#F1C40F",

    "High": "#E67E22",

    "Critical": "#C0392B"

}



def normalize_risk(value):

    """
    Converts different risk names into
    standard SOC categories.
    """

    value = str(value).strip().lower()


    mapping = {


        "low":
        "Low",

        "low risk":
        "Low",


        "medium":
        "Medium",

        "medium risk":
        "Medium",


        "high":
        "High",

        "high risk":
        "High",


        "critical":
        "Critical",

        "critical risk":
        "Critical"

    }


    return mapping.get(

        value,

        "Medium"

    )
# ============================================================
# INSIDERGUARD AI
# Explainable Insider Cyber Risk Early Warning System
# ============================================================


import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
from datetime import datetime



# ============================================================
# PAGE CONFIGURATION
# ============================================================


st.set_page_config(

    page_title="INSIDERGUARD AI",

    page_icon="🛡️",

    layout="wide"

)



# ============================================================
# VISUAL STYLE
# ============================================================


st.markdown(

"""

<style>

body {

background-color:#F4F6F8;

}


[data-testid="stSidebar"] {

background-color:#142B44;

}


[data-testid="stSidebar"] * {

color:white;

}


h1 {

color:#142B44;

}


h2 {

color:#1F4E79;

}


div[data-testid="metric-container"] {

background:white;

padding:15px;

border-radius:10px;

border-left:5px solid #1F77B4;

}


</style>

""",

unsafe_allow_html=True

)



# ============================================================
# DATA LOADING
# ============================================================


DATA_PATH = Path("data")



@st.cache_data

def load_data():


    employees = pd.read_csv(

        DATA_PATH / "employee_risk_scores.csv"

    )


    alerts = pd.read_csv(

        DATA_PATH / "final_explainable_alerts.csv"

    )


    lead_time = pd.read_csv(

        DATA_PATH / "lead_time_results.csv"

    )


    risk_distribution = pd.read_csv(

        DATA_PATH / "risk_distribution.csv"

    )


    return (

        employees,

        alerts,

        lead_time,

        risk_distribution

    )



employees, alerts, lead_time, risk_distribution = load_data()



# ============================================================
# DATA CLEANING
# ============================================================


employees["risk_score"] = pd.to_numeric(

    employees["risk_score"],

    errors="coerce"

)


alerts["Deviation"] = pd.to_numeric(

    alerts["Deviation"],

    errors="coerce"

)


if "SHAP Impact" in alerts.columns:

    alerts["SHAP Impact"] = pd.to_numeric(

        alerts["SHAP Impact"],

        errors="coerce"

    )



# ============================================================
# HEADER
# ============================================================


st.title(

    "INSIDERGUARD AI"

)


st.subheader(

    "Explainable Insider Cyber Risk Early Warning Platform"

)


st.write(

"""

An AI-driven cybersecurity monitoring platform combining:


• User Entity Behaviour Analytics (UEBA)

• Machine Learning Risk Prediction

• Explainable AI (SHAP)

• Behavioural Anomaly Detection


The system provides early warning indicators
to support proactive insider threat investigation.

"""

)



c1,c2,c3 = st.columns(3)



c1.success(

    "Detection Engine Active"

)


c2.info(

    "Random Forest Ensemble"

)


c3.info(

    "SHAP Explainability Enabled"

)



st.divider()



# ============================================================
# SIDEBAR NAVIGATION
# ============================================================


st.sidebar.title(

    "INSIDERGUARD AI"

)


st.sidebar.write(

    "Security Operations Centre"

)



page = st.sidebar.radio(

    "MODULES",

    [

        "Security Command Centre",

        "Threat Monitoring",

        "User Investigation",

        "Explainable AI Reasoning",

        "Behaviour Intelligence",

        "Model Performance",

        "Incident Report"

    ]

)



st.sidebar.divider()



st.sidebar.write(

f"""

SYSTEM STATUS


Users Monitored:

{employees['user'].nunique()}



Active Alerts:

{len(alerts)}



System Time:

{datetime.now().strftime('%Y-%m-%d %H:%M')}

"""

)



# ============================================================
# FUNCTION DEFINITIONS
# (Filled in next parts)
# ============================================================


def security_command_center():

    pass



def threat_monitoring():

    pass



def user_investigation():

    pass



def explainable_ai():

    pass



def behaviour_intelligence():

    pass



def model_performance():

    pass



def incident_report():

    pass

# ============================================================
# SECURITY COMMAND CENTRE FUNCTION
# ============================================================


def security_command_center():


    st.header(

        "Security Command Centre"

    )


    st.write(

    """
    Centralised cybersecurity monitoring dashboard.

    This module provides visibility into:

    • Insider risk exposure

    • Active security alerts

    • High-risk users

    • Organisational threat posture

    """

    )



    total_users = employees["user"].nunique()


    total_alerts = len(alerts)



    high_risk = employees[

        employees["risk_category"]

        .isin(

            [

                "High",

                "Critical"

            ]

        )

    ].shape[0]



    average_risk = employees["risk_score"].mean()



    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "Users Monitored",

        total_users

    )


    c2.metric(

        "Active Alerts",

        total_alerts

    )


    c3.metric(

        "High Risk Users",

        high_risk

    )


    c4.metric(

        "Risk Exposure",

        f"{average_risk:.2%}"

    )



    st.divider()



    col1,col2 = st.columns(2)



    with col1:


        st.subheader(

            "Risk Category Distribution"

        )


        risk = (

            employees["risk_category"]

            .value_counts()

            .reset_index()

        )


        risk.columns = [

            "Risk Category",

            "Users"

        ]



        fig = px.pie(

            risk,

            names="Risk Category",

            values="Users",

            hole=0.45

        )



        st.plotly_chart(

            fig,

            use_container_width=True

        )



    with col2:


        st.subheader(

            "Alert Priority Distribution"

        )



        priority = (

            employees["alert_priority"]

            .value_counts()

            .reset_index()

        )


        priority.columns = [

            "Priority",

            "Count"

        ]



        fig = px.bar(

            priority,

            x="Priority",

            y="Count"

        )



        st.plotly_chart(

            fig,

            use_container_width=True

        )



    st.divider()



    st.subheader(

        "Latest Insider Risk Alerts"

    )


    st.dataframe(

        alerts.head(20),

        use_container_width=True

    )





# ============================================================
# THREAT MONITORING FUNCTION
# ============================================================


def threat_monitoring():


    st.header(

        "Insider Threat Monitoring"

    )


    st.write(

    """
    Continuous monitoring of employee behaviour
    patterns to identify users requiring security
    investigation.

    """

    )



    st.divider()



    risk_categories = st.multiselect(

        "Filter Risk Categories",

        employees["risk_category"].unique(),

        default=employees["risk_category"].unique()

    )



    filtered = employees[

        employees["risk_category"]

        .isin(risk_categories)

    ]



    filtered = filtered.sort_values(

        "risk_score",

        ascending=False

    )



    st.subheader(

        "Security Investigation Queue"

    )



    st.dataframe(

        filtered,

        use_container_width=True,

        height=450

    )



    st.divider()



    st.subheader(

        "Highest Risk Users"

    )



    top_users = filtered.head(10)



    fig = px.bar(

        top_users,

        x="user",

        y="risk_score",

        color="risk_category",

        title="Top Insider Risk Users"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ============================================================
    # USER INVESTIGATION FUNCTION
    # ============================================================

    def user_investigation():

        st.header(

            "User Investigation Workspace"

        )

        st.write(

            """
            Detailed insider risk investigation view.
    
            Analysts can review:
    
            • User risk score
    
            • Risk category
    
            • Behavioural evidence
    
            • Deviations from normal activity
    
            """

        )

        selected_user = st.selectbox(

            "Select User",

            alerts["user"].unique(),

            key="investigation_user"

        )

        profile = employees[

            employees["user"]

            ==

            selected_user

            ]

        evidence = alerts[

            alerts["user"]

            ==

            selected_user

            ]

        if len(profile) > 0:
            user = profile.iloc[0]

            c1, c2, c3 = st.columns(3)

            c1.metric(

                "Risk Score",

                f"{user['risk_score']:.2%}"

            )

            c2.metric(

                "Risk Category",

                user["risk_category"]

            )

            c3.metric(

                "Alert Priority",

                user["alert_priority"]

            )

            st.divider()

            st.subheader(

                "Behavioural Evidence"

            )

            st.dataframe(

                evidence[

                    [

                        "Indicator",

                        "Observed",

                        "Normal Avg",

                        "Deviation"

                    ]

                ],

                use_container_width=True

            )

            fig = px.bar(

                evidence,

                x="Indicator",

                y="Deviation",

                title="Behaviour Deviation Analysis"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

    # ============================================================
    # EXPLAINABLE AI FUNCTION
    # ============================================================

    def explainable_ai():

        st.header(

            "Explainable AI Threat Reasoning"

        )

        st.write(

            """
            SHAP-based explanations show why the machine
            learning model assigned a specific insider risk score.
    
            This improves transparency and supports
            human security decisions.
    
            """

        )

        selected_user = st.selectbox(

            "Select User For AI Explanation",

            alerts["user"].unique(),

            key="shap_user"

        )

        explanation = alerts[

            alerts["user"]

            ==

            selected_user

            ]

        if "SHAP Impact" in explanation.columns:

            explanation = explanation.sort_values(

                "SHAP Impact",

                ascending=False

            )

            fig = px.bar(

                explanation,

                x="SHAP Impact",

                y="Indicator",

                orientation="h",

                title="SHAP Risk Contribution"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

            st.subheader(

                "Prediction Evidence"

            )

            st.dataframe(

                explanation[

                    [

                        "Indicator",

                        "Observed",

                        "Normal Avg",

                        "Deviation",

                        "SHAP Impact"

                    ]

                ],

                use_container_width=True

            )


        else:

            st.warning(

                "SHAP information not available."

            )

    # ============================================================
    # BEHAVIOUR INTELLIGENCE FUNCTION
    # ============================================================

    def behaviour_intelligence():

        st.header(

            "User Entity Behaviour Analytics"

        )

        st.write(

            """
            UEBA identifies suspicious behaviour by
            measuring deviations between observed activity
            and normal user behaviour patterns.
    
            """

        )

        behaviour = (

            alerts.groupby(

                "Indicator"

            )

            .agg(

                {

                    "Deviation": "mean",

                    "user": "count"

                }

            )

            .reset_index()

        )

        behaviour.columns = [

            "Indicator",

            "Average Deviation",

            "Affected Users"

        ]

        behaviour = behaviour.sort_values(

            "Average Deviation",

            ascending=False

        )

        st.subheader(

            "Major Insider Risk Indicators"

        )

        st.dataframe(

            behaviour,

            use_container_width=True

        )

        fig = px.bar(

            behaviour.head(10),

            x="Indicator",

            y="Average Deviation",

            title="Top Behavioural Risk Drivers"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )
# ============================================================
# MODEL PERFORMANCE FUNCTION
# ============================================================


def model_performance():


    st.header(

        "Model Performance Evaluation"

    )


    st.write(

    """
    Cross-validation evaluation of the insider risk
    detection model.

    The evaluation demonstrates model reliability,
    generalisation ability, and detection capability.

    """

    )



    performance = pd.DataFrame(

    {

        "Metric":[

            "Accuracy",

            "Precision",

            "Recall",

            "F1 Score",

            "ROC-AUC"

        ],


        "Mean Score":[

            0.892857,

            0.851695,

            0.957143,

            0.900078,

            0.982653

        ],


        "Standard Deviation":[

            0.039123,

            0.054841,

            0.034993,

            0.033782,

            0.008896

        ]

    }

    )



    performance["Percentage"] = (

        performance["Mean Score"] * 100

    ).round(2)



    st.dataframe(

        performance,

        use_container_width=True

    )



    fig = px.bar(

        performance,

        x="Metric",

        y="Percentage",

        text="Percentage",

        title="Cross Validation Performance"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.divider()



    st.subheader(

        "Early Detection Capability"

    )


    if len(lead_time) > 0:


        st.dataframe(

            lead_time,

            use_container_width=True

        )


    else:


        st.info(

            "Lead-time analysis data unavailable."

        )





# ============================================================
# INCIDENT REPORT FUNCTION
# ============================================================


def incident_report():


    st.header(

        "Insider Cyber Risk Incident Report"

    )



    st.write(

    """
    Automatically generated investigation summary
    for security analysts.

    """

    )



    selected_user = st.selectbox(

        "Generate Report For",

        alerts["user"].unique(),

        key="incident_user"

    )



    user_profile = employees[

        employees["user"]

        ==

        selected_user

    ]



    evidence = alerts[

        alerts["user"]

        ==

        selected_user

    ]



    if len(user_profile) > 0:



        user = user_profile.iloc[0]



        report = f"""

INSIDERGUARD AI

INSIDER CYBER RISK REPORT


CASE ID:

IR-{datetime.now().strftime('%Y%m%d%H%M')}



USER:

{selected_user}



RISK SCORE:

{user['risk_score']:.2%}



RISK CATEGORY:

{user['risk_category']}



ALERT PRIORITY:

{user['alert_priority']}



PRIMARY BEHAVIOURAL INDICATORS:


{evidence[['Indicator','Deviation']].to_string(index=False)}



RECOMMENDATION:


Security analyst investigation recommended.

AI output should support,
not replace, human security decisions.

"""



        st.code(

            report,

            language="text"

        )



        st.download_button(

            "Download Incident Report",

            report,

            file_name="insider_risk_report.txt"

        )





# ============================================================
# APPLICATION ROUTER
# ============================================================


if page == "Security Command Centre":


    security_command_center()



elif page == "Threat Monitoring":


    threat_monitoring()



elif page == "User Investigation":


    user_investigation()



elif page == "Explainable AI Reasoning":


    explainable_ai()



elif page == "Behaviour Intelligence":


    behaviour_intelligence()



elif page == "Model Performance":


    model_performance()



elif page == "Incident Report":


    incident_report()



# ============================================================
# FOOTER
# ============================================================


st.divider()


st.caption(

"""
INSIDERGUARD AI

Explainable Machine Learning Framework
for Early Insider Cyber Risk Detection

"""

)

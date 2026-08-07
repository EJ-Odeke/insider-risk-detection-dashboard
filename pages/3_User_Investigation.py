import streamlit as st
import plotly.express as px
import pandas as pd

from utils.theme import apply_security_theme


apply_security_theme()

from utils.data_loader import (
    load_employee_data,
    load_alert_data
)



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="User Investigation",

    layout="wide"

)



# ============================================================
# LOAD DATA
# ============================================================

employees = load_employee_data()

alerts = load_alert_data()



# ============================================================
# CLEAN DATA
# ============================================================

employees["user"] = (

    employees["user"]

    .astype(str)

)



alerts["user"] = (

    alerts["user"]

    .astype(str)

)



employees["risk_score"] = pd.to_numeric(

    employees["risk_score"],

    errors="coerce"

)



alerts["risk_score"] = pd.to_numeric(

    alerts["risk_score"],

    errors="coerce"

)



# ============================================================
# HEADER


st.title(

    "Insider Risk Investigation"

)


st.caption(

    "Individual User Behaviour Analysis | Risk Drivers | Explainable AI Evidence"

)



# ============================================================
# USER SELECTION
# ============================================================

available_users = sorted(

    set(alerts["user"].dropna())

    |

    set(employees["user"].dropna())

)



selected_user = st.selectbox(

    "Select User",

    available_users

)



# ============================================================
# USER PROFILE
# ============================================================

user_alerts = alerts[

    alerts["user"]

    ==

    selected_user

]



user_profile = employees[

    employees["user"]

    ==

    selected_user

]



# Alert dataset contains investigation evidence

if not user_alerts.empty:

    profile = user_alerts.iloc[0]


elif not user_profile.empty:

    profile = user_profile.iloc[0]


else:

    profile = None



if profile is not None:


    risk_score = profile.get(

        "risk_score",

        0

    )


    category = profile.get(

        "risk_category",

        "Unknown"

    )


    priority = profile.get(

        "alert_priority",

        "Unknown"

    )


else:


    risk_score = 0

    category = "Unknown"

    priority = "Unknown"



# ============================================================
# RISK SUMMARY
# ============================================================

c1, c2, c3, c4 = st.columns(4)



c1.metric(

    "Risk Score",

    f"{risk_score:.1%}"

)



c2.metric(

    "Risk Category",

    category

)



c3.metric(

    "Alert Priority",

    priority

)



c4.metric(

    "Risk Signals",

    len(user_alerts)

)



st.divider()



# ============================================================
# BEHAVIOURAL EVIDENCE
# ============================================================

st.subheader(

    "Behavioural Evidence"

)



if not user_alerts.empty:


    evidence_columns = [

        "Indicator",

        "Observed",

        "Normal Avg",

        "Deviation",

        "SHAP Impact"

    ]



    available_columns = [

        col

        for col in evidence_columns

        if col in user_alerts.columns

    ]



    evidence = user_alerts[

        available_columns

    ]



    st.dataframe(

        evidence,

        use_container_width=True,

        hide_index=True

    )


else:


    st.warning(

        "No behavioural evidence found."

    )



# ============================================================
# BEHAVIOUR DEVIATION ANALYSIS
# ============================================================

if not user_alerts.empty:


    st.divider()


    st.subheader(

        "Behaviour Deviation Analysis"

    )



    deviation_data = user_alerts[

        [

            "Indicator",

            "Deviation"

        ]

    ].copy()



    # Convert -90.7% into -90.7

    deviation_data["Deviation"] = (

        deviation_data["Deviation"]

        .astype(str)

        .str.replace("%", "", regex=False)

        .astype(float)

    )



    deviation_data["Deviation Status"] = deviation_data["Deviation"].apply(

        lambda x:

        "Negative Deviation"

        if x < 0

        else

        "Positive Deviation"

    )



    color_map = {

        "Negative Deviation": "#C0392B",

        "Positive Deviation": "#8B4513"

    }



    fig = px.bar(

        deviation_data,

        x="Indicator",

        y="Deviation",

        color="Deviation Status",

        color_discrete_map=color_map,

        text="Deviation"

    )



    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside"

    )



    fig.update_layout(

        height=500,

        xaxis_title="Behaviour Indicator",

        yaxis_title="Deviation (%)",

        xaxis_tickangle=-45,

        legend_title="Deviation Type",

        margin=dict(

            l=40,

            r=40,

            t=60,

            b=140

        )

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ============================================================
# CASE ASSESSMENT
# ============================================================

st.divider()



st.subheader(

    "Case Assessment"

)



if risk_score >= 0.75:


    st.error(

        "CRITICAL RISK — Immediate analyst review recommended"

    )



elif risk_score >= 0.50:


    st.warning(

        "ELEVATED RISK — Additional monitoring recommended"

    )



else:


    st.info(

        "LOW RISK — Continue routine monitoring"

    )
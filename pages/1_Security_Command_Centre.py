from utils.theme import apply_security_theme


apply_security_theme()

import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_loader import (
    load_employee_data,
    load_alert_data
)





st.set_page_config(

    page_title="Security Command Centre",

    layout="wide"

)





st.markdown(

    """

    <style>

    .block-container {

        padding-top: 0.8rem;

        padding-bottom: 0.5rem;

    }


    h1 {

        font-size: 30px;

    }


    h2 {

        font-size: 20px;

    }


    div[data-testid="metric-container"] {

        padding: 5px;

    }


    </style>

    """,

    unsafe_allow_html=True

)





SECURITY_COLORS = {

    "Low": "#27AE60",

    "Medium": "#F1C40F",

    "High": "#E67E22",

    "Critical": "#C0392B"

}


RISK_ORDER = [

    "Low",

    "Medium",

    "High",

    "Critical"

]




employees = load_employee_data()

alerts = load_alert_data()




# risk engin

employees["risk_score"] = pd.to_numeric(

    employees["risk_score"],

    errors="coerce"

)



def assign_risk(score):

    if score >= 0.90:

        return "Critical"

    elif score >= 0.70:

        return "High"

    elif score >= 0.40:

        return "Medium"

    else:

        return "Low"



employees["dashboard_risk"] = (

    employees["risk_score"]

    .apply(assign_risk)

)



if "severity" in alerts.columns:

    alerts["severity"] = (

        alerts["severity"]

        .astype(str)

        .str.strip()

        .str.title()

    )



if "alert_priority" in alerts.columns:

    alerts["alert_priority"] = (

        alerts["alert_priority"]

        .astype(str)

        .str.strip()

        .str.title()

    )



#header

st.title(
    "Insider Cyber Risk Prediction & Intelligence Centre"
)


st.caption(
    "Responsible Explainable Ensemble Learning Framework | Behavioural Analytics | Early Threat Detection"
)




total_users = employees["user"].nunique()


total_alerts = len(alerts)



high_risk_users = employees[

    employees["dashboard_risk"]

    .isin(

        [

            "High",

            "Critical"

        ]

    )

].shape[0]



critical_users = employees[

    employees["dashboard_risk"]

    ==

    "Critical"

].shape[0]



risk_exposure = employees["risk_score"].mean()



a,b,c,d,e = st.columns(5)



a.metric(

    "Users",

    f"{total_users:,}"

)


b.metric(

    "Alerts",

    f"{total_alerts:,}"

)


c.metric(

    "High Risk",

    f"{high_risk_users:,}"

)


d.metric(

    "Critical",

    f"{critical_users:,}"

)


e.metric(

    "Exposure",

    f"{risk_exposure:.1%}"

)




if critical_users > 0:

    st.error(

        f"CRITICAL STATE — {critical_users} users require action"

    )


elif high_risk_users > 0:

    st.warning(

        f"HIGH RISK STATE — {high_risk_users} users require review"

    )


else:

    st.success(

        "SECURITY STATE NORMAL"

    )




left,right = st.columns(2)



# -------------------------------
# RISK DISTRIBUTION

with left:


    st.subheader(

        "Risk Distribution"

    )


    risk = (

        employees["dashboard_risk"]

        .value_counts()

        .reindex(

            RISK_ORDER,

            fill_value=0

        )

        .reset_index()

    )


    risk.columns = [

        "Risk",

        "Users"

    ]



    fig = px.pie(

        risk,

        names="Risk",

        values="Users",

        hole=0.55,

        color="Risk",

        color_discrete_map=SECURITY_COLORS

    )


    fig.update_layout(

        height=280,

        margin=dict(

            l=10,

            r=10,

            t=30,

            b=10

        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# -------------------------------
# THREAt

with right:


    st.subheader(

        "Threat Severity"

    )


    if "severity" in alerts.columns:


        severity = (

            alerts["severity"]

            .value_counts()

            .reindex(

                RISK_ORDER,

                fill_value=0

            )

            .reset_index()

        )


        severity.columns = [

            "Severity",

            "Alerts"

        ]



        fig = px.bar(

            severity,

            x="Severity",

            y="Alerts",

            text="Alerts",

            color="Severity",

            color_discrete_map=SECURITY_COLORS

        )


        fig.update_layout(

            height=280,

            margin=dict(

                l=10,

                r=10,

                t=30,

                b=10

            )

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )





st.subheader(

    "Priority Investigation Queue"

)



investigation = (

    employees

    .sort_values(

        "risk_score",

        ascending=False

    )

    [

        [

            "user",

            "risk_score",

            "dashboard_risk"

        ]

    ]

    .head(8)

)



st.dataframe(

    investigation,

    use_container_width=True,

    hide_index=True,

    height=260

)





st.subheader(

    "Latest Alerts"

)



alert_columns = [

    "user",

    "severity",

    "alert_priority",

    "Indicator",

    "Deviation"

]



available = [

    c for c in alert_columns

    if c in alerts.columns

]



st.dataframe(

    alerts

    .sort_values(

        "risk_score",

        ascending=False

    )

    [

        available

    ]

    .head(8),

    use_container_width=True,

    hide_index=True,

    height=260

)

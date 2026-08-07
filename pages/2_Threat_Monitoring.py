import streamlit as st
import pandas as pd
import plotly.express as px
from utils.theme import apply_security_theme


apply_security_theme()

from utils.data_loader import (
    load_employee_data,
    load_alert_data
)




st.set_page_config(

    page_title="Threat Monitoring Centre",

    layout="wide"

)




RISK_COLORS = {

    "Low": "#27AE60",

    "Medium": "#F1C40F",

    "High": "#E67E22",

    "Critical": "#C0392B"

}




employees = load_employee_data()

alerts = load_alert_data()





employees["risk_score"] = pd.to_numeric(

    employees["risk_score"],

    errors="coerce"

)


alerts["risk_score"] = pd.to_numeric(

    alerts["risk_score"],

    errors="coerce"

)




st.title(
    "Insider Risk Monitoring Centre"
)

st.caption(
    "Behavioural Analytics | Early Risk Detection | Threat Investigation"
)



active_cases = alerts["user"].nunique()


detected_anomalies = alerts["Indicator"].nunique()


high_risk_users = employees[

    employees["risk_score"] >= 0.70

]["user"].nunique()


risk_exposure = employees["risk_score"].mean()



c1, c2, c3, c4 = st.columns(4)



c1.metric(

    "Active Threat Cases",

    f"{active_cases:,}"

)



c2.metric(

    "Detected Anomalies",

    f"{detected_anomalies:,}"

)



c3.metric(

    "High-Risk Users",

    f"{high_risk_users:,}"

)



c4.metric(

    "Risk Exposure",

    f"{risk_exposure:.1%}"

)



st.divider()





left, right = st.columns(

    [1.4, 1]

)



with left:


    st.subheader(

        "Behavioural Anomaly Patterns — Threat Drivers"

    )


    indicators = (

        alerts["Indicator"]

        .value_counts()

        .reset_index()

    )


    indicators.columns = [

        "Indicator",

        "Count"

    ]



    fig = px.bar(

        indicators,

        x="Count",

        y="Indicator",

        orientation="h",

        text="Count",

        color="Count",

        color_continuous_scale=[

            "#F1C40F",

            "#C0392B"

        ]

    )


    fig.update_traces(

        textposition="outside"

    )


    fig.update_layout(

        height=520,

        margin=dict(

            l=30,

            r=30,

            t=60,

            b=30

        ),

        font=dict(

            size=14

        ),

        xaxis_title="Detected Events",

        yaxis_title="Behaviour Signal"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




with right:


    st.subheader(

        "Top Escalating Users"

    )


    escalation_columns = [

        "user",

        "risk_score",

        "Indicator"

    ]


    available = [

        c for c in escalation_columns

        if c in alerts.columns

    ]



    escalation = (

        alerts

        .sort_values(

            "risk_score",

            ascending=False

        )

        [

            available

        ]

        .head(10)

    )



    st.dataframe(

        escalation,

        use_container_width=True,

        hide_index=True,

        height=420

    )





st.divider()



st.subheader(

    "Active Threat Investigation Feed"

)



feed_columns = [

    "user",

    "risk_category",

    "risk_score",

    "Indicator",

    "Deviation",

    "SHAP Impact"

]



available_columns = [

    c for c in feed_columns

    if c in alerts.columns

]



feed = (

    alerts

    .sort_values(

        "risk_score",

        ascending=False

    )

    [

        available_columns

    ]

    .head(15)

)



st.dataframe(

    feed,

    use_container_width=True,

    hide_index=True,

    height=350

)




st.divider()



st.subheader(

    "Recent Threat Signals"

)



signals_columns = [

    "user",

    "Indicator",

    "risk_score"

]



available_signals = [

    c for c in signals_columns

    if c in alerts.columns

]



signals = (

    alerts

    .sort_values(

        "risk_score",

        ascending=False

    )

    [

        available_signals

    ]

    .head(10)

)



st.dataframe(

    signals,

    use_container_width=True,

    hide_index=True,

    height=250

)

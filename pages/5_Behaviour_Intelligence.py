import streamlit as st
import pandas as pd
import plotly.express as px
from utils.theme import apply_security_theme


apply_security_theme()

from utils.data_loader import load_alert_data



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Behaviour Intelligence Centre",

    layout="wide"

)



# ============================================================
# LOAD DATA
# ============================================================

alerts = load_alert_data()



# ============================================================
# HEADER
# ============================================================

st.title(

    "Behaviour Intelligence Centre"

)


st.caption(

    "User Behaviour Analytics | Anomaly Detection | Insider Risk Signals"

)



# ============================================================
# VALIDATION
# ============================================================

if alerts.empty:

    st.error(

        "No behavioural data available."

    )

    st.stop()



# ============================================================
# DATA CLEANING
# ============================================================

alerts["user"] = alerts["user"].astype(str)



# Convert deviation percentage

if "Deviation" in alerts.columns:


    alerts["Deviation"] = (

        alerts["Deviation"]

        .astype(str)

        .str.replace("%","",regex=False)

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



alerts = alerts.dropna(

    subset=["Deviation"]

)



# ============================================================
# KPI SUMMARY
# ============================================================

c1,c2,c3,c4 = st.columns(4)



c1.metric(

    "Behaviour Indicators",

    alerts["Indicator"].nunique()

)



c2.metric(

    "Users Analysed",

    alerts["user"].nunique()

)



c3.metric(

    "Highest Deviation",

    f"{alerts['Deviation'].min():.1f}%"

)



if "SHAP Impact" in alerts.columns:


    c4.metric(

        "Average AI Impact",

        f"{alerts['SHAP Impact'].mean():.3f}"

    )


else:


    c4.metric(

        "AI Impact",

        "N/A"

    )



st.divider()



# ============================================================
# BEHAVIOURAL ANOMALY PATTERNS
# ============================================================

st.subheader(

    "Behavioural Anomaly Patterns"

)



behaviour_summary = (

    alerts

    .groupby("Indicator")

    .agg(

        Users=("user","nunique"),

        Average_Deviation=("Deviation","mean"),

        Average_SHAP=("SHAP Impact","mean")

    )

    .reset_index()

)



behaviour_summary = behaviour_summary.sort_values(

    "Average_Deviation"

)



top_patterns = behaviour_summary.head(10)



fig = px.bar(

    top_patterns,

    x="Average_Deviation",

    y="Indicator",

    orientation="h",

    color="Average_Deviation",

    color_continuous_scale=[

        "#C0392B",

        "#8B4513"

    ],

    text="Average_Deviation"

)



fig.update_traces(

    texttemplate="%{text:.1f}%",

    textposition="outside"

)



fig.update_layout(

    height=500,

    xaxis_title="Deviation From Normal (%)",

    yaxis_title="Behaviour Indicator"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# HIGH RISK USERS
# ============================================================

st.divider()



st.subheader(

    "Users With Highest Behavioural Deviation"

)



user_behaviour = (

    alerts

    .groupby("user")

    .agg(

        Risk_Signals=("Indicator","count"),

        Average_Deviation=("Deviation","mean"),

        Average_AI_Impact=("SHAP Impact","mean")

    )

    .reset_index()

)



user_behaviour = user_behaviour.sort_values(

    "Average_Deviation"

)



st.dataframe(

    user_behaviour.head(15),

    use_container_width=True,

    hide_index=True

)



# ============================================================
# SECURITY INSIGHT
# ============================================================

st.info(

"""

UEBA Insight:

The system highlights users whose behaviour differs from
normal activity patterns.

Priority attention should be given to:

• High deviation behaviour

• Multiple risk indicators

• Strong AI risk contribution

"""

)
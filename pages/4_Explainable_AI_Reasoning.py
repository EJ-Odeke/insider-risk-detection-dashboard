import streamlit as st
import plotly.express as px
import pandas as pd
from utils.theme import apply_security_theme


apply_security_theme()

from utils.data_loader import load_alert_data




st.set_page_config(

    page_title="AI Risk Explanation Centre",

    layout="wide"

)




alerts = load_alert_data()




alerts["user"] = alerts["user"].astype(str)



alerts["SHAP Impact"] = pd.to_numeric(

    alerts["SHAP Impact"],

    errors="coerce"

)



alerts = alerts.dropna(

    subset=["SHAP Impact"]

)





st.title(

    "AI Risk Explanation Centre"

)



st.caption(

    "SHAP-Based Behavioural Risk Drivers | Model Transparency | AI Decision Support"

)




if alerts.empty:

    st.error(

        "No AI explanation data available."

    )

    st.stop()



if "SHAP Impact" not in alerts.columns:

    st.error(

        "SHAP Impact column missing."

    )

    st.stop()




users = sorted(

    alerts["user"]

    .dropna()

    .unique()

)



users.insert(

    0,

    "All Users"

)



selected_user = st.selectbox(

    "Select User",

    users

)





if selected_user == "All Users":


    user_explanation = alerts.copy()


    mode = "Global AI Risk Explanation"



else:


    user_explanation = alerts[

        alerts["user"]

        ==

        selected_user

    ]


    mode = "Individual User Explanation"



user_explanation = user_explanation.sort_values(

    "SHAP Impact",

    ascending=False

)




top_factor = user_explanation.iloc[0]



# Short version for KPI display

main_factor = str(

    top_factor["Indicator"]

)



if len(main_factor) > 25:

    main_factor = main_factor[:25] + "..."



c1, c2, c3 = st.columns(3)



c1.metric(

    "Risk Drivers",

    len(user_explanation)

)



c2.metric(

    "Main Risk Factor",

    main_factor

)



c3.metric(

    "Maximum SHAP Impact",

    f"{top_factor['SHAP Impact']:.3f}"

)



st.caption(mode)



st.divider()




st.subheader(

    "AI Risk Contribution Analysis"

)



shap_plot = user_explanation.head(15)



fig = px.bar(

    shap_plot,

    x="SHAP Impact",

    y="Indicator",

    orientation="h",

    text="SHAP Impact",

    color="SHAP Impact",

    color_continuous_scale=[

        "#8B4513",

        "#C0392B"

    ]

)



fig.update_traces(

    texttemplate="%{text:.3f}",

    textposition="outside"

)



fig.update_layout(

    height=500,

    yaxis={

        "categoryorder": "total ascending"

    },

    xaxis_title="Contribution to Risk Prediction",

    yaxis_title="Behaviour Indicator",

    margin=dict(

        l=40,

        r=40,

        t=50,

        b=40

    )

)



st.plotly_chart(

    fig,

    use_container_width=True

)




st.divider()



st.subheader(

    "Explainable Evidence"

)



columns = [

    "user",

    "Indicator",

    "Observed",

    "Normal Avg",

    "Deviation",

    "SHAP Impact"

]



available_columns = [

    col

    for col in columns

    if col in user_explanation.columns

]



st.dataframe(

    user_explanation[available_columns],

    use_container_width=True,

    hide_index=True

)




st.divider()



st.subheader(

    "AI Interpretation"

)



highest = user_explanation.iloc[0]



if selected_user == "All Users":


    st.info(

        f"""

The strongest behavioural driver across monitored users is:

**{highest['Indicator']}**

This factor has the highest influence on overall insider risk prediction.

SHAP values explain how behavioural factors contribute to the AI decision.

"""

    )


else:


    st.warning(

        f"""

The strongest contributor to this user's risk score was:

**{highest['Indicator']}**

Observed:

{highest['Observed']}

Normal baseline:

{highest['Normal Avg']}

Deviation:

{highest['Deviation']}

Analysts should validate this behaviour using organisational context.

"""

    )



st.info(

    """

SHAP explains feature contribution to the AI prediction.

It supports security decisions but does not confirm malicious intent.

Human investigation remains essential.

"""

)

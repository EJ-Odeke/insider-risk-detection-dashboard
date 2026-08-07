import streamlit as st


def apply_security_theme():

    st.markdown(

    """

    <style>


    /* =====================================================
       GLOBAL APPLICATION
    ====================================================== */

    .stApp {

        background-color: #E8EDF2;

        color: #1E293B;

    }



    /* =====================================================
       HEADINGS
    ====================================================== */

    h1 {

        color: #0F172A;

        font-weight: 800;

        letter-spacing: -0.5px;

    }



    h2, h3 {

        color: #12355B;

        font-weight: 700;

    }



    /* =====================================================
       BODY TEXT
    ====================================================== */

    p, label {

        color: #334155;

    }



    /* =====================================================
       METRIC CARDS
    ====================================================== */

    [data-testid="metric-container"] {


        background-color: #FFFFFF;


        border-radius: 12px;


        padding: 15px;


        border: 1px solid #CBD5E1;


        border-left: 5px solid #ACBAC4;


        box-shadow:

        0px 3px 8px rgba(15,23,42,0.08);


    }



    [data-testid="stMetricValue"] {


        color: #0F172A;


        font-size: 28px;


        font-weight: 800;


    }



    [data-testid="stMetricLabel"] {


        color: #475569;


        font-weight: 600;


    }



    /* =====================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {


        background-color: #ACBAC4;


        border-right:

        1px solid #94A3B8;


    }



    section[data-testid="stSidebar"] p,

    section[data-testid="stSidebar"] label {


        color: #0F172A;


    }



    /* =====================================================
       DATA TABLES
    ====================================================== */

    .stDataFrame {


        background-color: #FFFFFF;


        border-radius: 12px;


        border: 1px solid #CBD5E1;


    }



    /* =====================================================
       BUTTONS
    ====================================================== */

    .stButton button {


        background-color: #2563EB;


        color: white;


        border-radius: 8px;


        border: none;


        font-weight: 600;


    }



    .stButton button:hover {


        background-color: #1D4ED8;


        color: white;


    }



    /* =====================================================
       SELECT BOX
    ====================================================== */

    div[data-baseweb="select"] > div {


        background-color: white;


        border-radius: 8px;


        border: 1px solid #CBD5E1;


    }



    /* =====================================================
       ALERT BOXES
    ====================================================== */

    .stAlert {


        border-radius: 10px;


    }



    /* =====================================================
       DIVIDERS
    ====================================================== */

    hr {


        border-color: #94A3B8;


    }



    </style>

    """,

    unsafe_allow_html=True

    )
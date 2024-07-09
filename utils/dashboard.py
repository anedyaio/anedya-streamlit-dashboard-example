# utils/dashboard.py
import streamlit as st

import streamlit_shadcn_ui as ui

from utils.pageconfig import V_SPACE
from utils.grid import singlegrid, multigrid
from utils import charts
from utils.charts import humidityData

def drawDashboard():
    headercols = st.columns([0.8,0.2], gap="small",vertical_alignment="center")
    with headercols[0]:
        st.title("Anedya Dashboard", anchor=False)
    with headercols[1]:
        V_SPACE(1)
        refreshcols = st.columns([0.42,0.42,0.16], gap="small",vertical_alignment="center")
        with refreshcols[0]:
            refresh=st.button("Refresh",)
        with refreshcols[1]:
            logout = st.button("Logout")

    if refresh:
        for key in st.session_state.keys():
            if key not in ["LoggedIn"]:
                del st.session_state[key]
    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    st.markdown("This dashboard provides live view of the Anedya's Office. Also allowing you to control the IoT systems remotely!")
    
    gridcols=st.columns([0.8,0.2],gap="small")
    with gridcols[0]:
        st.subheader(body="Current Status", anchor=False)
    # with gridcols[1]:
    #     st.markdown(
    #         """
    #         <head>
    #         <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.4.2/uicons-regular-rounded/css/uicons-regular-rounded.css'>
    #         </head>
    #         <body>
    #         <i class="fi fi-rr-square"></i>
    #         </body>
    #         """,unsafe_allow_html=True
    #     )
    # with gridcols[2]:
    #     st.markdown(
    #         """
    #         <head>
    #         <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.4.2/uicons-regular-straight/css/uicons-regular-straight.css'>
    #         </head>
    #         <body>
    #         <i class="fi fi-rs-apps-add"></i>
    #         </body>
    #         """,unsafe_allow_html=True
    #     )

    with gridcols[1]:
        # tabgrid=st.columns([1,0.5,1],gap="small")
        # with tabgrid[2]:
        tabs=ui.tabs(options=["Single Grid","Multi Grid"], default_value="Single Grid", key="kanaries")
        

    if tabs == "Single Grid":
        singlegrid()
        # tabs = "Multi Grid"
        # st.session_state.tab = "Multi Grid"

    else:
        multigrid()
        # tabs = "Single Grid"
        # st.session_state.tab = "Single Grid"

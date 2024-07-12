# utils/dashboard.py
import streamlit as st

import streamlit_shadcn_ui as ui

from utils.pageconfig import V_SPACE
from utils.grid import singlegrid, multigrid

def refresh():
    for key in st.session_state.keys():
            if key not in ["LoggedIn"]:
                del st.session_state[key]

def logout():
    st.session_state.LoggedIn = False
    st.rerun()

def drawDashboard():
    headercols = st.columns([0.8,0.2], gap="small",vertical_alignment="center")
    with headercols[0]:
        st.title("Anedya Dashboard", anchor=False)
    with headercols[1]:
        V_SPACE(1)
        refreshcols = st.columns([0.42,0.42,0.16], gap="small",vertical_alignment="center")
        with refreshcols[0]:
            st.button("Refresh",on_click=refresh)
        with refreshcols[1]:
            st.button("Logout",on_click=logout)

    st.markdown("This dashboard provides live view of the Anedya's Office. Also allowing you to control the IoT systems remotely!")
    
    gridcols=st.columns([0.8,0.2],gap="small")
    with gridcols[0]:
        st.subheader(body="Current Status", anchor=False)

    with gridcols[1]:
        tabs=ui.tabs(options=["Single Grid","Multi Grid"], default_value="Single Grid", key="kanaries")

    if tabs == "Single Grid":
        singlegrid()

    else:
        multigrid()

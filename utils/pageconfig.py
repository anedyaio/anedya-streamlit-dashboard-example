# utils/pageconfig.py
import streamlit as st
from streamlit_autorefresh import st_autorefresh

def page_config():
    st.set_page_config(page_title="Anedya IoT Dashboard",page_icon="🌤️", layout="wide")
    st_autorefresh(interval=30000, limit=None, key="auto-refresh-handler")

    #Hide Deploy button and three dots
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton{visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")

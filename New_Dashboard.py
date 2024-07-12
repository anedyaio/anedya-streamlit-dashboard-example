import streamlit as st

from utils.pageconfig import page_config
from utils.anedya import anedya_config, fetchHumidityData, fetchTemperatureData, GetFanStatus, GetHumidifierStatus
from utils.global_vars import nodeId, apiKey
from utils.action_buttons import ButtonText, State, CurrentData
from utils.login import drawLogin
from utils.dashboard import drawDashboard


page_config()

def main():
    global nodeId, apiKey
    anedya_config(NODE_ID=nodeId,API_KEY=apiKey)

    if"LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    ButtonText()
    State()
    CurrentData()

    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        fetchHumidityData()
        fetchTemperatureData()

        GetFanStatus()
        GetHumidifierStatus()

        drawDashboard()

if __name__ == "__main__":
    main()
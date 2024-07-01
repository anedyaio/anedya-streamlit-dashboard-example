# The Anedya IoT cloud enables users to monitor and control IoT devices remotely. The dashboard displays real-time data on humidity and temperature, as well as providing control buttons to operate a fan and a light. 
# The control buttons sync with real-time changes, reflecting the current state of the devices.

import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

from utils.anedya import anedya_config
from utils.anedya import anedya_sendCommand
from utils.anedya import anedya_getValue
from utils.anedya import anedya_setValue
from utils.anedya import fetch_room_temp
from utils.anedya import fetch_coil_temp

# nodeId = "20deeee8-f8ae-11ee-9dd8-c3aa61afe2fb"  # get it from anedya dashboard -> project -> node 
nodeId = "e8e528ac-3545-11ef-9ecc-a1461caa74a3"  # get it from anedya dashboard -> project -> node 
apiKey = "ae0651239c4beffc68e3ccf1829b55e98068f57af598e2af9151aaa53f5e5898"  # aneyda project apikey

st.set_page_config(page_title="Project: Glacier", layout="wide")

#uncomment to show count
# count = st_autorefresh(interval=30000, limit=None, key="auto-refresh-handler")
st_autorefresh(interval=30000, limit=None, key="auto-refresh-handler")

# --------------- HELPER FUNCTIONS -----------------------
def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")


room_temp = pd.DataFrame()
coil_temp = pd.DataFrame()


def main():
    global room_temp, coil_temp
    anedya_config(NODE_ID=nodeId, API_KEY=apiKey)

    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    if "current_room_temp" not in st.session_state:
        st.session_state.current_room_temp = 0

    if "current_coil_temp" not in st.session_state:
        st.session_state.current_coil_temp = 0

    if "set_room_temp" not in st.session_state:
        st.session_state.set_room_temp = "0"

    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        room_temp = fetch_room_temp()
        coil_temp = fetch_coil_temp()
        drawDashboard()


def drawLogin():
    cols = st.columns([1, 0.8, 1], gap='small')
    with cols[0]:
        pass
    with cols[1]:
        st.title("Project: Glacier", anchor=False)
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")
        submit_button = st.button(label="Submit")

        if submit_button:
            if username_inp == "admin" and password_inp == "admin":
                st.session_state.LoggedIn = True
                st.rerun()
            else:
                st.error("Invalid Credential!")
    with cols[2]:
        print()


def drawDashboard():
    headercols = st.columns([1, 0.1, 0.1], gap="small")
    with headercols[0]:
        st.title("Project: Glacier", anchor=False)
    with headercols[1]:
        st.button("Refresh")

    with headercols[2]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    # st.markdown("Dashboard to control the Meter")

    st.subheader(body="Current Status", anchor=False)
    cols = st.columns(2, gap="medium")
    with cols[0]:
        st.metric(label="Room Temperature", value=str(st.session_state.current_room_temp) + " %")
    with cols[1]:
        st.metric(label="Coil Temperature", value=str(st.session_state.current_coil_temp) + "  °C")
    # with cols[2]:
    #    st.metric(label="Refresh Count", value=count)
    st.subheader(body="Set Parameters", anchor=False)
    buttons = st.columns([0.3,0.3,1], gap="small")
    with buttons[0]:
        # st.text("Room temp set pint:")
        room_temp_input=st.text_input("Room Temperature",placeholder=st.session_state.set_room_temp)
        # make thrre columns
        cols2 = st.columns([0.3,0.3,0.4], gap="small")
        with cols2[0]:
            pass
        with cols2[1]:
            pass
        with cols2[2]:
            submit_button = st.button(label=" Set Data ")
            if submit_button:
                if room_temp_input !="":
                    st.session_state.set_room_temp = str(room_temp_input)
                    anedya_sendCommand("set_room_temp", room_temp_input)
                    room_temp_input=""
                    st.rerun()

    with buttons[1]:
        pass
    with buttons[2]:
        pass

    charts = st.columns(2, gap="small")
    with charts[0]:
        st.subheader(body="Room Temperature", anchor=False)
        if room_temp.empty:
            st.write("No Data !!")
        else:
            room_temp_chart_an = alt.Chart(data=room_temp).mark_area(
                line={'color': '#1fa2ff'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#1fa2ff', offset=1),
                        alt.GradientStop(color='rgba(255,255,255,0)', offset=0)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0,
                ),
                interpolate='monotone',
                cursor='crosshair'
            ).encode(
                x=alt.X(
                    shorthand="Datetime:T",
                    axis=alt.Axis(format="%Y-%m-%d %H:%M:%S", title="Datetime", tickCount=10, grid=True, tickMinStep=5),
                ),  # T indicates temporal (time-based) data
                y=alt.Y(
                    "aggregate:Q",
                    scale=alt.Scale(domain=[0, 45]),
                    axis=alt.Axis(title="temeperature (°C)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                        alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            # Display the Altair chart using Streamlit
            st.altair_chart(room_temp_chart_an, use_container_width=True)

    with charts[1]:
        st.subheader(body="Coil Temperature", anchor=False)
        if coil_temp.empty:
            st.write("No Data !!")
        else:
            coil_temp_chart_an = alt.Chart(data=coil_temp).mark_area(
                line={'color': '#1fa2ff'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#1fa2ff', offset=1),
                        alt.GradientStop(color='rgba(255,255,255,0)', offset=0)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0,
                ),
                interpolate='monotone',
                cursor='crosshair'
            ).encode(
                x=alt.X(
                    shorthand="Datetime:T",
                    axis=alt.Axis(format="%Y-%m-%d %H:%M:%S", title="Datetime", tickCount=10, grid=True, tickMinStep=5),
                ),  # T indicates temporal (time-based) data
                y=alt.Y(
                    "aggregate:Q",
                    # scale=alt.Scale(domain=[0, 100]),
                    scale=alt.Scale(zero=False, domain=[0, 100]),
                    axis=alt.Axis(title="Temperature (°C)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                        alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            st.altair_chart(coil_temp_chart_an, use_container_width=True)







if __name__ == "__main__":
    main()

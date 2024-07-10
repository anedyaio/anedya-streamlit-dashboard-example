import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

from utils.anedya import anedya_config
from utils.anedya import anedya_sendCommand
from utils.anedya import anedya_getValue
from utils.anedya import anedya_setValue
from utils.anedya import fetchHumidityData
from utils.anedya import fetchTemperatureData

nodeId = "NODE-ID"  # get it from anedya dashboard -> project -> node 
apiKey = "YOUR-API-KEY"  # aneyda project apikey

st.set_page_config(page_title="Anedya IoT Dashboard", layout="wide")


st_autorefresh(interval=10000, limit=None, key="auto-refresh-handler")

# --------------- HELPER FUNCTIONS -----------------------


def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")


humidityData = pd.DataFrame()
temperatureData = pd.DataFrame()


def main():

    anedya_config(nodeId, apiKey)
    global humidityData, temperatureData

    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    if "FanButtonText" not in st.session_state:
        st.session_state.FanButtonText = "Turn Fan On!"

    if "LightButtonText" not in st.session_state:
        st.session_state.LightButtonText = "Turn Light On!"

    if "LightState" not in st.session_state:
        st.session_state.LightState = False

    if "FanState" not in st.session_state:
        st.session_state.FanState = False

    if "CurrentHumidity" not in st.session_state:
        st.session_state.CurrentHumidity = 0

    if "CurrentTemperature" not in st.session_state:
        st.session_state.CurrentTemperature = 0

    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        humidityData = fetchHumidityData()
        temperatureData = fetchTemperatureData()

        GetFanStatus()
        GetLightStatus()

        drawDashboard()


def drawLogin():
    cols = st.columns([1, 0.8, 1], gap='small')
    with cols[0]:
        pass
    with cols[1]:
        st.title("Anedya Demo Dashboard", anchor=False)
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
        st.title("Anedya Demo Dashboard", anchor=False)
    with headercols[1]:
        st.button("Refresh")
    with headercols[2]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    st.markdown("This dashboard provides live view of the Anedya's Office. Also allowing you to control the Light and Fan remotely!")

    st.subheader(body="Current Status", anchor=False)
    cols = st.columns(2, gap="medium")
    with cols[0]:
        st.metric(label="Humidity", value=str(st.session_state.CurrentHumidity) + " %")
    with cols[1]:
        st.metric(label="Temperature", value=str(st.session_state.CurrentTemperature) + "  °C")
    # with cols[2]:
    #    st.metric(label="Refresh Count", value=count)

    buttons = st.columns(2, gap="small")
    with buttons[0]:
        st.text("Control Fan:")
        st.button(label=st.session_state.FanButtonText, on_click=operateFan)
    with buttons[1]:
        st.text("Control Light:")
        st.button(label=st.session_state.LightButtonText, on_click=operateLight)

    charts = st.columns(2, gap="small")
    with charts[0]:
        st.subheader(body="Humidity ", anchor=False)
        if humidityData.empty:
            st.write("No Data Available!")
        else:
            humidity_chart_an = alt.Chart(data=humidityData).mark_area(
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
                    scale=alt.Scale(domain=[20, 60]),
                    axis=alt.Axis(title="Humidity (%)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                        alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            # Display the Altair chart using Streamlit
            st.altair_chart(humidity_chart_an, use_container_width=True)

    with charts[1]:
        st.subheader(body="Temperature", anchor=False)
        if temperatureData.empty:
            st.write("No Data Available!")
        else:
            temperature_chart_an = alt.Chart(data=temperatureData).mark_area(
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
                    scale=alt.Scale(zero=False, domain=[10, 50]),
                    axis=alt.Axis(title="Temperature (°C)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                        alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            st.altair_chart(temperature_chart_an, use_container_width=True)


def operateFan():
    if st.session_state.FanState is False:
        anedya_sendCommand("Fan", "ON")
        anedya_setValue("Fan", True)
        st.session_state.FanButtonText = "Turn Fan Off!"
        st.session_state.FanState = True
        st.toast("Fan turned on!")
    else:
        st.session_state.FanButtonText = "Turn Fan On!"
        st.session_state.FanState = False
        anedya_sendCommand("Fan", "OFF")
        anedya_setValue("Fan", False)
        st.toast("Fan turned off!")


def operateLight():
    if st.session_state.LightState is False:
        anedya_sendCommand("Light", "ON")
        anedya_setValue("Light", True)
        st.session_state.LightButtonText = "Turn Light Off!"
        st.session_state.LightState = True
        st.toast("Light turned on!")
    else:
        anedya_sendCommand("Light", "OFF")
        anedya_setValue("Light", False)
        st.session_state.LightButtonText = "Turn Light On!"
        st.session_state.LightState = False
        st.toast("Light turned off!")


@st.cache_data(ttl=4, show_spinner=False)
def GetFanStatus() -> list:
    value = anedya_getValue("Fan")
    if value[1] == 1:
        on = value[0]
        if on:
            st.session_state.FanState = True
            st.session_state.FanButtonText = "Turn Fan Off!"
        else:
            st.session_state.FanState = False
            st.session_state.FanButtonText = "Turn Fan On!"
    return value


@st.cache_data(ttl=4, show_spinner=False)
def GetLightStatus() -> list:
    value = anedya_getValue("Light")
    if value[1] == 1:
        on = value[0]
        if on:
            st.session_state.LightState = True
            st.session_state.LightButtonText = "Turn Light Off!"
        else:
            st.session_state.LightState = False
            st.session_state.LightButtonText = "Turn Light On!"
    return value


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamviz
import pytz
from datetime import date, datetime,timedelta,time
from streamlit_autorefresh import st_autorefresh

from utils.anedya import anedya_config
from utils.anedya import anedya_sendCommand
from utils.anedya import anedya_getValue
from utils.anedya import anedya_setValue
from utils.anedya import fetchHumidityData
from utils.anedya import fetchTemperatureData
from utils.anedya import anedya_get_latestData

nodeId = "NODE_ID"  # get it from anedya dashboard -> project -> node
apiKey = "API_KEY"  # aneyda project apikey

st.set_page_config(page_title="Anedya IoT Dashboard", layout="wide")


st_autorefresh(interval=20000, limit=None, key="auto-refresh-handler")

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
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    if "from_date" not in st.session_state:
        # Get the current date
        current_date = datetime.now()
        # Extract the year, month, and day
        # Subtract one day to get yesterday's date
        yesterday_date = current_date - timedelta(days=1)
        # Extract the year, month, and day
        yesterday_year = yesterday_date.year
        yesterday_month = yesterday_date.month
        yesterday_day = yesterday_date.day
        # Create a date object for yesterday
        yesterday_date_object = date(yesterday_year, yesterday_month, yesterday_day)
        st.session_state.from_date = yesterday_date_object

    if "to_date" not in st.session_state:
        # Get the current date
        current_date = datetime.now()
        # Extract the year, month, and day
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        # Create a date object
        current_date_object = date(current_year, current_month, current_day)
        st.session_state.to_date = current_date_object

    if "from_time" not in st.session_state:
        # Get the current date
        current_date = datetime.now()
        # Extract the year, month, and day
        reset_date = current_date - timedelta(hours=3.8)
        hour = reset_date.hour
        minute = reset_date.minute
        # Create a date object
        current_time_object = time(hour, minute)       
        st.session_state.from_time = current_time_object
    if "to_time" not in st.session_state:
        # Get the current date
        current_date = datetime.now()
        # Extract the year, month, and day
        hour = current_date.hour
        minute = current_date.minute
        # Create a date object
        current_time_object = time(hour, minute)       
        st.session_state.to_time = current_time_object

    if "from_input_time" not in st.session_state:
        current_date = datetime.now()
        epoach_time=int(current_date.timestamp())
        st.session_state.from_input_time = int(epoach_time - 86400)
    if "to_input_time" not in st.session_state:
        current_date = datetime.now()
        epoach_time=int(current_date.timestamp())
        st.session_state.to_input_time = epoach_time

        
    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        # st.session_state.counter=st.session_state.counter+1
        # st.write(st.session_state.counter)
        st.session_state.CurrentHumidity = anedya_get_latestData("humidity")
        st.session_state.CurrentTemperature = anedya_get_latestData("temperature")

        interval=st.session_state.to_input_time - st.session_state.from_input_time
        agg_interval=10
        if interval > 2592000:
            agg_interval = 60
        elif interval > 864000:
            agg_interval = 30
        elif interval > 86400:
            agg_interval = 10
        humidityData = fetchHumidityData(param_from=st.session_state.from_input_time, param_to=st.session_state.to_input_time,param_aggregation_interval_in_minutes=agg_interval)
        temperatureData = fetchTemperatureData(param_from=st.session_state.from_input_time, param_to=st.session_state.to_input_time,param_aggregation_interval_in_minutes=agg_interval)

        GetFanStatus()
        GetLightStatus()

        drawDashboard()


def drawLogin():
    cols = st.columns([1, 0.8, 1], gap="small")
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

    st.markdown(
        "This dashboard provides live view of the Anedya's Office. Also allowing you to control the Light and Fan remotely!"
    )

    st.subheader(body="Current Status", anchor=False)
    cols = st.columns(2, gap="medium", vertical_alignment="center")
    with cols[0]:
        with st.container(height=270, border=False):
            # st.metric(label="Humidity", value=str(st.session_state.CurrentHumidity) + " %")
            streamviz.gauge(
                gVal=(st.session_state.CurrentHumidity) / 100,
                gTitle="Humidity",
                gMode="gauge+number",
                gSize="MED",
                grLow=30,
                gcLow="blue",
                grMid=60,
                gcMid="green",
                gcHigh="red",
                sFix="%",
            )
    with cols[1]:
        with st.container(height=270, border=False):
            streamviz.gauge(
                gVal=st.session_state.CurrentTemperature,
                gTitle="Temperature",
                gMode="gauge+number",
                gSize="MED",
                grLow=40,
                gcLow="green",
                grMid=50,
                gcMid="orange",
                gcHigh="red",
                sFix="°C",
                arBot=0,
                arTop=100,
                cWidth=True,
            )

    # with cols[2]:
    # #    st.metric(label="Refresh Count", value=count)
    #     pass

    st.subheader(body="Controls", anchor=False)
    buttons = st.columns([0.2,0.2,0.6], gap="small")
    with buttons[0]:
        org_btn1=st.columns([0.4,0.6], gap="small",vertical_alignment="center")
        with org_btn1[0]:
            st.text("Control Fan:")
        with org_btn1[1]:
            st.button(label=st.session_state.FanButtonText, on_click=operateFan)

    with buttons[1]:
        org_btn2=st.columns([0.47,0.53], gap="small",vertical_alignment="center")
        with org_btn2[0]:
            st.text("Control Light:")
        with org_btn2[1]:
            st.button(label=st.session_state.LightButtonText, on_click=operateLight)

    with st.container():
        st.subheader(body="Time Range", anchor=False)
        datetime_cols = st.columns([1,1,0.2], gap="small", vertical_alignment="bottom")
        with datetime_cols[0]:
            from_cols=st.columns(2, gap="small")
            with from_cols[0]:
                # st.text("From:")
                from_start_datetime=st.date_input('From',key="from:date",value=st.session_state.from_date)
            with from_cols[1]:
                from_time_input=st.time_input('time',key="from:time",value=st.session_state.from_time,label_visibility="hidden")
            
            if from_start_datetime and from_time_input:
                st.session_state.from_time = from_time_input
                st.session_state.from_date = from_start_datetime
                
                combined_datetime = pd.to_datetime(f"{from_start_datetime} {from_time_input}")
                # st.write("Combined datetime:", combined_datetime)

                # Define the India time zone
                india_tz = pytz.timezone('Asia/Kolkata')

                # Localize the combined datetime to the India time zone
                localized_datetime = india_tz.localize(combined_datetime)

                # Convert the localized datetime to epoch time
                from_time = int(localized_datetime.timestamp())
                if from_time!=st.session_state.from_input_time:
                    st.session_state.from_input_time=from_time
                    st.rerun()

        with datetime_cols[1]:
            to_cols=st.columns(2)
            with to_cols[0]:
                # st.text("To:")
                to_start_datetime=st.date_input('To',key="to:date",value=st.session_state.to_date)
            with to_cols[1]:
                to_time_input=st.time_input('time',key="to:time",value=st.session_state.to_time,label_visibility="hidden")
            if to_start_datetime and to_time_input:
                st.session_state.to_time = to_time_input
                st.session_state.to_date = to_start_datetime
                combined_datetime = pd.to_datetime(f"{to_start_datetime} {to_time_input}")
                # st.write("Combined datetime:", combined_datetime)

                # Define the India time zone
                india_tz = pytz.timezone('Asia/Kolkata')

                # Localize the combined datetime to the India time zone
                localized_datetime = india_tz.localize(combined_datetime)

                # Convert the localized datetime to epoch time
                to_time = int(localized_datetime.timestamp())
                if to_time!=st.session_state.to_input_time:
                    st.session_state.to_input_time=to_time
                    st.rerun()

        with datetime_cols[2]:
            reset_btn=st.button(label="Set Default", on_click=reset_time_range)
            if reset_btn:
                st.rerun()

    # ------------------------chart container------------------------
    with st.container():
        # st.write(st.session_state.from_input_time, st.session_state.to_input_time)
        if st.session_state.from_input_time < st.session_state.to_input_time:
            charts = st.columns(2, gap="small")
            with charts[0]:
                st.subheader(body="Humidity ", anchor=False)

                if humidityData.empty:
                    st.write("No Data Available!")
                else:
                    humidity_chart_an = (
                        alt.Chart(data=humidityData)
                        .mark_area( # type: ignore
                            line={"color": "#1fa2ff"},
                            color=alt.Gradient(
                                gradient="linear",
                                stops=[
                                    alt.GradientStop(color="#1fa2ff", offset=1),
                                    alt.GradientStop(color="rgba(255,255,255,0)", offset=0),
                                ],
                                x1=1,
                                x2=1,
                                y1=1,
                                y2=0,
                            ),
                            interpolate="monotone",
                            cursor="crosshair",
                        )
                        .encode(  # type: ignore
                            x=alt.X(
                                shorthand="Datetime:T",
                                axis=alt.Axis(
                                    format="%Y-%m-%d %H:%M:%S",
                                    title="Datetime",
                                    tickCount=10,
                                    grid=True,
                                    tickMinStep=5,
                                ),
                            ),  # T indicates temporal (time-based) data
                            y=alt.Y(
                                "aggregate:Q",
                                scale=alt.Scale(domain=[20, 100]),
                                axis=alt.Axis(title="Humidity (%)", grid=True, tickCount=10),
                            ),  # Q indicates quantitative data
                            tooltip=[
                                alt.Tooltip(
                                    "Datetime:T",
                                    format="%Y-%m-%d %H:%M:%S",
                                    title="Time",
                                ),
                                alt.Tooltip("aggregate:Q", format="0.2f", title="Value"),
                            ],
                        )
                        .properties(height=400)
                        .interactive()
                    )

                    # Display the Altair chart using Streamlit
                    st.altair_chart(humidity_chart_an, use_container_width=True)

            with charts[1]:
                st.subheader(body="Temperature", anchor=False)

                if temperatureData.empty:
                    st.write("No Data Available!")
                else:
                    temperature_chart_an = (
                        alt.Chart(data=temperatureData)
                        .mark_area( # type: ignore
                            line={"color": "#1fa2ff"},
                            color=alt.Gradient(
                                gradient="linear",
                                stops=[
                                    alt.GradientStop(color="#1fa2ff", offset=1),
                                    alt.GradientStop(color="rgba(255,255,255,0)", offset=0),
                                ],
                                x1=1,
                                x2=1,
                                y1=1,
                                y2=0,
                            ),
                            interpolate="monotone",
                            cursor="crosshair",
                        )
                        .encode(  # type: ignore
                            x=alt.X(
                                shorthand="Datetime:T",
                                axis=alt.Axis(
                                    format="%Y-%m-%d %H:%M:%S",
                                    title="Datetime",
                                    tickCount=10,
                                    grid=True,
                                    tickMinStep=5,
                                ),
                            ),  # T indicates temporal (time-based) data
                            y=alt.Y(
                                "aggregate:Q",
                                # scale=alt.Scale(domain=[0, 100]),
                                scale=alt.Scale(zero=False, domain=[10, 50]),
                                axis=alt.Axis(
                                    title="Temperature (°C)", grid=True, tickCount=10
                                ),
                            ),  # Q indicates quantitative data
                            tooltip=[
                                alt.Tooltip(
                                    "Datetime:T",
                                    format="%Y-%m-%d %H:%M:%S",
                                    title="Time",
                                ),
                                alt.Tooltip("aggregate:Q", format="0.2f", title="Value"),
                            ],
                        )
                        .properties(height=400)
                        .interactive()
                    )  # type: ignore

                    st.altair_chart(temperature_chart_an, use_container_width=True)
        else:
            st.warning("  'To' should be greater than 'From'",icon="⚠️")
    # ----------------------- Map Container------------------------------------            
    with st.container():
        st.subheader(body="Device Location", anchor=False)
        locationData = pd.DataFrame(
            {"latitude": [23.074214884363126], "longitude": [72.52071042512968]}
        )
        st.map(
            locationData, zoom=16, color="#0044ff", size=14, use_container_width=True
        )


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

def reset_time_range():
    # Get the current date
    current_date = datetime.now()
    # Extract the year, month, and day
    hour = current_date.hour
    minute = current_date.minute
    # Create a date object
    current_time_object = time(hour, minute)       
    st.session_state.to_time = current_time_object

    # Extract the year, month, and day
    reset_date = current_date - timedelta(hours=3.8)
    hour = reset_date.hour
    minute = reset_date.minute
    # Create a date object
    from_time_object = time(hour, minute)       
    st.session_state.from_time = from_time_object
    
    # Extract the year, month, and day
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    # Create a date object
    current_date_object = date(current_year, current_month, current_day)
    st.session_state.to_date = current_date_object

    # Subtract one day to get yesterday's date
    yesterday_date = current_date - timedelta(days=1)
    # Extract the year, month, and day
    yesterday_year = yesterday_date.year
    yesterday_month = yesterday_date.month
    yesterday_day = yesterday_date.day
    # Create a date object for yesterday
    yesterday_date_object = date(yesterday_year, yesterday_month, yesterday_day)
    st.session_state.from_date = yesterday_date_object

    # st.rerun()


if __name__ == "__main__":
    main()

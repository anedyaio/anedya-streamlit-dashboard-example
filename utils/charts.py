# utils/charts.py
import streamlit as st
import altair as alt

from utils.global_vars import temperatureData, humidityData


def HumidityChart(start_date,end_date):
    global humidityData
    st.subheader(body="Humidity ", anchor=False)
    if humidityData.empty:
        st.write("No Data !!")
    else:
        humidity_chart_an = alt.Chart(data=humidityData[(humidityData['Datetime']>=start_date)&(humidityData['Datetime']<=end_date)]).mark_area(
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
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(title="Humidity (%)", grid=True, tickCount=10),
            ),  # Q indicates quantitative data
            tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                    alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
        ).properties(height=400).interactive()

        # Display the Altair chart using Streamlit
        st.altair_chart(humidity_chart_an, use_container_width=True)

def TemperatureChart(start_date,end_date):
    global temperatureData
    st.subheader(body="Temperature", anchor=False)
    if temperatureData.empty:
        st.write("No Data !!")
    else:
        temperature_chart_an = alt.Chart(data=temperatureData[(temperatureData['Datetime']>=start_date)&(temperatureData['Datetime']<=end_date)]).mark_area(
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
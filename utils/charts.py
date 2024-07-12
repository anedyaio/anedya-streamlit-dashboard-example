# utils/charts.py
import streamlit as st
import altair as alt

from utils.global_vars import temperatureData, humidityData


def HumidityChart(start_date,end_date):
    st.subheader(body="Humidity ", anchor=False)

    csv_file = 'humidity_data.csv'
    if os.path.exists(csv_file):
        humidity_data = pd.read_csv(csv_file, index_col='Datetime', parse_dates=True)

        # Filter data within the specified range
        filtered_data = humidity_data[(humidity_data.index >= start_date) & (humidity_data.index <= end_date)]

        if not filtered_data.empty:
            humidity_chart_an = alt.Chart(filtered_data.reset_index()).mark_area(
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

        else:
            st.error("No data available in the specified range.",icon="🕵️‍♂️")
    
    else:
        st.error("No Data !!",icon="⚠️")

def TemperatureChart(start_date,end_date):
    st.subheader(body="Temperature", anchor=False)

    csv_file = 'temperature_data.csv'
    if os.path.exists(csv_file):
        temperature_data = pd.read_csv(csv_file, index_col='Datetime', parse_dates=True)

        # Filter data within the specified range
        filtered_data = temperature_data[(temperature_data.index >= start_date) & (temperature_data.index <= end_date)]
    
        if not temperatureData.empty:
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

        else:
            st.error("No data available in the specified range.",icon="🕵️‍♂️")
        
    else:
        st.error("No Data !!",icon="⚠️")
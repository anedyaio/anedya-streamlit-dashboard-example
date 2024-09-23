"""Charts for the dashboard."""
import streamlit as st
import altair as alt


# ====================== Altair charts ======================
def humidity_chart(param_humidity_data):
    if param_humidity_data.empty:
        st.write("No Data Available!")
    else:
        humidity_chart_an = (
            alt.Chart(data=param_humidity_data)
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
        
def temperature_chart(param_temperature_data):
    if param_temperature_data.empty:
        st.write("No Data Available!")
    else:
        temperature_chart_an = (
            alt.Chart(data=param_temperature_data)
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

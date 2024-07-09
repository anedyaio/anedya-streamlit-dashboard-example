# utils/action_buttons.py
import streamlit as st

from utils.anedya import anedya_sendCommand
from utils.anedya import anedya_setValue

def ButtonText():
    if "FanButtonText" not in st.session_state:
        st.session_state.FanButtonText = "Turn Fan On!"

    if "HumidifierButtonText" not in st.session_state:
        st.session_state.HumidifierButtonText = "Turn Humidifier On!"

    if "HomeVantilaterButtonText" not in st.session_state:
        st.session_state.HomeVantilaterButtonText = "Turn Home Vantilater On!"

    if "ExhaustFanButtonText" not in st.session_state:
        st.session_state.ExhaustFanButtonText = "Turn Exhaust Fan On!"

def State():
    if "HumidifierState" not in st.session_state:
        st.session_state.HumidifierState = False

    if "FanState" not in st.session_state:
        st.session_state.FanState = False

    if "HomeVantilaterState" not in st.session_state:
        st.session_state.HomeVantilaterState = False

    if "ExhaustFanState" not in st.session_state:
        st.session_state.ExhaustFanState = False

def CurrentData():
    if "CurrentHumidity" not in st.session_state:
        st.session_state.CurrentHumidity = 0

    if "CurrentTemperature" not in st.session_state:
        st.session_state.CurrentTemperature = 0
    
    if "CurrentCarbonMonoxide" not in st.session_state:
        st.session_state.CurrentCarbonMonoxide = 0

    if "CurrentCarbonDioxide" not in st.session_state:
        st.session_state.CurrentCarbonDioxide = 0

def operateExhaustFan():
    if st.session_state.ExhaustFanState is False:
        anedya_sendCommand("ExhaustFan", "ON")
        anedya_setValue("ExhaustFan", True)
        st.session_state.ExhaustFanState = True
        st.toast("Exhaust Fan turned on!",icon=":material/wind_power:")
        st.session_state.ExhaustFanButtonText = "Turn Exhaust Fan Off!"
    else:
        anedya_sendCommand("ExhaustFan", "OFF")
        anedya_setValue("ExhaustFan", False)
        st.session_state.ExhaustFanState = False
        st.toast("Exhaust Fan turned off!",icon=":material/settings_heart:")
        st.session_state.ExhaustFanButtonText = "Turn Exhaust Fan On!"

def operateHomeVantilater():
    if st.session_state.HomeVantilaterState is False:
        anedya_sendCommand("HomeVantilater", "ON")
        anedya_setValue("HomeVantilater", True)
        st.session_state.HomeVantilaterState = True
        st.toast("Home Vantilater turned on!",icon=":material/diversity_1:")
        st.session_state.HomeVantilaterButtonText = "Turn Home Vantilater Off!"
    else:
        anedya_sendCommand("HomeVantilater", "OFF")
        anedya_setValue("HomeVantilater", False)
        st.session_state.HomeVantilaterState = False
        st.toast("Home Vantilater turned off!",icon=":material/eco:")
        st.session_state.HomeVantilaterButtonText = "Turn Home Vantilater On!"

def operateHumidifier():
    if st.session_state.HumidifierState is False:
        anedya_sendCommand("Humidifier", "ON")
        anedya_setValue("Humidifier", True)
        st.session_state.HumidifierState = True
        st.toast("Humidifier turned on!",icon=":material/humidity_indoor:")
        st.session_state.HumidifierButtonText = "Turn Humidifier Off!"
    else:
        anedya_sendCommand("Humidifier", "OFF")
        anedya_setValue("Humidifier", False)
        st.session_state.HumidifierState = False
        st.toast("Humidifier turned off!",icon=":material/humidity_percentage:")
        st.session_state.HumidifierButtonText = "Turn Humidifier On!"

def operateFan():
    if st.session_state.FanState is False:
        anedya_sendCommand("Fan", "ON")
        anedya_setValue("Fan", True)
        st.session_state.FanState = True
        st.toast("Fan turned on!",icon=":material/mode_fan:")
        st.session_state.FanButtonText = "Turn Fan Off!"
    else:
        anedya_sendCommand("Fan", "OFF")
        anedya_setValue("Fan", False)
        st.session_state.FanState = False
        st.toast("Fan turned off!",icon=":material/mode_fan_off:")
        st.session_state.FanButtonText = "Turn Fan On!"

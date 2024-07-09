# utils/login.py
import streamlit as st
import time as ts


def drawLogin():
    titlecol = st.columns([1, 0.8, 1], gap='small')
    with titlecol[1]:
        st.title("Anedya Dashboard", anchor=False)
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")
        submit_button = st.button(label="Submit")

        if submit_button:
            if username_inp == "admin" and password_inp == "admin":
                st.success("Login Successful",icon="✅")
                ts.sleep(1)
                st.session_state.LoggedIn = True
                st.rerun()
            else:
                st.error("Invalid Credentials!",icon="⚠️")

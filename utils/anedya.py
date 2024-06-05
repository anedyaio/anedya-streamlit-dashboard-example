import json
import requests
import time
import streamlit as st

nodeId = ""
apiKey = ""



def anedya_config(NODE_ID,API_KEY):
    global nodeId,apiKey
    nodeId=NODE_ID
    apiKey=API_KEY

def anedya_sendCommand(COMMAND_NAME, COMMAND_DATA):

    url = "https://api.anedya.io/v1/commands/send"
    apiKey_in_formate = "Bearer " + apiKey

    commandExpiry_time = int(time.time() + 518400) * 1000

    payload = json.dumps(
        {
            "nodeid": nodeId,
            "command": COMMAND_NAME,
            "data": COMMAND_DATA,
            "type": "string",
            "expiry": commandExpiry_time,
        }
    )
    headers = {"Content-Type": "application/json", "Authorization": apiKey_in_formate}

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    # st.write(response.text)


def anedya_setValue(KEY,VALUE):
    url = "https://api.anedya.io/v1/valuestore/setValue"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps({
    "namespace": {
        "scope": "node",
        "id": nodeId
    },
    "key": KEY,
    "value": VALUE,
    "type": "boolean"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    "Authorization": apiKey_in_formate
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.status_code)
    # print(payload)
    print(response.text)
    return response

def anedya_getValue(KEY):
    
    url = "https://api.anedya.io/v1/valuestore/getValue"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps({
    "namespace": {
        "scope": "node",
        "id": nodeId
    },
    "key": KEY
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    "Authorization": apiKey_in_formate
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseMessage=response.text
    print(responseMessage)
    errorCode=json.loads(responseMessage).get("errorcode")
    if errorCode==0:
        data=json.loads(responseMessage).get("value")
        value=[data,1]
    else:
        print(responseMessage)
        # st.write("No previous value!!")
        value=[False,-1]
     
    return value



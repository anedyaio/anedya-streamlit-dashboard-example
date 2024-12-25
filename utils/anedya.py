import json
import requests
import time
import uuid
import streamlit as st
import pandas as pd
import pytz  # Add this import for time zone conversion

nodeId = ""
apiKey = ""


def anedya_config(NODE_ID, API_KEY) -> bool:
    global nodeId, apiKey
    if NODE_ID == "" and API_KEY == "":
        st.error("Please config a valid NODE ID and API key.")
        return False
    elif API_KEY == "":
        st.error("Please config a valid API key.")
        return False
    elif NODE_ID == "":
        st.error("Please config a valid NODE ID.")
        return False
    try:
        # Create a UUID object from the provided string
        my_uuid = uuid.UUID(NODE_ID)
        # Get the version of the UUID
        version = my_uuid.version
        nodeId = NODE_ID
        apiKey = API_KEY
        return True
    except ValueError:
        st.error("Please enter a valid NODE ID.")
        return False


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

    requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    # st.write(response.text)


def anedya_setValue(KEY, VALUE):
    url = "https://api.anedya.io/v1/valuestore/setValue"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps(
        {
            "namespace": {"scope": "node", "id": nodeId},
            "key": KEY,
            "value": VALUE,
            "type": "boolean",
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": apiKey_in_formate,
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.status_code)
    # print(payload)
    print(response.text)
    return response


def anedya_getValue(KEY):
    url = "https://api.anedya.io/v1/valuestore/getValue"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps({"namespace": {"scope": "node", "id": nodeId}, "key": KEY})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": apiKey_in_formate,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseMessage = response.text
    print(responseMessage)
    errorCode = json.loads(responseMessage).get("errorcode")
    if errorCode == 0:
        data = json.loads(responseMessage).get("value")
        value = [data, 1]
    else:
        print(responseMessage)
        # st.write("No previous value!!")
        value = [False, -1]

    return value


@st.cache_data(ttl=15, show_spinner=False)
def anedya_get_latestData(param_variable_identifier: str) -> list:
    url = "https://api.anedya.io/v1/data/latest"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps({"nodes": [nodeId], "variable": param_variable_identifier})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": apiKey_in_formate,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_message = response.text
    # print(response_message)
    response_message_json=json.loads(response_message)
    data = response_message_json.get("data")
    if response_message_json.get("success"):
        if data !={}:
            data = response_message_json.get("data")[nodeId].get("value")
            timestamp = response_message_json.get("data")[nodeId].get("timestamp")
            # print(data, timestamp)
            return [data, timestamp]
        else:
            return [None, None]
    else:
        st.error(f"Response for {param_variable_identifier}: {response_message_json.get("error")}")
        st.stop()


def anedya_getData(
    param_variable_identifier: str,
    param_from: int,
    param_to: int,
    param_aggregation_interval_in_minutes: float,
) -> list:
    url = "https://api.anedya.io/v1/aggregates/variable/byTime"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps(
        {
            "variable": param_variable_identifier,
            "from": param_from,
            "to": param_to,
            "config": {
                "aggregation": {"compute": "avg", "forEachNode": True},
                "interval": {
                    "measure": "minute",
                    "interval": param_aggregation_interval_in_minutes,
                },
                "responseOptions": {"timezone": "UTC"},
                "filter": {"nodes": [nodeId], "type": "include"},
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": apiKey_in_formate,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_message = response.text
    res_code = response.status_code
    return [response_message, res_code]


@st.cache_data(ttl=60, show_spinner=False)
def fetchHumidityData(
    param_from, param_to, param_aggregation_interval_in_minutes=10
) -> pd.DataFrame:
    # currentTime = int(time.time())
    # pastHour_Time = int(currentTime - 86400)
    # st.session_state.counter=st.session_state.counter+1
    # st.write(st.session_state.counter)

    response_message = anedya_getData(
        "humidity",
        param_from=param_from,
        param_to=param_to,
        param_aggregation_interval_in_minutes=param_aggregation_interval_in_minutes,
    )

    if response_message[1] == 200:
        data_list = []

        # Parse JSON string
        response_data = json.loads(response_message[0]).get("data")
        for timeStamp, value in reversed(response_data.items()):
            for entry in reversed(value):
                data_list.append(entry)

        if data_list:

            # st.session_state.CurrentHumidity = round(data_list[0]["aggregate"], 2)
            df = pd.DataFrame(data_list)
            # Convert timestamp to datetime and set it as the index
            df["Datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            local_tz = pytz.timezone("Asia/Kolkata")  # Change to your local time zone
            df["Datetime"] = (
                df["Datetime"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
            )
            df.set_index("Datetime", inplace=True)
            # Drop the original 'timestamp' column as it's no longer needed
            df.drop(columns=["timestamp"], inplace=True)
            # print(df.head(70))
            # Reset the index to prepare for Altair chart
            chart_data = df.reset_index()

        return chart_data
    else:
        # st.write(response_message)
        print(response_message[0])
        value = pd.DataFrame()
        return value


@st.cache_data(ttl=60, show_spinner=False)
def fetchTemperatureData(
    param_from=0, param_to=0, param_aggregation_interval_in_minutes=10
) -> pd.DataFrame:

    # currentTime = int(time.time())    #to means recent time
    # pastHour_Time = int(currentTime - 86400)

    response_message = anedya_getData(
        "temperature",
        param_from=param_from,
        param_to=param_to,
        param_aggregation_interval_in_minutes=param_aggregation_interval_in_minutes,
    )

    if response_message[1] == 200:
        data_list = []

        # Parse JSON string
        response_data = json.loads(response_message[0]).get("data")
        for timeStamp, value in reversed(response_data.items()):
            for entry in reversed(value):
                data_list.append(entry)

        if data_list:
            # st.session_state.CurrentTemperature = round(data_list[0]["aggregate"], 2)
            df = pd.DataFrame(data_list)
            df["Datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            local_tz = pytz.timezone("Asia/Kolkata")  # Change to your local time zone
            df["Datetime"] = (
                df["Datetime"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
            )
            df.set_index("Datetime", inplace=True)

            # Droped the original 'timestamp' column as it's no longer needed
            df.drop(columns=["timestamp"], inplace=True)
            # print(df.head())
            # Reset the index to prepare for Altair chart
            chart_data = df.reset_index()

        return chart_data
    else:
        # st.write(response_message)
        print(response_message[0])
        value = pd.DataFrame()
        return value


@st.cache_data(ttl=50, show_spinner=False)
def anedya_getDeviceStatus():
    url = "https://api.anedya.io/v1/health/status"
    apiKey_in_formate = "Bearer " + apiKey

    payload = json.dumps({"nodes": [nodeId], "lastContactThreshold": 60})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": apiKey_in_formate,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseMessage = response.text
    print(responseMessage)
    errorCode = json.loads(responseMessage).get("errcode")
    if errorCode == 0:
        device_status = json.loads(responseMessage).get("data")[nodeId].get("online")
        value = [device_status, 1]
    else:
        print(responseMessage)
        # st.write("No previous value!!")
        value = [False, -1]

    return value

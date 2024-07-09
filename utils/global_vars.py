# utils/global_vars.py
import pandas as pd

# HumidityData = pd.DataFrame()
# TemperatureData = pd.DataFrame()
# CarbonMonoxideData = pd.DataFrame()
# CarbonDioxideData = pd.DataFrame()

humidityData = pd.DataFrame()
# humidityData = pd.DataFrame(columns=['Datetime', 'aggregate'])
temperatureData = pd.DataFrame()
carbonmonoxideData = pd.DataFrame()
carbondioxideData = pd.DataFrame()

nodeId = "YOUR-NODE-ID"  # get it from anedya dashboard -> project -> node 
apiKey = "YOUR-CONNECTION-KEY"

multiselect = ""
select = ""
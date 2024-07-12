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

nodeId = "300e6de2-25ab-11ef-84ba-139754672fc5"  # get it from anedya dashboard -> project -> node 
apiKey = "de86d4be9edd1229709dc8de0c3376a5b92586ed6c394db93cc12cadeee3077a"

multiselect = []
select = []
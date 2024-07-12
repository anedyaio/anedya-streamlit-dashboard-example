# utils/charts_simulation.py
from utils.charts import TemperatureChart, HumidityChart

function_dict = {
    "TemperatureChart": TemperatureChart,
    "HumidityChart": HumidityChart,
    "CarbonMonoxideChart": TemperatureChart,
    "CarbonDioxideChart": HumidityChart,
}
def chart_simulate(parameters):
    for chart_name in parameters:
        for chart_name in function_dict:
            function_dict[chart_name]()

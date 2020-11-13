import numpy as np
import pandas as pd 

sensor_data = pd.read_json('sensors.json')

print(sensor_data.head())
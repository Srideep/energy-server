#!/usr/bin/env python3
from bottle import run, route, request, response, Bottle
import json
import pandas as pd 

"""
Author : Srideep Maulik
"""
#Reading Current, Voltage and Time values of the Sensor from its json file
sensor_data = pd.read_json('sensors.json')



def approx_energy(starttime, stoptime):
    '''Approximate the Energy Consumption (kWh) of the Senson over an interval of time.   

    Parameters
    ----------    
    start_time , stop_time : Interval of time for the energy approximation (seconds)          

    Returns
    -------
    total_energy : Approximation of the energy consumption in kWh over the intereted time interval
    '''
    start_time = int(starttime)
    stop_time = int(stoptime)
    time_range = list(range(start_time, stop_time))    
    selected_data = sensor_data.query('time == @time_range')
    current = selected_data['current'].sum(axis=0)
    voltage = selected_data['voltage'].sum(axis=0)
    time = selected_data['time'].sum(axis=0)
    energy_kWh = (voltage*current*time)/(36*pow(10,5))    
    total_energy = round(energy_kWh/(pow(10,12)), 3) 

    result = {"results": { "energy": total_energy, "unit": "kWh" }}

    return result

"""Declaration Bottle Application"""
app = Bottle()


# POST method Server for the accepting the time interval parameters
@app.route('/', method='POST')
def sensor_power():
    sensor_dict = {}
    for item in request.params:
        sensor_dict[item]=request.params.get(item)
    start_time = sensor_dict["starttime"]
    end_time = sensor_dict["endtime"]
    data = approx_energy(start_time, end_time)       
    return '{}\n'.format(data)
    


    

"""Application is deployed"""

run(app,host='localhost', port=8080, debug=True, reloader=True)


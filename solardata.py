# -*- coding: utf-8 -*-
"""
File: solardata.py
Author: Nathan Fritsche <ccoderun@gmail.com>
Date: 2024-01-21

Gathers real-time solar data including stats, events and alerts related to solar activity.
"""

# Copyright (C) 2024 Nathan Fritsche

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import requests
import os
from dotenv import load_dotenv

load_dotenv()
tok = os.getenv('NCDC_TOK')

# SEE: https://www.ncdc.noaa.gov/cdo-web/webservices/

#TODO: DocStrings, PEP-8 Linting
def fetch_solar_data():
    """
    Summary of the function.
    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.

    Returns:
        Description of the return value.
    """  
    api_url = "https://services.swpc.noaa.gov/products/solar-wind/"
    plasma_1day = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    curr_solar_windspeed = 'https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json'
    alerts = 'https://services.swpc.noaa.gov/products/alerts.json'
    try:
        solar_data = {}
        response = requests.get(plasma_1day)
        response.raise_for_status()
        plasma_data = response.json()
        solar_data['plasma'] = plasma_data
        print(f'Plasma 1 Day: {plasma_data}')
        # #
        response = requests.get(alerts)
        response.raise_for_status()
        alert_data = response.json()
        print(f'Alerts: {alert_data}')
        alerts2024 = []
        for d in alert_data:
            if '2024' in d.get('issue_datetime','na'):
                alerts2024.append(d)
        for alert_msg in alerts2024:
            adt = alert_msg.get('issue_datetime', 'na')
            ams = alert_msg.get('message', 'na')
            print('-'*30)
            print(f'# {adt}: {ams}\n')
        # #
        solar_data['alerts'] = alerts2024
        response = requests.get(curr_solar_windspeed)
        response.raise_for_status()
        wind_data = response.json()
        solar_data['wind'] = wind_data
        print(f'Solar Windspeed: {wind_data}')

        return solar_data
    except requests.exceptions.RequestException as e:
        print("Error fetching solar data:", e)
        return None

def get_category(value, typical_values):
    if value <= typical_values["very_low"]:
        return "Very Low"
    elif value <= typical_values["low"]:
        return "Low"
    elif value <= typical_values["medium"]:
        return "Medium"
    elif value <= typical_values["high"]:
        return "High"
    else:
        return "Very High"

def display_solar_data(solar_data):
    if not solar_data:
        return
    
    typical_values = {
        "sunspots": 50,
        "x_class_flares": 5,
        "m_class_flares": 20,
        "c_class_flares": 100,
        "solar_wind_speed": 500,
        "solar_wind_density": 10,
        "kp_index": 5,
        "goes_xray_flux": 1.0e-5
    }
    
    sunspots = solar_data["sunspots"]
    solar_flare_activity = solar_data["flare_activity"]
    solar_activity = solar_data["solar_activity"]

    print("Current Solar Data:")
    print("-------------------")
    print("Sunspots:")
    print("  - Number of Sunspots: ", sunspots["number"], "(", get_category(sunspots["number"], typical_values["sunspots"]), ")")
    print("  - Latest Observation Time: ", sunspots["latest_observation_time"])
    print("  - Location: ", sunspots["location"])
    print()

    print("Solar Flare Activity:")
    print("  - X-class Flares: ", solar_flare_activity["xray_flux"]["xray_class_count"]["x"], "(", get_category(solar_flare_activity["xray_flux"]["xray_class_count"]["x"], typical_values["x_class_flares"]), ")")
    print("  - M-class Flares: ", solar_flare_activity["xray_flux"]["xray_class_count"]["m"], "(", get_category(solar_flare_activity["xray_flux"]["xray_class_count"]["m"], typical_values["m_class_flares"]), ")")
    print("  - C-class Flares: ", solar_flare_activity["xray_flux"]["xray_class_count"]["c"], "(", get_category(solar_flare_activity["xray_flux"]["xray_class_count"]["c"], typical_values["c_class_flares"]), ")")
    print()

    print("Solar Activity:")
    print("  - Solar Wind Speed (km/s): ", solar_activity["solar_wind"]["speed"], "(", get_category(solar_activity["solar_wind"]["speed"], typical_values["solar_wind_speed"]), ")")
    print("  - Solar Wind Density (p/cm^3): ", solar_activity["solar_wind"]["density"], "(", get_category(solar_activity["solar_wind"]["density"], typical_values["solar_wind_density"]), ")")
    print("  - Kp Index: ", solar_activity["kp_index"]["current"], "(", get_category(solar_activity["kp_index"]["current"], typical_values["kp_index"]), ")")
    print("  - GOES X-ray Flux (W/m^2): ", solar_activity["goes_xray_flux"]["flux"], "(", get_category(solar_activity["goes_xray_flux"]["flux"], typical_values["goes_xray_flux"]), ")")
    print("  - GOES X-ray Class: ", solar_activity["goes_xray_flux"]["class"])

def show_definitions():
    print("Definitions:")
    print("-------------")
    print("Sunspots: The number of visible dark spots on the Sun's surface.")
    print("Solar Flare Activity: Measures the occurrence of solar flares in different classes (X, M, C).")
    print("Solar Wind Speed: The speed of the solar wind in kilometers per second.")
    print("Solar Wind Density: The density of the solar wind in protons per cubic centimeter.")
    print("Kp Index: A measure of geomagnetic activity caused by solar storms.")
    print("GOES X-ray Flux: Measures the X-ray radiation emitted by the Sun.")
    print("GOES X-ray Class: Classifies the X-ray flares based on their intensity.")
    

if __name__ == "__main__":
    solar_data = fetch_solar_data()
    print(solar_data)
    #TODO: Find correct API to give me all of this cool data! ANd then this will work. :)
    # display_solar_data(solar_data)

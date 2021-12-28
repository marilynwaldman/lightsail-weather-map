import os as os
import pathlib
import zipfile
import json
from functools import wraps, update_wrapper
from datetime import datetime
from pathlib import Path
from weather_data import  get_weather_data
from weather_map import make_weather_map 
import pandas as pd


from app import server

if __name__ == "__main__":

    #Bootstrap(server)
    server.config['TEMPLATES_AUTO_RELOAD'] = True
    server.vars = {}

    logo_path = os.path.join(server.root_path, 'static/img/logo.png' )
    server.vars['logo_path'] = logo_path
    map_dir = os.path.join(server.root_path, 'weathermaps')
    map_path = os.path.join(map_dir, 'wxwarning.html')
    server.vars['map_path'] = map_path
    #weather_df =  get_weather_data(server)
    #time_now = make_weather_map(weather_df, map_path)
    #server.vars['current_map_time'] = time_now
    #print(weather_df.head())

    server.run(host='0.0.0.0', port=8000)
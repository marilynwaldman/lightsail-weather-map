import os as os
import pathlib
import zipfile
import json
from functools import wraps, update_wrapper
from datetime import datetime
from pathlib import Path
from weather_data import  get_weather_data
from weather_map import make_weather_map 
import shutil


from app import server

if __name__ == "__main__":

    #Bootstrap(server)
    #server.config['TEMPLATES_AUTO_RELOAD'] = True
    #server.vars = {}
    cwd = Path.cwd()

    logo_path = os.path.join(cwd, 'static/img/logo.png' )
    server.vars['logo_path'] = logo_path
    map_dir = os.path.join(cwd, 'weathermaps')
    if os.path.exists(map_dir) and os.path.isdir(map_dir):
         shutil.rmtree(map_dir)

    os.mkdir(map_dir) 
    map_path =  str(map_dir)+'wxwarning.html'
    server.vars['map_path'] = map_path
    server.vars['map_dir'] = map_dir
    #weather_df =  get_weather_data(server)
    #time_now = make_weather_map(weather_df, map_path)
    #server.vars['current_map_time'] = time_now
    #print(weather_df.head())

    server.run(host='0.0.0.0', port=8000)
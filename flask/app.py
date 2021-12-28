import os as os
from functools import wraps, update_wrapper
from datetime import datetime
from pathlib import Path
from weather_data import  get_weather_data
from weather_map import make_weather_map 
import geopandas as gpd



#from ediblepickle import checkpoint
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response


###############################################
#      Define navbar with logo                #
###############################################



server = Flask(__name__)

#Bootstrap(app)
server.config['TEMPLATES_AUTO_RELOAD'] = True
server.vars = {}

def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
        
  return update_wrapper(no_cache, view)


@server.route('/')
def main():
  return redirect('/index.html')

@server.route('/index.html', methods=['GET'])
def index():
  if request.method == 'GET':
    #static_dir = os.path.join(server.root_path, 'static/')
    #map_path = os.path.join(static_dir, 'wxwarning.html')
    
    map_path = server.vars.get("map_path")
    print(map_path)
    weather_df =  get_weather_data(server)
    #if weather_df is None:
    #  return redirect('/dataerror.html')
    timestamp = make_weather_map(weather_df, map_path)
    server.vars['Title_line1'] = 'Current U.S. Weather Statements'
    server.vars['Title_line2'] = timestamp[0:10]+' '+timestamp[11:16]+' UTC'
    print(map_path)
    #server.vars['map_path'] = map_path
    #print(server.vars['map_path'])
    

    if Path(map_path).exists():
        return render_template('display.html', vars=server.vars)
    else:     
        return redirect('/maperror.html')

    pass



@server.route('/maps/map.html')
@nocache
def show_map():
  
  map_path = server.vars.get("map_path")
  print("show map")
  print(map_path)
  map_file = Path(map_path)
  if map_file.exists():
    return send_file(map_path)
  else:
    return render_template('error.html', culprit='map file', details="the map file couldn't be loaded")

  pass


@server.route('/get_logo')
def get_logo():
  #logo_path = os.path.join(server.root_path, 'static/img/logo.png' )
  logo_path = server.vars.get("logo_path")
  logo_file = Path(logo_path)
  if logo_file.exists():
    return send_file(logo_path)
  else:
    return render_template('error.html', culprit='logo file', details="the logo file couldn't be loaded")

  pass


@server.route('/error.html')
def error():
  details = "There was some kind of error."
  return render_template('error.html', culprit='logic', details=details)

@server.route('/apierror.html')
def apierror():
  details = "There was an error with one of the API calls you attempted."
  return render_template('error.html', culprit='API', details=details)

@server.route('/maperror.html')
def geoerror():
  details = "Map not found."
  return render_template('error.html', culprit='the Map', details=details)

@server.route('/dataerror.html')
def dataerror():
  details = "Weather data not found."
  return render_template('error.html', culprit='the Weather Data', details=details)

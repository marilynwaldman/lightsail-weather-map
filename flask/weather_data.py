# Program wxwarning
# by Todd Arbetter (todd.e.arbetter@gmail.com)
# Software Engineer, IXMap, Golden, CO

# collects latests National Weather Service Warnings, Watches, Advisories,
# and Statements, plots shapefiles on an interactive map in various colors.
# The map is able to pan and zoom, and on mouseover will give the type of
# weather statement, start, and expiry.

# created with streamlit and folium

# import some libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import requests
from requests.models import ChunkedEncodingError
import os as os
import shutil
import requests
import tarfile
import datetime as dt
import ssl
import urllib3


def get_weather_data(app):
    # We create a downloads directory within the streamlit static asset directory
    # and we write output files to it

    #get latest wx warnings from NWS
    dest_path = os.path.join(os.getcwd(), 'downloads/')
     
    if os.path.exists(dest_path) and os.path.isdir(dest_path):
         shutil.rmtree(dest_path)

    os.mkdir(dest_path) 
    destination =  str(dest_path)+'current_all.tar.gz'
    url='https://tgftp.nws.noaa.gov/SL.us008001/DF.sha/DC.cap/DS.WWA/current_all.tar.gz'
    
    http = urllib3.PoolManager()
    resp = http.request(
         "GET",
          url,
          preload_content=False)
    print("response code")
    print(resp.status)

    
    with open(destination,"wb") as f:
        for chunk in resp.stream(32):
                f.write(chunk)

    resp.release_conn()

    wxdata = tarfile.open(name=destination)
    
    wxdata.list(verbose=True)

    wxdata.extractall(path=str(dest_path)+'/current_all/')


    infile = str(dest_path) + '/current_all/current_all.shp'

    #Read in weather info

    weather_df = gpd.read_file(infile)

    #weather_df = gpd.read_file('current_warnings/current_warnings.shp')

    weather_df = weather_df.drop(columns=['PHENOM','SIG','WFO','EVENT','ONSET','ENDS','CAP_ID','MSG_TYPE','VTEC'])
    
    return weather_df




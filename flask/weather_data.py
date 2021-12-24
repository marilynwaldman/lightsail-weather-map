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

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response,destination):
    CHUNK_SIZE=32768
    i = 1
    with open(destination,"wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
#                st.write('Chunk:',i)
                f.write(chunk)
                i += 1


def get_weather_data(app):
    # We create a downloads directory within the streamlit static asset directory
    # and we write output files to it

    #get latest wx warnings from NWS
    url='https://tgftp.nws.noaa.gov/SL.us008001/DF.sha/DC.cap/DS.WWA/current_all.tar.gz'

    session = requests.Session()

    response = session.get(url,stream=True,verify=False)
    token = get_confirm_token(response)

    if token:
        params = {'confirm':token}
        response = session.get(url,params=params,stream=True,verify=False)

    #have to set map path - used by template

    dest_path = os.path.join(os.getcwd(), 'downloads/')
     
    if os.path.exists(dest_path) and os.path.isdir(dest_path):
         shutil.rmtree(dest_path)

    os.mkdir(dest_path)   
    print("in weather data")  

    destination =  str(dest_path)+'current_all.tar.gz'

    save_response_content(response,destination)
    wxdata = tarfile.open(name=destination)
    wxdata.list(verbose=True)

    wxdata.extractall(path=str(dest_path)+'/current_all/')

    print('extracted data')

    infile = str(dest_path) + '/current_all/current_all.shp'

    #Read in weather info

    weather_df = gpd.read_file(infile)

    #weather_df = gpd.read_file('current_warnings/current_warnings.shp')

    weather_df = weather_df.drop(columns=['PHENOM','SIG','WFO','EVENT','ONSET','ENDS','CAP_ID','MSG_TYPE','VTEC'])
    
    return weather_df




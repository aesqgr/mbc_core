import streamlit as st

import json
from src.yelp_api import requests
import json
import pandas as pd
import sys
from streamlit_folium import folium_static
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/")
from config import geo_districts, geo_hoods, local_ip
import folium
import socket


def app():
    st.title('Home')
    st.write('This is the `home page` of this multi-page app.')
    


def get_datafr(name, detail):
    url_st = f"{local_ip}:5000/population/{detail}/"
    data = json.loads(requests.request("GET",url=url_st).text)["Population"]
    df = pd.DataFrame.from_dict(data).T[name]
    print(type(df))
    return df

def get_hoods():
    req = requests.request("GET", url=f"{local_ip}:5000/population/general/hoods")
    data = json.loads(req.text)
    return data["Neighborhood"]

def get_districts():
    req = requests.request("GET", url=f"{local_ip}:5000/population/general/districts")
    data = json.loads(req.text)
    return data["Districts"]




def api_yelp(location):
    req = requests.request("GET", url=f"{local_ip}:5000/yelp/"+location)
    data = json.loads(req.text)
    df = pd.DataFrame(data["businesses"])
    return df




import streamlit as st
import json
from src.yelp_api import requests
import json
import pandas as pd
import sys
import folium
from matplotlib import pyplot as plt
from streamlit_folium import folium_static
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/")
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/src/dasboard_pages")
from config import geo_districts
from src.dashboard_pages.home_st import get_districts, api_yelp,geo_hoods,geo_districts,get_datafr,local_ip,get_hoods


def app():
    st.title('Population')
    st.write('This is the *population* page.')
    columns_select = st.beta_columns(2)
    with columns_select[0]:
        district_option = st.selectbox('Select Disctric', (get_districts()))
    with columns_select[1]:
        year_option = st.slider('Select year :', 2013, 2017)
    st.pyplot(df_hoods(district_option,year_option))
    st.header("Evolution of population")
    columns = st.beta_columns(2)
    with columns[0]:
        option = st.radio('Select level of detail:', ('district', 'hood'))
    with columns[1]:
        year = st.slider('Select year:', 2013, 2017)
    st.markdown("<div style = color:#0f1117"+str(folium_static(heat_map(option,year)))+"</div>", unsafe_allow_html=True)



def heat_map(detail,year):
    url_st = f"{local_ip}:5000/population/{detail}/"
    data = json.loads(requests.request("GET",url=url_st).text)["Population"][str(year)]
    result = {}
    result["Name"] = {index:list(data.keys())[index] for index in range(len(list(data.keys())))}
    result["Population"] = {index:list(data.values())[index] for index in range(len(list(data.values())))}
    mapa = folium.Map(
        location=[41.387900,2.1699200],
        tiles="cartodbdark_matter",
        zoom_start=11,
    )
    df = pd.DataFrame.from_dict(result)
    folium.Choropleth(
        geo_data = geo_districts if detail == 'district' else geo_hoods,
        name= "choropleth",
        data=df,
        columns=["Name","Population"],
        key_on="properties.NOM",
        bins = 9,
        fill_color="OrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Population per {detail} in {year} ",
    ).add_to(mapa)
    
    return mapa

def get_chart_values(detail,year):
    url_st = f"{local_ip}:5000/population/{detail}/"
    data = json.loads(requests.request("GET",url=url_st).text)["Population"]["2017"]
    result = {}
    result["District"] = {index:list(data.keys())[index] for index in range(len(list(data.keys())))}
    result["Population"] = {index:list(data.values())[index] for index in range(len(list(data.values())))}
    return pd.DataFrame(result).T


def df_hoods(district,year):
    url = "http://192.168.88.243:5000/population/district/hoods"
    req = requests.request("GET",url=url)
    values = json.loads(req.text)
    data = values["Population"][str(year)][district]
    fig = plt.figure(figsize=(5,5))
    plt.bar(list(data.keys()), list(data.values()))
    plt.xticks(rotation=90)
    fig.savefig('temp.png', transparent=True)
    return plt
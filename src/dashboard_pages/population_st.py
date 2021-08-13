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
from textwrap import wrap

def app():
    st.title('Population')
    st.write('This is the *population* page.')
    columns_select = st.beta_columns(2)
    with columns_select[0]:
        district_option = st.selectbox('Select Disctrict', (get_districts()))
    with columns_select[1]:
        year_option = st.slider('Select year :', 2013, 2017)
    columns_center = st.beta_columns(2)
    with columns_center[0]:
        st.pyplot(df_hoods(district_option,year_option))
    with columns_center[1]:
        st.pyplot(df_age(district_option,year_option))
    st.header("Population Heatmap")
    columns = st.beta_columns(2)
    with columns[0]:
        option = st.radio('Select level of detail:', ('district', 'hood'))
    with columns[1]:
        year = st.slider('Select year:', 2013, 2017)
    st.markdown("<div style = color:#0f1117"+str(folium_static(heat_map(option,year)))+"</div>", unsafe_allow_html=True)

@st.cache
def get_hood_data():
    url_st = f"{local_ip}:5000/population/hood/"
    data = json.loads(requests.request("GET",url=url_st).text)["Population"]
    return data

@st.cache
def get_district_data():
    url_st = f"{local_ip}:5000/population/district/"
    data = json.loads(requests.request("GET",url=url_st).text)["Population"]
    return data

def heat_map(detail,year):
    data = get_hood_data()[str(year)] if detail == 'hood' else get_district_data()[str(year)]
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


@st.cache
def get_dfhoods_data():
    url = f"{local_ip}:5000/population/district/hoods"
    req = requests.request("GET",url=url)
    values = json.loads(req.text)
    return values

def df_hoods(district,year):
    data = get_dfhoods_data()["Population"][str(year)][district]
    fig = plt.figure()
    ax = plt.axes()
    fig.set_facecolor('#0f1117')
    ax.set_facecolor('#0f1117')
    plt.xticks(rotation=45)
    labels = ['\n'.join(wrap(x, 12)) for x in  list(data.keys())]
    plt.barh(labels,list(data.values()), color="#810c09")
    params = {
            "ytick.color" : "w",
            "xtick.color" : "w",
            "axes.labelcolor" : "w",
            "axes.edgecolor" : "w"}
    plt.rcParams.update(params)
    return fig

def df_age(district,year):
    url = f"http://192.168.88.243:5000/population/district/age/{district}/{year}/gender/"
    req = requests.request("GET",url=url)
    data = json.loads(req.text)
    fig = plt.figure()
    ax = plt.axes()
    fig.set_facecolor('#0f1117')
    ax.set_facecolor('#0f1117')
    plt.xticks(rotation=45)
    plt.barh(list(data["Female"]),list(data["Female"].values()), color="#810c09")
    plt.barh(list(data["Male"]),list(data["Male"].values()), color="#810c09")
    params = {
                "ytick.color" : "w",
                "xtick.color" : "w",
                "axes.labelcolor" : "w",
                "axes.edgecolor" : "w"}
    plt.rcParams.update(params)
    plt.axvline(x=0)
    return fig
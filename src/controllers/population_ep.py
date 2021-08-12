import numpy as np
from src.app import app
from flask import request
from flask import jsonify
from src.database import population
import pandas as pd
import json
from src.helpers.handle_error import handle_error

all = population.find({})
df = pd.DataFrame(list(all))
app.config['JSON_AS_ASCII'] = False
ages = list(df["Age"].unique())
districts = list(df["District_Name"].unique())
years = list(df["Year"].unique())
hoods = list(df["Neighborhood_Name"].unique())
q = lambda x: population.find({"District_Name":x},{"Neighborhood_Name":1, "_id":0}).distinct("Neighborhood_Name")
district_hoods = {district:list(q(district)) for district in districts}

@handle_error
@app.route('/population/general/<options>')
def pop_general(options):
    if options == 'districts':
        return {"Districts": districts}
    elif options == 'hoods':
        return {"Neighborhood": hoods}
    elif options == 'district_hoods':
        return {"Districts and Hoods" : district_hoods}
    else:
        return {"Error":"Options are: districts, hoods or district_hoods"}


@handle_error
@app.route('/population/')
def pop_global():
    pop = df.groupby("Year")["Number"].sum().to_dict()
    return {"Population": pop}

@handle_error
@app.route('/population/district/')
def district():
    q = lambda x: pd.DataFrame(list(population.find({"Year":x},{"District_Name":1,"Number":1, "_id":0}))).groupby("District_Name")["Number"].sum()
    years_districts = {str(year):q(int(year)).to_dict() for year in years} 
    return {"Population" : years_districts}

@handle_error
@app.route('/population/hood/')
def district_hood():
    q = lambda x: pd.DataFrame(list(population.find({"Year":x},{"Neighborhood_Name":1,"Number":1, "_id":0}))).groupby("Neighborhood_Name")["Number"].sum()
    years_hoods = {str(year):q(int(year)).to_dict() for year in years} 
    return {"Population" : years_hoods}

@handle_error
@app.route('/population/district/hoods')
def district_detail_hood():
    q = lambda x: pd.DataFrame(list(population.find({"District_Name":x},{"Neighborhood_Name":1,"Number":1, "_id":0}))).groupby("Neighborhood_Name")["Number"].sum()
    years_districts_hoods = {str(year):{district:q(district).to_dict() for district in districts} for year in years} 
    return {"Population" : years_districts_hoods}
    
@handle_error
@app.route('/population/district/hoods/age')
def district_hood_age():
    q = lambda x,y: pd.DataFrame(list(population.find({"Neighborhood_Name":x, "Year":int(y)},{"Age":1,"Number":1, "_id":0}))).groupby("Age")["Number"].sum()
    years_districts_hoods_age = {str(year):{district:{hood:q(hood,year).to_dict() for  hood in district_hoods[district]} for district in districts} for year in years} 
    return {"Population" : years_districts_hoods_age}

@handle_error
@app.route('/population/district/hoods/age/<district>')
def district_hood_age_gender(district):
    q = lambda x,y,z: pd.DataFrame(list(population.find({"District_Name":district,"Neighborhood_Name":x, "Year":int(y),"Age":z},{"Gender":1,"Number":1, "_id":0}))).groupby("Gender")["Number"].sum()
    years_districts_hoods_age_gender = {str(year):{district:{hood:{age:q(hood,year,age).to_dict() for age in ages} for  hood in district_hoods[district]} for district in districts} for year in years} 
    return {"Population" : years_districts_hoods_age_gender}
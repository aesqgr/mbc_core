import numpy as np
from src.app import app
from flask import request
from src.database import population
import matplotlib.pyplot as plt
import pandas as pd

barrios = list(population.find({},{"District.Name":1,"Neighborhood.Name":1,"Gender":1,"Age":1,"Number":1, "_id":0}))
barri = [{"District": barrio["District"]["Name"],"Neighborhood": barrio["Neighborhood"]["Name"],"Age":barrio["Age"],"Gender":barrio["Gender"],"Number":barrio["Number"] } for barrio in barrios]
df_population = pd.DataFrame.from_dict(barri)
population = df_population.groupby(["District","Neighborhood"]).sum()



@app.route('/population/district/<district>')
def district(district):
    return {
        'Name': district,
        'Population': int(population.loc[district].sum())
    }


@app.route('/population/district/<district>/detail/')
def district_detail(district):
    return {
        'Name': district,
        'Population': population.loc[district].to_dict()['Number']
        }


@app.route('/population/hood/<neighborhood>')
def neighborhood_detail(neighborhood):
    return {
        "Name": neighborhood,
        "Population" : int(population.groupby("Neighborhood").sum().to_dict()["Number"][neighborhood])
        }


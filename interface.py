from flask import Flask, render_template, request, redirect, url_for
from zeep import Client
import folium
import requests
from db import get_voiture, get_autonomie, get_tempsRecharge
from math import *

app = Flask(__name__)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    car = get_voiture()
    return render_template('calcul.html', car=car)
	
@app.route('/calcul', methods=['GET', 'POST'])
def calcul():
    id = request.form['id']
    
    autonomie = get_autonomie(id)
    tempsRecharge = get_tempsRecharge(id)
    
    
    rue1 = request.form['rue1']
    voie1 = request.form['voie1']
    ville1 = request.form['ville1']
    rue2 = request.form['rue2']
    voie2 = request.form['voie2']
    ville2 = request.form['ville2']
    client = Client('http://127.0.0.1:8000/?wsdl')
    coords = client.service.getCoordinate(rue1,voie1,ville1)
    latStart = coords[0]
    lonStart = coords[1]
    coords2 = client.service.getCoordinate(rue2,voie2,ville2)
    latEnd = coords2[0]
    lonEnd = coords2[1]
    result = client.service.getDistance(rue1, voie1, ville1, rue2, voie2, ville2)
    result2 = client.service.getStops(autonomie, rue1, voie1, ville1, rue2, voie2, ville2)
    result = ceil(result)
    i = 0
    nbstop = 0
    list2 = []
    for i in result2:
        list2.append(i['float'])
        nbstop = nbstop+1
    
    tempsRecharge = 30
    url = f"http://127.0.0.1:5002/tempsTrajet/{result}/{nbstop}/{tempsRecharge}"
    reponse = requests.get(url)
    tempsJson = reponse.json()
    temps = tempsJson['result']
    
    
    
    #Follium
    
    # trip = []
    # trip.append(tuple[latStart,lonStart])
    
    map=folium.Map(width=1500,height=500,location=[latStart,lonStart], zoom_level=0)
    
    folium.Marker([latStart,lonStart]).add_to(map)
    for stop in list2:
        # trip.append(tuple(stop))
        folium.Marker(stop, popup="Borne", icon=folium.Icon(color='red')).add_to(map)
    folium.Marker([latEnd,lonEnd]).add_to(map)
    # trip.append(tuple([latEnd,lonEnd]))
    
    # print(trip)
    
    # folium.PolyLine(trip, color="red", weight=2.5, opacity=1).add_to(map)
    
    return render_template('trip.html', result=result, list2=list2, temps=temps, map=map._repr_html_())
    #latStart=latStart, lonStart=lonStart, latEnd=latEnd, lonEnd=lonEnd
    
# if __name__ == "__main__":
#     app.run(port=80)



#FOR TEST !!!!!

from spyne import Application, rpc, ServiceBase, Unicode, Iterable, Integer, Float, String
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import  Soap11
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import requests
import math

numero1 = "93"
rue1 = "rue bellecombe"
ville1 = "lyon"
numero2 = "40"
rue2 = "chemin du platon"
ville2 = "saint martin bellevue"


def getBornes(numero1, rue1, ville1, numero2, rue2, ville2):
            
            autonomie = 40
            listBornes = []
            url1 = "https://nominatim.openstreetmap.org/search?q="+str(numero1)+"+"+str(rue1)+"+"+str(ville1)+"&format=jsonv2"
            reponse1 = requests.get(url1)
            contenu1 = reponse1.json()
            print(url1)
            for element in contenu1:
                templat1 = element['lat']
                templon1 = element['lon']
                lat1 = float(templat1)
                lon1 = float(templon1)
                latrad1 = float(templat1)
                lonrad1 = float(templon1)
                print(lat1)
                print(lon1)
            url2 = "https://nominatim.openstreetmap.org/search?q="+str(numero2)+"+"+str(rue2)+"+"+str(ville2)+"&format=jsonv2"
            reponse2 = requests.get(url2)
            contenu2 = reponse2.json()
            print(url2)
            for element in contenu2:
                templat2 = element['lat']
                templon2 = element['lon']
                lat2 = float(templat2)
                lon2 = float(templon2)
                latrad2 = float(templat2)
                lonrad2 = float(templon2)
                print(lat2)
                print(lon2)
            lonrad1, latrad1, lonrad2, latrad2 = map(radians, [lonrad1, latrad1, lonrad2, latrad2])
            dlon = lonrad2 - lonrad1 
            dlat = latrad2 - latrad1 
            a = sin(dlat/2)**2 + cos(latrad1) * cos(latrad2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            # Radius of earth in kilometers is 6371
            km = 6371* c
            # calcul nb stops
            slot = math.ceil(km/autonomie)
            print(slot)
            # calcul coord bornes
            i = 1
            latBorne = lat1 + (abs(lat1-lat2)/km)*autonomie
            lonBorne = lon1 + (abs(lon1-lon2)/km)*autonomie
            listBornes.append([latBorne,lonBorne])
            while i < slot-1:
                latBorne = latBorne + (abs(latBorne-lat2)/(km-autonomie))*autonomie
                lonBorne = lonBorne + (abs(lonBorne-lon2)/(km-autonomie))*autonomie
                listBornes.append([latBorne,lonBorne])
                i = i+1
            print(listBornes)
            print(km)
            
            
getBornes(numero1, rue1, ville1, numero2, rue2, ville2)

# autonomie = 50
# km = 101.36
# lat = 45.7627736
# lon = 4.8639401

# lat2 = 45.9620684
# lon2 = 6.141314431283396

# latBorne = lat + (abs(lat-lat2)/km)*autonomie
# lonBorne = lon + (abs(lon-lon2)/km)*autonomie
# print(latBorne)
# print(lonBorne)



# listStops = [[45.841419229773294, 5.368017018916214], [45.920064859546585, 5.872093937832429]]

# listBornes = []
# rayon = 10000
# for stop in listStops:
#                 url = f"https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&rows=1&facet=region&geofilter.distance={stop[0]}%2C{stop[1]}%2C{rayon}"
#                 reponse = requests.get(url)
#                 contenu = reponse.json()
#                 lat = contenu['records'][0]['fields']['ylatitude']
#                 lon = contenu['records'][0]['fields']['xlongitude']
                
#                 listBornes.append([lat,lon])
                
# print(listBornes)


# def getCoordinate(numero, rue, ville):
#             url = "https://nominatim.openstreetmap.org/search?q="+str(numero)+"+"+str(rue)+"+"+str(ville)+"&format=jsonv2"
#             reponse = requests.get(url)
#             contenu = reponse.json()
#             print(url)
#             coord = []
#             for element in contenu:
#                 lat = element['lat']
#                 lon = element['lon']
#                 coord.append(lat)
#                 coord.append(lon)
#             print(coord[0])
# getCoordinate("40", "chemin du platon", "saint martin bellevue")
        
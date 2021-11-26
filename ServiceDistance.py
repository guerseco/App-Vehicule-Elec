from spyne import Application, rpc, ServiceBase, Unicode, Iterable, Integer, Float, String, Array, Double
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import  Soap11
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import requests
import math


class HelloWorldService(ServiceBase):

    
    @rpc(Integer, String, String, _returns=Iterable(Unicode))
    def getCoordinate(ctx, numero, rue, ville):
            url = "https://nominatim.openstreetmap.org/search?q="+str(numero)+"+"+str(rue)+"+"+str(ville)+"&format=jsonv2"
            reponse = requests.get(url)
            contenu = reponse.json()
            print(url)
            coord = []
            for element in contenu:
                lat = element['lat']
                lon = element['lon']
                coord.append(lat)
                coord.append(lon)

            return coord
                
    @rpc(Float, Float, Float, Float, _returns=Float)
    def haversine(ctx, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        # Radius of earth in kilometers is 6371
        km = 6371* c
        return km
    
    @rpc(Integer, String, String, Integer, String, String, _returns=Float)
    def getDistance(ctx, numero1, rue1, ville1, numero2, rue2, ville2):
            url1 = "https://nominatim.openstreetmap.org/search?q="+str(numero1)+"+"+str(rue1)+"+"+str(ville1)+"&format=jsonv2"
            reponse1 = requests.get(url1)
            contenu1 = reponse1.json()
            print(url1)
            for element in contenu1:
               templat1 = element['lat']
               templon1 = element['lon']
               lat1 = float(templat1)
               lon1 = float(templon1)
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
                print(lat2)
                print(lon2)
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            # Radius of earth in kilometers is 6371
            km = 6371* c
            return km
        
    @rpc(Integer, Integer, String, String, Integer, String, String, _returns=Array(Array(Float)))
    def getStops(ctx, autonomie, numero1, rue1, ville1, numero2, rue2, ville2):
            
            listStops = []
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
            latStop = lat1 + (abs(lat1-lat2)/km)*autonomie
            lonStop = lon1 + (abs(lon1-lon2)/km)*autonomie
            listStops.append([latStop,lonStop])
            while i < slot-1:
                latStop = latStop + (abs(latStop-lat2)/(km-autonomie))*autonomie
                lonStop = lonStop + (abs(lonStop-lon2)/(km-autonomie))*autonomie
                listStops.append([latStop,lonStop])
                i = i+1
            print(listStops)
                
                
            listBornes = []
            rayon = 30000
            for stop in listStops:
                url = f"https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&rows=1&facet=region&geofilter.distance={stop[0]}%2C{stop[1]}%2C{rayon}"
                reponse = requests.get(url)
                contenu = reponse.json()
                
                lat = contenu['records'][0]['fields']['ylatitude']
                lon = contenu['records'][0]['fields']['xlongitude']
                
                listBornes.append([lat,lon])
            
            return listBornes

            # return listStops
        
    # @rpc(Integer, Integer, Integer, Integer, _returns=Float)
    # def tempsTrajet(ctx, distance, autonomie, nbArrets, vMoy, tempsRecharge):
    #     temps = distance/vMoy + nbArrets*tempsRecharge
    #     return temps

    # def getBornes(self, listStops, rayon):
        
    #     listBornes = []
        
    #     for stop in listStops:
    #         url = f"https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&rows=1&facet=region&geofilter.distance={stop[0]}%2C{stop[1]}%2C{rayon}"
    #         reponse = requests.get(url)
    #         contenu = reponse.json()
            
    #         lat = reponse['records'][0]['fields']['ylatitude']
    #         lon = reponse['records'][0]['fields']['xlongitude']
            
    #         listBornes.append([lat,lon])
            
    #     return listBornes

            
application = Application([HelloWorldService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application) # server


from wsgiref.simple_server import make_server
server = make_server('127.0.0.1', 8000, wsgi_application)
server.serve_forever()
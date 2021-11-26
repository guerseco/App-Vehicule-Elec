from flask import Flask, render_template, request, redirect, url_for
from zeep import Client
import sqlite3
import folium
import requests

# i = 2
# result = 2
# tempsRecharge = 30

# url = f"http://127.0.0.1:5002/tempsTrajet/{result}/{i}/{tempsRecharge}"
# reponse = requests.get(url)
# temps = reponse.json()

# print(temps)

# list =  [{
#     'float': [
#         45.852516,
#         5.337319
#     ]
# }, {
#     'float': [
#         45.9569,
#         5.83438
#     ]
# }]

    
# list2 = []
# for i in list:
#     list2.append(i['float'])
    

test = {'result': 50.0}

print(test['result'])
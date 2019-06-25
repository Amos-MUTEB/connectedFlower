# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:42:34 2019

@author: amosm
"""

# import datetime, 


import requests # librairie, pouvoir interroger un serveur distant
import json # librairie, interpreter et format les données json

fichier = open("Bd_connectedFlower.txt","r")

identifiant= input("\nQuelle est votre identifiant: ")
password= input("\nEntrez votre mot de passe: ")
password_lenght = len(password)
if password_lenght < 8 :
   print("mot de passe trop court")
else:
   print("\n\t\t\t ---  Bienvenue Monsieur {}, sur connectedFlower ! --- \n\n".format(identifiant))

informations=[
        "securite",
        "1. Informations sur la plante",
        "2. Informations sur les capteurs",
        "3. Bilan de la plante"
        ]
print(informations[1])
print(informations[2])
print(informations[3])
choix = int(input("\nQuelles informations souhaitez-vous consulté : "))

# choix 1 inforamtion sur la plante
if (choix==1):
    tableauPlante= []
    for line in fichier:
        tableau = [line.replace('\n', '').split(";")]
        tableauPlante += tableau

    print(tableauPlante)
    choice = input("\n Taper le nom de la plante : ")
    plante = "aucune plante trouvée"
    for i in tableauPlante:
        if (i[0] == choice):
            plante = i
        #else:
         #   print("\n Aucune plante trouvée")
            #choice = input("\n Taper le nom de la plante : ")
    #print(choice)

    for valeur in plante:
        # plante= int ((plante[0]))   
        lumiere = float((plante[1]))
        humidite = float((plante[2]))
        temperature= float((plante[3]))
        humiditeS= float((plante[4]))

    final = temperature + humidite
    #print("le nom de la plante est : " , plante)
    print("\n\t\t\t Voici les informations de la plante : " , choice)
    print("\n- Lumiere maximale de la plante : " , lumiere, "lux")
    print("- Humidité maximal de la plante : " , humidite, "%")
    print("- Température ambiante maximale : " , temperature, "dégré")
    print("- Humidite du sol : " , humiditeS, "%")


    choi = int(input("\nTapez 0 pour revenir en arrière et 5 pour quitter: "))
    if choi== 0:
        print(informations[1])
        print(informations[2])
        print(informations[3])
        choix = int(input("\nQuelles informations souhaitez-vous consulté : "))
# informations sur les capteurs
        
elif choix ==2:
    url_api= "https://api.thinger.io/"
    parametre = "oauth/token"

    main_api = url_api + parametre

#informations de connexion à thinger.io
    mydata ={ "Content-Type": "application/x-www-form-urlencoded ",
        "grant_type" : "password",
        "username" : "Amos",
        "password" : "Planteconnecte"
        }

    objet_api= requests.post(main_api, data = mydata)
    json_data = objet_api.json()

    main_api = url_api + parametre
    parametre = "v1/users/Amos/devices?authorization=" + json_data["access_token"]
    main_api =  url_api + parametre

    print(requests.get(main_api).json()) # vérifie si il y a une connexion établie entre l'API arduino et le serveur thinger.io

    # récuperation de la valeur de la température sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/Température?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    temperature = (object_api.json())

    # récuperation de la valeur de la lumière sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/lux?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    light = (object_api.json())
    
    # récuperation de la valeur de l'humidité sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/Humidité_ambiante?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    humidity = (object_api.json())

    # récuperation de la valeur de l'humidité du sol sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/Humidite_du_sol?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    soil_moisture = (object_api.json())

    # stockage des valeurs prisent sur arduino
    capteur = {
        "lumiere": light['out'],
        "temperature" : temperature ['out'],
        "humidite_ambiante": humidity ['out'],
        "humidite_du_sol" : soil_moisture ['out']
        }

    # affichage des valeurs de capteurs
    print ("Lumiere optimale : " , capteur["lumiere"])
    print ("Température ambiante : " , capteur["temperature"])
    print ("Humidité ambiante : " , capteur["humidite_ambiante"])
    print ("Humidité du sol  : " , capteur["humidite_du_sol"])
    
    choix = input("\nTapez 0 pour revenir en arrière et 5 pour quitter:  ")

elif choix ==3:
    print ("\nl'Amour de Dieu est immense")
else:
    print("\nVeuillez choisir une option !!! \n")
    print(informations[1])
    print(informations[2])
    print(informations[3])
    choix = int(input("\nQuelles informations souhaitez-vous consulté : "))


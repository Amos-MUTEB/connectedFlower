# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:42:34 2019

@author: amosm
"""

# import datetime, 
import requests # librairie, pouvoir interroger un serveur distant
import json # librairie, interpreter et format les données json

# ouverture de la base de donnée 
fichier = open("Bd_connectedFlower.txt","r")

# authentification afin de voir les ressources 
identifiant= input("\nQuelle est votre identifiant: ")
motdepasse= input("\nEntrez votre mot de passe: ")
motdepasse_poid = len(motdepasse)
if motdepasse_poid < 8 :
   print("mot de passe trop court") # condition de sécurité
else:
   print("\n\t\t\t ---  Bienvenue Monsieur {}, sur connectedFlower ! --- \n\n".format(identifiant))

# 1er tableau d'affichage 
informations=[
        "securite",
        "1. Informations sur la plante",
        "2. Informations sur les capteurs",
        "3. Bilan de la plante"
        ]
print(informations[1]) # affiche la ligne 1 du tableau
print(informations[2]) # affiche la ligne 2 du tableau
print(informations[3]) # affiche la ligne 3 du tableau
choix = int(input("\nQuelles informations souhaitez-vous consulté : ")) # transforme le choix de l'utilisateur en un entier

# choix 1 information sur la plante
if (choix==1): # le choix de l'utilisateur à la valeur 1
    tableauPlante= [] # creer un tableau
    for line in fichier: 
        tableau = [line.replace('\n', '').split(";")]
        tableauPlante += tableau 

    print(tableauPlante) # affiche les plantes disponible dans la base de donée
    choix2 = input("\n Taper le nom de la plante : ") # demande à l'utilisateur son de choix de plante
    plante = "aucune plante trouvée"
    for i in tableauPlante:
        if (i[0] == choix2):
            plante = i

    for valeur in plante:
        lumiere = float((plante[1])) # transforme les valeurs du capteur de lumière en décimale
        humidite = float((plante[2])) # transforme les valeurs du capteur d'humidité ambiante en décimale
        temperature= float((plante[3])) # transforme les valeurs du capteur de temperature en décimale
        humiditeS= float((plante[4])) # transforme les valeurs du capteur d'humidité en décimale

    # affiche les informations de la base de donnée
    print("\n\t\t\t Voici les informations de la plante : " , choix2)
    print("\n- Lumiere maximale de la plante : " , lumiere, "lux")
    print("- Humidité maximal de la plante : " , humidite, "%")
    print("- Température ambiante maximale : " , temperature, "dégré")
    print("- Humidite du sol : " , humiditeS, "%")

# condition sécuritaire 
    choi = int(input("\nTapez 0 pour revenir en arrière et 5 pour quitter: "))
    if choi== 0:
        print(informations[1])
        print(informations[2])
        print(informations[3])
        choix = int(input("\nQuelles informations souhaitez-vous consulté : "))
        
# choix 2 informations sur les capteurs
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
    temperature = (object_api.json()) # recupère la valeur de la température sur le serveur et la stock dans la variable temperature

    # récuperation de la valeur de la lumière sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/lux?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    lumiere1 = (object_api.json()) # recupère la valeur de la lumière sur le serveur et la stock dans la variable lumiere1
    
    # récuperation de la valeur de l'humidité sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/Humidité_ambiante?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    humidite = (object_api.json()) # recupère la valeur de la humidite sur le serveur et la stock dans la variable humidite

    # récuperation de la valeur de l'humidité du sol sur le serveur thinger.io
    parametre ="v2/users/Amos/devices/Amosmuteb/Humidite_du_sol?authorization="+ json_data["access_token"]
    tab = []
    main_api =url_api + parametre
    object_api = requests.get(main_api)
    sol_humidite = (object_api.json()) # recupère la valeur de la humidite du sol sur le serveur et la stock dans la variable sol_humidite

    # stockage des valeurs prisent sur arduino
    capteur = {
        "lumiere": lumiere1['out'],
        "temperature" : temperature ['out'],
        "humidite_ambiante": humidite ['out'],
        "humidite_du_sol" : sol_humidite ['out']
        }

    # affichage des valeurs de capteurs
    print ("Lumiere optimale : " , capteur["lumiere"]) 
    print ("Température ambiante : " , capteur["temperature"])
    print ("Humidité ambiante : " , capteur["humidite_ambiante"])
    print ("Humidité du sol  : " , capteur["humidite_du_sol"])
    
    choix = input("\nTapez 0 pour revenir en arrière et 5 pour quitter:  ")
    
 # choix 3 possibilité de melanger les deux informations et de pouvoir les traiters
elif choix ==3:
    print ("\nl'Amour de Dieu est immense")

else:
    print("\nVeuillez choisir une option !!! \n")
    print(informations[1])
    print(informations[2])
    print(informations[3])
    choix = int(input("\nQuelles informations souhaitez-vous consulté : "))


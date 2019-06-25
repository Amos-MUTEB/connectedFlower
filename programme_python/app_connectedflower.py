# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:56:59 2019

@author: amosm
"""
from tkinter import *
import webbrowser

def open_thinger():
    webbrowser.open_new("https://console.thinger.io/#/console/dashboard/Projet")
# creer une première fenetre
window = Tk()

# personnaliser cette fenêtre
window.title("Connected Flower")
window.geometry("800x500")
window.minsize(480, 360)
window.config(background='#41B77F')
window.iconbitmap ("logo.ico")   
#creer la frame
frame=Frame(window, bg='#41B77F')
#ajouter un premier texte
label_title= Label(frame, text="Bienvenue sur Connected Flower", font=("courrier",40), bg = '#41B77F', fg = 'white')
label_title.pack()

#ajouter un second texte
label_subtitle= Label(frame, text="votre application pour une plante intelligente", font=("courrier",26), bg = '#41B77F', fg = 'white')
label_subtitle.pack()

# ajouter un premier bouton
yt_button=Button(frame, text="s'authentifier", font=("courrier", 26), bg='white', fg='#41B77F', command=open_thinger)
yt_button.pack()

#ajouter
frame.pack(expand=YES)

# afficher
window.mainloop()


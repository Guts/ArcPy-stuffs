# -*- coding: cp1252 -*-
#-------------------------------------------------------------------------------
# Name:        FrequExcel
# Purpose:     Calcule le nombre d'occurences des données d'un attribut d'un shape
#               et inscrit les fréquences dans un fichier excel
# Author:      Julien M.
# Created:     22/11/2011
# Copyright:   (c) IRD 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#######  Import des modules
from Tkinter import *
from tkFileDialog import askopenfilename as ficible
from tkFileDialog import asksaveasfilename as savefic
from tkMessageBox import showinfo as info
import Pmw

from os import path
from sys import exit

from arcpy import SearchCursor as curs
from arcpy import ListFields as lister_champs

import xlwt

#######  Définition des fonctions
def valider():
    "Retourne le champ choisi et le nom du shape"
    global chp_cible, shp
    chp_cible = choix_champ.get()
    return chp_cible, shp

def annuler():
    "Quitte le programme"
    fen.destroy()
    exit()

###### Variables basiques
liste_chps = []
chp_cible = ""
dico_occurences = {}
###### Programme principal
fen = Tk()
fen.withdraw()
fen.title("FrequExcel")
shp = ficible(filetypes = [("Shapefiles","*.shp")])
for field in lister_champs(shp):
    liste_chps.append(field.name)
choix_champ = Pmw.ComboBox(fen, labelpos = NW,
                     label_text = "Choisir le champ : ",
                     scrolledlist_items = liste_chps,
                     listheight = 150,)
choix_champ.pack()
Button(fen, text="Calculer", command=valider).pack()
Button(fen, text="Annuler", command=annuler).pack()
fen.mainloop()

###### Calcul des fréquences
print "Calcul des fréquences"
rows = curs(shp, "", "", chp_cible, "")
for j in rows:
    if dico_occurences.has_key(j.getValue(chp_cible)):
        dico_occurences[j.getValue(chp_cible)] = dico_occurences.get(j.getValue(chp_cible))+1
    else:
        dico_occurences[j.getValue(chp_cible)] = 1

##### Création du fichier excel
print "Création et configuration du fichier excel"
book = xlwt.Workbook(encoding = 'Latin-1')
feuy1 = book.add_sheet('Frequences', cell_overwrite_ok=True)

font1 = xlwt.Font()             # création police 1
font1.name = 'Times New Roman'
font1.bold = True
entete = xlwt.XFStyle()         # création style pour les en-têtes
entete.font = font1

# Intitulés
feuy1.write(0,0,chp_cible, entete)
feuy1.write(0,1,'Occurences', entete)

###### Inscription dans un fichier excel
print "Inscription des fréquences dans le fichier excel"
x, y = 0, 0
for clef, valeur in dico_occurences.items():
    feuy1.write(x+1,y, clef)
    feuy1.write(x+1,y+1, valeur)
    x = x+1

##### Sauvegarde du fichier excel
cible = savefic(filetypes=[("Classeurs Excel","*.xls")])
if path.splitext(cible)[1] != ".xls":
    cible = cible + ".xls"
book.save(cible)
info(title="Operation terminee.", message="Calcul termine. Fichier excel sauvegarde . " + cible)
annuler()
# -*- coding: cp1252 -*-
#-------------------------------------------------------------------------------
# Name:        coding_mallas
# Purpose:     Code les mailles présence / absence avec les lettres
#              correspondantes à chaque thème. Calcule aussi quelques stats
#              et les consignes dans un fichier excel.
# Author:      Julien
# Created:     19/10/2011
# Updated :    20/02/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python


### Importation des modules nécessaires
from arcpy import AddField_management as new_champ
from arcpy import DeleteField_management as del_champ
from arcpy import CalculateField_management as calc_champ
from arcpy import ListFields as lister_champs
from arcpy import DeleteField_management as del_champ
from arcpy import MakeFeatureLayer_management as trans_lyr
from arcpy import SelectLayerByAttribute_management as sel_attr
from arcpy import GetCount_management as count_obj
from arcpy import SearchCursor as curs

from Tkinter import *
import xlwt
from sys import exit as EXIT


### Fonctions locales
def creat_prov(li_chps):
    '''Crée les champs provisoires'''
    print "Création des champs provisoires"
    global provis
    for chps in li_chps:
        chps_code = chps[0:3] + chps[-2:] + '_code'
        new_champ(mailles, chps_code, 'TEXT', 1)
        provis.append(chps_code)


def eff_prov(li_chps):
    '''Efface les champs provisoires'''
    print "Suppression des champs provisoires"
    for chps in li_chps:
        del_champ(mailles,chps)

### Couche cible
mailles = r'C:\Documents and Settings\Utilisateur\Mes documents\GIS DataBase\LE_hexa_tipo_aglo49D_2.shp'
print "Transformation du shape en .lyr"
lyr = trans_lyr(mailles)

### Fichier excel
print "Création et configuration du fichier excel"
book = xlwt.Workbook(encoding = 'Latin-1')
feuy1 = book.add_sheet('Global', cell_overwrite_ok=True)
feuy2 = book.add_sheet('Esenciales', cell_overwrite_ok=True)
feuy3 = book.add_sheet('Frequences', cell_overwrite_ok=True)
font1 = xlwt.Font()             # création police 1
font1.name = 'Times New Roman'
font1.bold = True

entete = xlwt.XFStyle()         # création style pour les en-têtes
entete.font = font1

# Intitulé
feuy1.write(0,0,'Total',entete)
feuy1.write(1,0,'Tot E = 0',entete)
feuy1.write(2,0,'Tot E = 1',entete)
feuy1.write(3,0,'Tot E = 2',entete)
feuy1.write(4,0,'Tot E = 3',entete)
feuy1.write(5,0,'Tot E = 4',entete)
feuy1.write(6,0,'Tot E = 5',entete)

feuy2.write(0,0,'Thème', entete)
feuy2.write(0,1,'Code', entete)
feuy2.write(0,2,'Total', entete)
feuy2.write(0,3,'Tot E = 1', entete)
feuy2.write(0,4,'Tot E = 2', entete)
feuy2.write(0,5,'Tot E = 3', entete)
feuy2.write(0,6,'Tot E = 4', entete)
feuy2.write(0,7,'Tot E = 5', entete)

feuy3.write(0,0,'Code', entete)
feuy3.write(0,1,'Occurences', entete)

# Largeur des colonnes
feuy1.col(0).width = 5000
feuy1.col(1).width = 5000
feuy2.col(0).width = 10000
feuy2.col(1).width = 5000
feuy2.col(2).width = 3000

### Création  des listes des champs : Esenciales, Apoyo et Esenciales e Apoyo
print "Création des listes python pour les champs"
chps_E = []        # liste des champs esenciales
chps_A = []        # liste des champs apoyo
chps_EA = []        # liste des champs esenciales e apoyo
provis = []        # liste des champs provisoires
code = ["A", "L", "E", "S", "T", "C", "D", "R", "B"]    # liste des codes


### Listing des champs de la couche cible à l'aide de l'outil arcgis
print "Listing des champs avec ArcGIS"
champs = lister_champs(mailles)

### Remplissage des listes de champs
for field in champs:
    if field.name[-1] == 'E' and field.name[0:3] != "Tot":
        chps_E.append(field.name)
    elif field.name[-1] == 'A' and field.name[-2] != 'E':
        chps_A.append(field.name)
    elif field.name[-2:] == 'EA':
        chps_EA.append(field.name)

# fonction de création des champs provisoires selon liste des champs
creat_prov(chps_E)

dico = {}
concac = ''

# remplissage du dictionnaire esenciales
x = 0
for i in chps_E:
    dico[i] = provis[x], code[x]
    x = x+1

# sélection des champs selon présence/absence et maj du champ
print "Sélection et mise à jour des champs selon les thèmes"
sel_attr(lyr,"CLEAR_SELECTION")
j = 1
for chp in dico:
    j = j+1
    expression = chp + "=1"
    expression2 = "'" + dico[chp][1] + "'"
    sel = sel_attr(lyr, "NEW_SELECTION", expression)
    nbr = count_obj(sel)
    feuy2.write(j, 0, chp)
    feuy2.write(j, 1, dico[chp][1])
    feuy2.write(j, 2, str(nbr))
    print "Nbr de mailles du champ " + expression + " : OK."
    calc_champ(sel, dico[chp][0] ,expression2, "PYTHON")
    concac = concac + "+" + "!" + dico[chp][0] + "!"

sel_attr(lyr,"CLEAR_SELECTION")


# concaténation dans le champ code
print "Concaténation des champs provisoires codes"
concac = concac[1:]
tipo =  dico[chp][1] + "_code"
new_champ(mailles, tipo , 'TEXT', 6)

# suppression des espaces
print "Suppression des espaces"
calc_champ(mailles, tipo , concac, "PYTHON")
tipo2 = "!" + tipo + "!.replace(' ','')"
calc_champ(mailles, tipo , tipo2, "PYTHON")

# Stats rapides
sel_attr(lyr,"CLEAR_SELECTION")

lig = 1
col = 2
while lig < 6:
    sel_attr(lyr,"CLEAR_SELECTION")
    expression = "Tot_E = " + str(lig)
    tot = sel_attr(lyr, "NEW_SELECTION", expression)
    feuy1.write(lig+1,1,str(count_obj(tot)))
    print "Comptage du nombre d'objets selon " + expression
    lig2 = 2
    col = col+1
    for chp in dico:
        expression2 = expression + " And " + chp + " = 1"
        them = sel_attr(lyr, "NEW_SELECTION", expression2)
        feuy2.write(lig2, col, str(count_obj(them)))
        lig2 = lig2+1
    lig = lig+1



print "Calcul des fréquences"
rows = curs(mailles, "Tot_E > 0", "")
dixou = {}
for j in rows:
    if dixou.has_key(j.E_code):
        dixou[j.E_code] = dixou.get(j.E_code)+1
    else:
        dixou[j.E_code] = 1

print "Inscription des fréquences dans le fichier excel"
x, y = 0, 0

for clef, valeur in dixou.items():
    feuy3.write(x+1,y, clef)
    feuy3.write(x+1,y+1, valeur)
    x = x+1


# fin de script : fermeture, sauvegarde et suppression
eff_prov(provis)
print "Enregistrement du fichier excel."
book.save(r'D:\A_Ordenar\Julien\tratamientos\mallas\result_coding_mallas.xls')
'''del champs, chps_A, chps_E, chps_EA , code, concac, dico, expression , expression2, lyr, mailles, sel, tipo, tipo2, x'''
print "Fin du script"
EXIT()
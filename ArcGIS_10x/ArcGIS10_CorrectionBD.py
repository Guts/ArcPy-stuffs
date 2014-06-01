# -*- coding: cp1252 -*-
#--------------------------------
# Nom:         Correction BD.py
# Objectif:    listes les dossiers, shapes et mxd dans une base de
#              données, stocke différentes informations, renomme selon les
#              normes informatiques et corrige les sources le cas échéant.
# Auteur:      Julien Moura
# Cr?e le :    12/04/2012
# Last update: 12/04/2012
# Python Version:  2.6.5
#--------------------------------
#!/usr/bin/env python

###################################
##### Import des librairies #######
###################################

from os import walk, path
from time import localtime
from xlwt import Workbook, Font, XFStyle, easyxf, Formula

###################################
###### Définition fonctions #######
###################################



###################################
########### Variables #############
###################################

chemin_BD = r'D:\A_Ordenar\Julien\tratamientos\4. ATENCIÓN MÉDICA'


liste_shapes = []         # liste des chemins des shapes
dico_err = {}             # liste des erreurs

today = unicode(localtime()[0]) + u"-" +\
        unicode(localtime()[1]) + u"-" +\
        unicode(localtime()[2])    # date du jour

###################################
######### Fichier Excel ###########
###################################
# configuration du fichier excel de sortie
book = Workbook(encoding = 'utf8')
feuy1 = book.add_sheet(u'Dossiers', cell_overwrite_ok=True)
feuy2 = book.add_sheet(u'Shapes', cell_overwrite_ok=True)
feuy3 = book.add_sheet(u'Champs', cell_overwrite_ok=True)
feuy4 = book.add_sheet(u'MXD', cell_overwrite_ok=True)
feuy5 = book.add_sheet(u'Metadatos', cell_overwrite_ok=True)

# personnalisation du fichier excel
font1 = Font()             # cr?ation police 1
font1.name = 'Times New Roman'
font1.bold = True

entete = XFStyle()         # cr?ation style pour les en-t?tes
entete.font = font1             # application de la police 1 au style entete
hyperlien = easyxf(u'font: underline single')
erreur = easyxf(u'font: name Arial, bold 1, colour red')

# colonnes feuille dossiers
feuy1.write(0, 0, u'Nom actuel', entete)
feuy1.write(0, 1, u'Nom chang?', entete)
feuy1.write(0, 2, u'Type g?om?trie', entete)
feuy1.write(0, 3, u'Emprise', entete)
feuy1.write(0, 4, u'Projection', entete)
feuy1.write(0, 5, u'EPSG', entete)
feuy1.write(0, 6, u'Nombre de champs', entete)
feuy1.write(0, 7, u'Nombre d\'objets', entete)
feuy1.write(0, 8, u'Ann?e de l\'information', entete)
feuy1.write(0, 9, u'Date derni?re actualisation', entete)
feuy1.write(0, 10, u'Liste des champs', entete)

###################################################
############## Programme principal ################
###################################################


# Listing des dossiers, shapes, mxd et metadatos
for root, dirs, files in walk(chemin_BD):
    for i in files:
        if path.splitext(path.join(root, i))[1] == u'.shp' and \
            path.isfile(path.join(root, i)[:-4] + u'.dbf') and \
            path.isfile(path.join(root, i)[:-4] + u'.shx'):
            liste_shapes.append(path.join(root, i))






## Sauvegarde du fichier excel

book.save(r'D:\A_Ordenar\Julien\tratamientos\BaseDonnees_Bilan.xls')


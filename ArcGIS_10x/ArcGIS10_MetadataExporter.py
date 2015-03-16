# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# --------------------------------
# Nom:        ArcCatalog2iso19139.py
# Objectif:   get the metadata from ArcCatalog and export it to ISO 19139.
# Auteur:     Julien Moura
# Crée le :   06/03/2015
# ArcGIS Version:  10.2.x
# Python Version:  2.7.x
# --------------------------------

# Help reference: http://resources.arcgis.com/fr/help/main/10.2/index.html#//00120000000t000000

###################################
##### Import des librairies #######
###################################

from os import walk, path
from arcpy import Describe as get_info
from arcpy import ListFields as lister_champs
from arcpy import GetCount_management as count_obj
from xlwt import Workbook, Font, XFStyle, easyxf, Formula
from Tkinter import Tk
from tkFileDialog import askdirectory as doss_cible
from tkFileDialog import asksaveasfilename as savefic
from tkMessageBox import showinfo as info


###################################
###### Définition fonctions #######
###################################
def listchemshapes(chemin):
    ''' Inscrit les chemins des shapes d'un répertoire donné (path)
     et de ses sous-répertoires dans liste_fichiers '''
    global liste_shapes
    liste_shapes = []
    for racine, dossier, fichiers in walk(chemin):
        for fic in fichiers:
            if path.splitext(fic)[1] == '.shp':
                shp = path.join(racine, fic)
                liste_shapes.append(shp.encode("utf-8"))
###################################
######### Fichier Excel ###########
###################################

# configuration du fichier excel de sortie
book = Workbook(encoding = 'Latin-1')
feuy1 = book.add_sheet('Shapes', cell_overwrite_ok=True)

# personnalisation du fichier excel
font1 = Font()             # création police 1
font1.name = 'Times New Roman'
font1.bold = True

entete = XFStyle()         # création style pour les en-têtes
entete.font = font1             # application de la police 1 au style entete
hyperlien = easyxf('font: underline single')


# titre des colonnes
feuy1.write(0, 0, 'Nom fichier', entete)
feuy1.write(0, 1, 'Chemin', entete)
feuy1.write(0, 2, 'Type', entete)
feuy1.write(0, 3, 'Index spatial (V/F)', entete)
feuy1.write(0, 4, 'Emprise', entete)
feuy1.write(0, 5, 'Projection', entete)
feuy1.write(0, 6, 'EPSG', entete)
feuy1.write(0, 7, 'Nombre de champs', entete)
feuy1.write(0, 8, 'Nombre d\'objets', entete)
feuy1.write(0, 9, 'Polyligne (V/F)', entete)
feuy1.write(0, 10, '3D (V/F)', entete)
feuy1.write(0, 11, 'Liste des champs', entete)

###################################################
############## Programme principal ################

import arcpy
from arcpy import env
env.workspace = "C:/data"

#set local variables
dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = dir + "Metadata/Translator/ESRI_ISO2ISO19139.xml"
arcpy.ESRITranslator_conversion("locations.shp", translator,
                                "locations_19139.xml", "locations_19139.txt")

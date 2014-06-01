# -*- coding: cp1252 -*-
#--------------------------------
# Nom:        dicoshapes.py
# Objectif:   dresse la liste des shapes présents dans un dossier et ses sous-dossiers ;
#             extrait les informations sur les shapes trouvés ;
#             construit un fichier excel avec les informations.
# Auteur:     Julien Moura
# Crée le :   06/10/2011
# Copyright:  (c) IRD
# ArcGIS Version:  10.0 (SP3)
# Python Version:  2.6.5
#--------------------------------
#!/usr/bin/env python

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
###################################################
# dossier à explorer
root = Tk()
root.withdraw()
cible = doss_cible()
# appel de la fonction pour lister les shapes
listchemshapes(cible)
# lecture des shapes trouvés
lig = 1
l_err = []
for shape in liste_shapes:
    champs = ""
    nbr_chps = 0
    try:
        desc = get_info(shape)    # objet de description d'arcpy
        feuy1.write(lig, 0, desc.basename)    # nom du shape (sans l'extension)
        lien = 'HYPERLINK("' + desc.path + '"; "Atteindre le dossier")'    # chemin du dossier contenant formaté pour être un lien
        feuy1.write(lig, 1, Formula(lien), hyperlien)
        feuy1.write(lig, 2, desc.shapeType)    # type de la géométrie
        feuy1.write(lig, 3, desc.hasSpatialIndex)    # indique si le shape possède un index spatial
        emprise = "Xmin : " + unicode(desc.extent.XMin) + ", Xmax : " + unicode(desc.extent.XMax) + ", Ymin : " + unicode(desc.extent.YMin) + ", Ymax : " + unicode(desc.extent.YMax)        # Extrait les bornes de l'emprise
        feuy1.write(lig, 4, emprise)
        feuy1.write(lig, 5, desc.spatialReference.name)    # Nom de la projection
        feuy1.write(lig, 6, desc.spatialReference.factoryCode)    # Code EPSG de la projection
        for chp in desc.fields:    # parcourt les champs du shape
            champs = champs + chp.name + " (" + chp.type + ", Lg. = " + unicode(chp.length) + ", Pr. = " + unicode(chp.precision) + "), "    # extrait quelques données sur chaque champ
            nbr_chps = nbr_chps +1    # compte le nombre de champs
        feuy1.write(lig, 7, nbr_chps)
        feuy1.write(lig, 11, champs)
        feuy1.write(lig, 8, int(str(count_obj(shape))))    # compte le nombre d'objets
        feuy1.write(lig, 9, desc.hasM)    # indique si le shape possède un
        feuy1.write(lig, 10, desc.hasZ)    # indique si le shape possède des données d'altitude
    except:    # gestion des erreurs
        l_err.append(shape)    # liste des shapes qui renvoient des erreurs
        feuy1.write(lig, 0, desc.basename)
        lien = 'HYPERLINK("' + desc.path + '"; "Atteindre le dossier")'    # chemin du dossier contenant formaté pour être un lien
        feuy1.write(lig, 1, Formula(lien), hyperlien)
        feuy1.write(lig, 2, "ERREUR", entete)
    lig = lig +1


## Sauvegarde du fichier excel
saved = savefic(initialdir= cible, filetypes=[("Classeurs Excel","*.xls")])
if path.splitext(saved)[1] != ".xls":
    saved = saved + ".xls"
book.save(saved)

## Bilan programme
if l_err == []:    # s'il n'y a pas d'erreur
    info(title=u"Fin de programme", message=u"Programme terminé.\nAucune erreur rencontrée.")
else:    # s'il y a des erreurs, création d'un fichier log
    from datetime import date
    fic = open(cible + "\\" + str(date.today()) + "_dico-shapes_log.txt", 'w')
    fic.write("Erreurs rencontrées sur les shapes suivants : \n\n")
    for i in l_err:
        fic.write(i.encode("utf-8"))
        fic.write("\n-------------------------\n")
    fic.close()
    info(title=u"Fin de programme", message=u"Programme terminé.\n" + unicode(len(l_err)) + u" erreur(s) rencontrée(s).\n Consultez le fichier log créé pour les détails : \n" + cible + "\\" + unicode(date.today()) + u"_dico-shapes_log.txt")

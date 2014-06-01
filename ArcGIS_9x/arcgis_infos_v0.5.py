# -*- coding: utf-8 -*-

#--------------------------------
# Nom:        dicoshapes.py
# Objectif:   dresse la liste des shapes présents dans un dossier et ses sous-dossiers ;
#           extrait les informations sur les shapes trouvés ;
#           construit un fichier excel avec les informations.
# Auteur:    Julien Moura
# Crée le    06/10/2011
# Copyright:  (c) IRD
# ArcGIS Version:  9.3
# Python Version:  2.5
#--------------------------------

###################################
##### Import des librairies #######
###################################

from os import walk, getcwd, path, chdir
from arcgisscripting import create
from xlwt import Workbook, Font, XFStyle
from Tkinter import Tk as fen
from tkFileDialog import askdirectory as parcourdoss

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
                liste_shapes.append(path.join(racine, fic))
    return liste_shapes

def infogis(chemin):
    '''récupération des informations des shapes avec les outils arcgis'''
    global listinfo
    listinfo = []
    nomch = []
    typech = []
    longch = []
    echellech = []
    precch = []
    nbrch = 0
    desc = gp.Describe(chemin)
    listinfo.append(desc.Basename)
    listinfo.append(desc.CatalogPath)
    listinfo.append(desc.DataType)
    listinfo.append(desc.DatasetType)
    listinfo.append(desc.ShapeType)
    listinfo.append(desc.ShapeFieldName)
    listinfo.append(desc.HasM)
    listinfo.append(desc.HasZ)
    listinfo.append(desc.HasSpatialIndex)
    listinfo.append(str(desc.Extent))
    listinfo.append(desc.SpatialReference.Name)
    listinfo.append(desc.SpatialReference.PCSCode)
    champs = gp.ListFields(chemin)
    for i in champs:
        nomch.append(str(i.Name))
        typech.append(str(i.Type))
        longch.append(str(i.Length))
        echellech.append(str(i.Scale))
        precch.append(str(i.Precision))
        nbrch = nbrch +1
    listinfo.append(nbrch)
    listinfo.append(str(nomch))
    listinfo.append(str(typech))
    listinfo.append(str(longch))
    listinfo.append(str(echellech))
    listinfo.append(str(precch))
    return listinfo

def xlcrir(liste,lig):
    '''écriture en boucle du fichier excel'''
    col = 0
    for i in liste:
        feuy1.write(lig,col,liste[col])
        col = col +1
    
###################################
######### Fichier Excel ###########
###################################

# configuration du fichier excel de sortie
book = Workbook(encoding = 'Latin-1')
feuy1 = book.add_sheet('Shapes', cell_overwrite_ok=True)

lig = 1

# personnalisation du fichier excel
font1 = Font()             # création police 1
font1.name = 'Times New Roman'
font1.bold = True

entete = XFStyle()         # création style pour les en-têtes
entete.font = font1             # application de la police 1 au style entete


# titre des colonnes
feuy1.write(0,0,'Nom fichier', entete)
feuy1.write(0,1,'Chemin', entete)
feuy1.write(0,2,'Format', entete)
feuy1.write(0,3,'Type du jeu de données', entete)
feuy1.write(0,4,'Géométrie', entete)
feuy1.write(0,5,'Nom du champ de la géométrie', entete)
feuy1.write(0,6,'Polyligne (T/F)', entete)
feuy1.write(0,7,'3D (T/F)', entete)
feuy1.write(0,8,'Index spatial (T/F)', entete)
feuy1.write(0,9,'Emprise', entete)
feuy1.write(0,10,'Projection', entete)
feuy1.write(0,11,'EPSG', entete)
feuy1.write(0,12,'Nombre de champs', entete)
feuy1.write(0,13,'Liste des champs', entete)
feuy1.write(0,14,'Type des champs', entete)
feuy1.write(0,15,'Longueur des champs', entete)
feuy1.write(0,16,'Echelle des champs', entete)
feuy1.write(0,17,'Précision des champs', entete)


###################################
###### Outil de géotraitement #####
###################################

gp = create(9.3)



###################################################
############## Programme principal ################
###################################################

# dossier à explorer
root = fen()
root.withdraw()
cible = parcourdoss()
cible = str(cible)

listchemshapes(cible)

for shape in liste_shapes:
    infogis(shape)
    xlcrir(listinfo,lig)
    lig = lig +1

chdir(cible)
book.save('Listing_shapes.xls')
print "Terminé."
print "Done.\nLe fichier excel se nomme Listing_shapes et se trouve dans : ", cible

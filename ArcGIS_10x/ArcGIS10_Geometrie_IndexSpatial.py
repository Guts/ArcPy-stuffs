#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     20/07/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from arcpy import *
from os import path, walk

cible = r'C:\Documents and Settings\Utilisateur\Bureau\Sin_metadatos\Vincent\Uso de suelo'

def listing_shp(cible):
    u"""Liste les shapes contenus dans un répertoire et ses sous-répertoires"""
    global liste_shp
    for root, dirs, files in walk(cible):
        for i in files:
            if path.splitext(path.join(root, i))[1] == u'.shp' and \
            path.isfile(path.join(root, i)[:-4] + u'.dbf') and \
            path.isfile(path.join(root, i)[:-4] + u'.shx') and \
            path.isfile(path.join(root, i)[:-4] + u'.prj'):
                liste_shp.append(path.join(root, i))
    # Fin de fonction
    return liste_shp

# Environnement de travail
env.workspace = cible
# liste des shapes de l'arborescence
liste_shp = []
listing_shp(cible)


for shp in liste_shp:
    print shp
    RepairGeometry_management(shp)
    print u"shp réparé"
    AddSpatialIndex_management(shp)
    print u"Index spatial ajouté"
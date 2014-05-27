# -*- coding: cp1252 -*-
# import des modules usuels
import os, arcgisscripting, xlwt

# création de l'objet de géotraitement
gp = arcgisscripting.create(9.3)

# 
feat = raw_input("Chemin du shape : ")

# Décrire l'objet
desc = gp.Describe(feat)

print "Nom fichier : ", desc.Basename
print "Chemin : ", desc.CatalogPath
print "Format : ", desc.DataType
print "Type du jeu de données : ", desc.DatasetType
'''print "Extension : ", desc.Extension'''
print "Géométrie : ", desc.ShapeType
print "Nom du champ de la géométrie : ", desc.ShapeFieldName
print "Polyligne : ", desc.HasM
print "3D : ", desc.HasZ
print "Index spatial : ", desc.HasSpatialIndex
print "Emprise : ", desc.Extent
print "Projection : ", desc.SpatialReference.Name, " (EPSG : ", desc.SpatialReference.PCSCode, ")"

# Lister les champs
print "\nListe détaillée des champs : "
listcp = gp.ListFields(feat)

for champ in listcp:
    print "\nNom : ",champ.Name
    print "\tType : ", champ.Type
    print "\tLongueur : ", champ.Length
    print "\tEchelle : ", str(champ.Scale)
    print "\tPrécision : ", str(champ.Precision)

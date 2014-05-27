# -*- coding: cp1252 -*-
# import des modules usuels
import os, arcgisscripting, xlwt

# cr�ation de l'objet de g�otraitement
gp = arcgisscripting.create(9.3)

# 
feat = raw_input("Chemin du shape : ")

# D�crire l'objet
desc = gp.Describe(feat)

print "Nom fichier : ", desc.Basename
print "Chemin : ", desc.CatalogPath
print "Format : ", desc.DataType
print "Type du jeu de donn�es : ", desc.DatasetType
'''print "Extension : ", desc.Extension'''
print "G�om�trie : ", desc.ShapeType
print "Nom du champ de la g�om�trie : ", desc.ShapeFieldName
print "Polyligne : ", desc.HasM
print "3D : ", desc.HasZ
print "Index spatial : ", desc.HasSpatialIndex
print "Emprise : ", desc.Extent
print "Projection : ", desc.SpatialReference.Name, " (EPSG : ", desc.SpatialReference.PCSCode, ")"

# Lister les champs
print "\nListe d�taill�e des champs : "
listcp = gp.ListFields(feat)

for champ in listcp:
    print "\nNom : ",champ.Name
    print "\tType : ", champ.Type
    print "\tLongueur : ", champ.Length
    print "\tEchelle : ", str(champ.Scale)
    print "\tPr�cision : ", str(champ.Precision)

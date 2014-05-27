#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     24/01/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# Name: CalculateField_Centroids.py
# Description: Use CalculateField to assign centroid values to new fields


#### Import  modules
from arcpy import env
from arcpy import GetParameterAsText
from arcpy import CreateFeatureclass_management as new_shp
from arcpy import SearchCursor as curs_rec
from arcpy import InsertCursor as curs_ins
from arcpy import AddField_management as new_chp
from arcpy import CalculateField_management as calc_chp
from arcpy import Array
from arcpy import Point

from os import path

### Paramètres en entrée
env.overwriteOutput = True

shp_in = GetParameterAsText(0)
shp_out = GetParameterAsText(1)


### Variables utiles

chp_x = "xCentroid"
chp_y = "yCentroid"

expr_centrX = "!SHAPE.CENTROID!.split()[0]"
expr_centrY = "!SHAPE.CENTROID!.split()[1]"

new_shp(path.dirname(shp_out), path.basename(shp_out), "Point", spatial_reference = shp_in)

add = curs_ins(shp_out)

ptArray = Array()
pt = Point()

### Préalables
new_chp(shp_in, chp_x, "DOUBLE", 18, 11)
new_chp(shp_in, chp_y, "DOUBLE", 18, 11)


### Calcul des centroids
calc_chp(shp_in, chp_x, expr_centrX, "PYTHON")
calc_chp(shp_in, chp_y, expr_centrY, "PYTHON")

rows = curs_rec(shp_in)

i = 0
for objet in rows:
    pt.ID = i
    pt.X = objet.getValue(chp_x)
    pt.Y = objet.getValue(chp_y)

    feat = add.newRow()
    feat.shape = pt
    add.insertRow(feat)
    ptArray.add(pt)

    i = i +1



del add, curs_ins, curs_rec, chp_x, chp_y, \
    expr_centrX, expr_centrY, feat, i, pt, rows, ptArray, shp_in, shp_out

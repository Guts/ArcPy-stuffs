# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : GDB Spatial (re)Indexer
# Purpose : Update spatial indexes of the features classes from SIRAD database
# Authors : Julien Moura
# Contact : julien.moura@ird.fr
# Python : 2.7.x
# Encoding: utf-8
# Created : 25/10/2012
# Updated : 06/11/2012
#-------------------------------------------------------------------------------

## Import modules

from arcpy import env as enviro
from arcpy import ListDatasets, ListFeatureClasses, \
                  RemoveSpatialIndex_management, AddSpatialIndex_management

## Variables

gdb = 'D:\Datos\SIRAD_2012.gdb'
enviro.workspace = gdb

feats = []  # liste des couches de la gdb
 
for dataset in ListDatasets("","featuredataset"):
    feats += ListFeatureClasses("*", "", dataset)

     
print u"Se esta borrando los índices espaciales y creando nuevos sobre %i capas" % len(feats)
for fc in feats:
    print "\n=>%s:" % fc
    try:
        RemoveSpatialIndex_management(fc)
        print u"\tÍndice espacial de %s borrado" % fc
    except:
        print u"\t%s no tiene índice." % fc
    # Creacción de los índices
    AddSpatialIndex_management(fc)
    print u"\tNuevo índice espacial de %s borrado" % fc

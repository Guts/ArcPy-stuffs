# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : SIRAD GDB Management
# Purpose : Runs various operations on the SIRAD database : listing, check geometry
# Authors : Julien Moura
# Contact : julien.moura@ird.fr
# Python : 2.7.x
# Encoding: utf-8
# Created : 23/10/2012
# Updated : 25/10/2012
# Version : 0.1
#-------------------------------------------------------------------------------

## Import modules

from arcpy import *
from os import sep

## Variables

gdb = 'D:\Datos\SIRAD_2012.gdb'
env.workspace = gdb

num_dataset = 0
num_feature = 0
num_distrito = 0


## Fonctions

def checkgeom(geodatabase):
    env.workspace = geodatabase
    featchecked = []
    CheckGeometry_management(ListFeatureClasses(),
                             geodatabase + "Features_CheckGeom")
    

 
# List all feature classes in feature datasets
for fds in arcpy.ListDatasets("","featuredataset"):
    fcs += arcpy.ListFeatureClasses("*","",fds)
          
# List all standalone feature classes
fcs = arcpy.ListFeatureClasses()
     
print "Running the check geometry tool on %i feature classes" % len(fcs)
arcpy.CheckGeometry_management(fcs, outTable)

print (str(arcpy.GetCount_management(outTable)) + " geometry problems were found.")
print ("See " + outTable + " for full details")

## Programme principal

for tem in ListDatasets():
    print tem
    num_dataset = num_dataset +1 
    env.workspace = gdb + sep + tem
    print env.workspace
    # ici les opérations dans chaque dataset de la gdb
    if len(ListFeatureClasses()) != 0:
        checkgeom(gdb)
        for feat in ListFeatureClasses():
            lchps = []
            print "\t" + feat
            num_feature = num_feature +1
            # ici les opérations dans chaque couche de chaque dataset de la gdb
            for nomchp in ListFields(feat): lchps.append(nomchp.name)
            if 'DISTRITO' or 'DISTRITOS' or 'distrito' or 'distritos' in lchps:
                print "\t\t" + feat + " => DISTRITO"
                num_distrito = num_distrito +1




# Finalisation
print u"\nNúmero de datasets: " + num_dataset
print u"\nNúmero de capas: " + num_feature
print u"\nNúmero de capas que tienen un atributo distrito: " + num_distrito

# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name : metadata exporter
# Purpose : get the metadata from ArcCatalog and export it to ISO 19139.
# Authors : Julien Moura
# Python : 2.7.8
# Encoding: utf-8
# Created : 07/05/2015
# Updated : 25/05/2015
#-------------------------------------------------------------------------------

###############################################################################
########### Libraries #############
###################################

# Standard library
from os import listdir, mkdir, path, walk  # files and folder managing

# 3rd party libraries
try:
    from arcpy import da, env as enviro, ExportMetadataMultiple_conversion as mdConverterMulti, GetInstallInfo, ListFeatureClasses
    print("Great! ArcGIS is well installed.")
except ImportError:
    print("ArcGIS isn't registered in the sys.path")
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy')
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin')
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\ArcToolbox\Scripts')
    try:
        from arcpy import da, env as enviro, ExportMetadataMultiple_conversion as mdConverterMulti, GetInstallInfo, ListFeatureClasses
        print("ArcGIS has been added to Python path and then imported.")
    except:
        print("ArcGIS isn'installed on this computer")

###############################################################################
########## Main program ###########
###################################

# path to explore
# source = raw_input('Path to explore: ')

source = path.abspath(r"\\ZOE\data")

# Variables environnement ArcGIS
enviro.workspace = path.abspath(source)

# path to store output files
dest = r'metadata_outputs'
if not path.isdir(dest):    # test if folder already exists
    mkdir(dest, 0777) 
else:
    pass

li_data = []

# outil d'export
esriFolder = GetInstallInfo("desktop")["InstallDir"]
mdConverter = esriFolder + r"Metadata\Translator\ARCGIS2ISO19139.xml"
mdConverter = path.normpath(mdConverter)

x = 0

for dirpath, workspaces, datatypes in da.Walk(source):
    enviro.workspace = path.abspath(dirpath)
    fcs = ListFeatureClasses('*')
    try:
        print dirpath + " : " + str(fcs)
    except UnicodeEncodeError:
        print dirpath.encode('utf-8') + " : " + str(fcs)
    if fcs:
        # path to store output files
        x += 1
        dest = r'metadata_outputs/{0}'.format(x)
        if not path.isdir(dest):    # test if folder already exists
            mkdir(dest, 0777) 
        else:
            pass
        # list and export
        fc_list = [path.join(enviro.workspace, fc) for fc in fcs]
        li_data.extend(fc_list)
        mdConverterMulti(fc_list, mdConverter, dest)
    else:
        pass

# -*- coding: UTF-8 -*-
#!/usr/bin/env python
##from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Multiprocessing sample
# Purpose:      basic structure to optimize code within ArcGIS using 
#               the multiprocessing library from Python
#
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.6.x
# Created:      18/02/2013
# Updated:      01/06/2014
# Licence:      GPL 3
# Sources :     inspired from http://blogs.esri.com/esri/arcgis/2012/09/26/distributed-processing-with-arcgis-part-1/
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################
# Standard library
import multiprocessing
from os import path
import re
import sys

# arcpy
try:
    import arcpy
    print("Great! ArcGIS is well installed.")
except ImportError:
    print("ArcGIS isn't registered in the sys.path")
    if path.isdir(r'C:\Program Files (x86)\ArcGIS\Desktop10'):
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10\arcpy')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10\bin')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10\ArcToolbox\Scripts')
        print("ArcGIS 10 has been found then added to Python path and imported.")
    elif path.isdir(r'C:\Program Files (x86)\ArcGIS\Desktop10.1'):
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\arcpy')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\bin')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\ArcToolbox\Scripts')
        print("ArcGIS 10.1 has been found then added to Python path and imported.")
    elif path.isdir(r'C:\Program Files (x86)\ArcGIS\Desktop10.2'):
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\ArcToolbox\Scripts')
        print("ArcGIS 10.2 has been found then added to Python path and imported.")
    else:
        print("Oups! I can't find any ArcGIS 10.x installation!")
    try:
        import arcpy
    except:
        print("ArcGIS isn'installed on this computer")


################################################################################
########### Functions ##############
###################################
def process_features(feature_class):
    """ just a simple example of a function to execute """
    # pretty print of # entities per feature class
    print("{} contains {} entities".format(feature_class, 
                                           arcpy.GetCount_management(feature_class)))
    # End of function
    return

def main(workspace):
    """ main function which prepare and share the execution amng processors """
    # variables
    arcpy.env.workspace = workspace     # define the environment workspace
    feats = arcpy.ListFeatureClasses('*') # list features classes contained into the workspace
    featsclass_list = [path.join(workspace, fc) for fc in feats]    # get the complete path

    # Create a pool class and run the jobs–the number of jobs is equal to the number of features class
    pool = multiprocessing.Pool()   # the number of processes to use could be specified
    pool.map(process_features, featsclass_list)

    # Synchronize the main process with the job processes to ensure proper cleanup.
    pool.close()
    pool.join()
    
    # End main
    return

################################################################################
######### Main program ############
###################################
if __name__ == '__main__':
    main(workspace = r'D:\Mes documents\GIS DataBase\Exemples_Tests\Alaska\shapefiles')
# -*- coding: UTF-8 -*-
#!/usr/bin/env python


import os
import re
import multiprocessing
import sys

try:
    import arcpy
    print("Great! ArcGIS is well installed.")
except ImportError:
    print("ArcGIS isn't registered in the sys.path")
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy')
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin')
    sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\ArcToolbox\Scripts')
    try:
        import arcpy
        print("ArcGIS has been added to Python path and then imported.")
    except:
        print("ArcGIS isn'installed on this computer")


def update_shapefiles(shapefile):
    # Define the projection to wgs84 — factory code is 4326
    print shapefile + " : " + arcpy.GetCount_management(shapefile) + " entities."

    # End update_shapefiles

def main():
    # Create a pool class and run the jobs–the number of jobs is equal to the number of shapefiles
    workspace = r'D:\Mes documents\GIS DataBase\Exemples_Tests\Alaska\shapefiles'
    arcpy.env.workspace = workspace
    fcs = arcpy.ListFeatureClasses('*')
    fc_list = [os.path.join(workspace, fc) for fc in fcs]
    pool = multiprocessing.Pool()
    pool.map(update_shapefiles, fc_list)

    # Synchronize the main process with the job processes to ensure proper cleanup.
    pool.close()
    pool.join()

# End main

if __name__ == '__main__':
    main()
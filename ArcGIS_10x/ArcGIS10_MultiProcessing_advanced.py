# -*- coding: UTF-8 -*-
#!/usr/bin/env python
##from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Multiprocessing sample
# Purpose:      basic structure to optimize code within ArcGIS using 
#               the multiprocessing library from Python
#
#
# Author:       Python GIS and stuff (http://pythongisandstuff.wordpress.com)
#
# Python:       2.6.x
# Created:      18/02/2013
# Updated:      01/06/2014
# Licence:      (c) http://pythongisandstuff.wordpress.com/about/
# Source :      http://pythongisandstuff.wordpress.com/2013/07/31/using-arcpy-with-multiprocessing-%E2%80%93-part-3/
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################
# Standard library
import multiprocessing
import time
try:
    import pp
    forceMP = False
except ImportError:
    forceMP = True

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
    elif path.isdir(r'C:\Program Files (x86)\ArcGIS\Desktop10.1'):
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\arcpy')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\bin')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.1\ArcToolbox\Scripts')
    elif path.isdir(r'C:\Program Files (x86)\ArcGIS\Desktop10.2'):
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\bin')
        sys.path.append(r'C:\Program Files (x86)\ArcGIS\Desktop10.2\ArcToolbox\Scripts')
    else:
        print("Oups! I can't find any ArcGIS 10.x installation!")
    try:
        import arcpy
        print("ArcGIS has been added to Python path and then imported.")
    except:
        print("ArcGIS isn'installed on this computer")


################################################################################
########### Functions #############
##################################
'''
Step 4 of 4: Example of using Multiprocessing/Parallel Python with Arcpy...
 
Can be run either:
 1. from the command line/a Python IDE (adjust paths to feature classes, as necessary)
 2. as a Script tool within ArcGIS (ensure 'Run Ptyhon script in Process' is NOT checked when importing)
 
 The Parallel Python library must be installed before it can be used.
'''

 
def performCalculation(points_fC, polygons_fC, searchDist, typeList, calcPlatform_input=None):
    '''performCalculation(pointsFeatureClass, polygonsFeatureClass, searchDistance, typeList, calcPlatform)
 
    All inputs are specific.
 
    calcPlatform is either 'mp', to use the inbuilt Multiprocessing library, or 'pp', to use Parallel Python 
    (if it exists, otherwise defaults to mp)
 
    '''
 
    # ---------------------------------------------------------------------------
    ## Pre-calculation checks
    # ---------------------------------------------------------------------------
 
    # Check calculation platform is valid, or resort to default...
    defaultCalcTpye = 'mp'
    calcTypeExplainDict = {'pp':'Parallel Python', 'mp':'Multiprocessing'}
    if forceMP: # unable to import Parallel Python library (it has to be installed seperately)
        arcpy.AddMessage("   WARNING: Cannot load Parallel Python library, forcing Multiprocessing library...")
        calcPlatform = 'mp'
    elif (calcPlatform_input not in ['mp', 'pp']) or (calcPlatform_input == None): # Invalid/no input, resort to default
        arcpy.AddMessage("   WARNING: Input calculation platform '%s' invalid; should be either 'mp' or 'pp'. Defaulting to %s..." % (calcPlatform_input, calcTypeExplainDict[defaultCalcTpye]))
        calcPlatform = defaultCalcTpye
    else:
        calcPlatform = calcPlatform_input
 
    # ---------------------------------------------------------------------------
    ## Data extraction (parallel execution)
    # ---------------------------------------------------------------------------
 
    searchDist = int(searchDist) # convert search distance to integer...
 
    # check all datasets are OK; if not, provide some useful output and terminate
    valid_points = arcpy.Exists(points_fC)
    arcpy.AddMessage("Points Feature Class: "+points_fC)
    valid_polygons = arcpy.Exists(polygons_fC)
    arcpy.AddMessage("Polygons Feature Class: "+polygons_fC)
    dataCheck  = valid_points & valid_polygons
 
    if not dataCheck:
        if not valid_points:
            arcpy.AddError("Points database or feature class, %s,  is invalid..." % (points_fC))
        if not valid_polygons:
            arcpy.AddError("Polygons database or feature class, %s,  is invalid..." % (polygons_fC))
 
    else: # Inputs are OK, start calculation...
 
        for type in typeList: # add fields to Points file
            arcpy.AddField_management(points_fC, "polygon_type%s_Sum" % type, "DOUBLE")
            arcpy.CalculateField_management(points_fC, "polygon_type%s_Sum" % type, 0, "PYTHON")
            arcpy.AddField_management(points_fC, "polygon_type%s_Count" % type, "DOUBLE")
            arcpy.CalculateField_management(points_fC, "polygon_type%s_Count" % type, 0, "PYTHON")
            arcpy.AddMessage("    Added polygon_type%s_Sum and polygon_type%s_Count fields to Points." % (type,type))
 
        pointsDataDict = {} # dictionary: pointsDataDict[pointID][Type]=[sum of Polygon type weightings, count of Ploygons of type]
        jobs = [] # jobs are added to the list, then processed in parallel by the available workers (CPUs)
 
        if calcPlatform == 'mp':
            arcpy.AddMessage("    Utilising Python Multiprocessing library:")
            pool = multiprocessing.Pool() # initate the processing pool - use all available resources
#           pool = multiprocessing.Pool(2) # Example: limit the processing pool to 2 CPUs...
            for type in typeList: # For this specific example
                arcpy.AddMessage("      Passing %s to processing pool..." % type)
                jobs.append(pool.apply_async(findPolygons, (points_fC, polygons_fC, type, searchDist))) # send jobs to be processed
 
            for job in jobs: # collect results from the job server (waits until all the processing is complete)
                if len(pointsDataDict.keys()) == 0: # first output becomes the new dictionary
                    pointsDataDict.update(job.get())
                else:
                    for key in job.get(): # later outputs should be added per key...
                        pointsDataDict[key].update(job.get()[key])
            del jobs
 
        elif calcPlatform == 'pp':
            ppservers=()
            job_server = pp.Server(ppservers=ppservers) # initate the job server - use all available resources
#           job_server = pp.Server(2, ppservers=ppservers) # Example: limit the processing pool to 2 CPUs...
            arcpy.AddMessage("    Utilising Parallel Python library:")
            for type in typeList: # For this specific example, it would only initate three processes anyway...
                arcpy.AddMessage("      Passing %s to processing pool..." % type)
                jobs.append(job_server.submit(findPolygons, (points_fC, polygons_fC, type, searchDist), (), ("arcpy",))) # send jobs to be processed
 
            for job in jobs: # collect results from the job server (waits until all the processing is complete)
                if len(pointsDataDict.keys()) == 0: # first output becomes the new dictioanry
                    pointsDataDict.update(job())
                else:
                    for key in job():
                        pointsDataDict[key].update(job()[key]) # later outputs should be added per key...
            del jobs
 
        # ---------------------------------------------------------------------------
        ## Writing data back to points file
        # ---------------------------------------------------------------------------
 
        arcpy.AddMessage("    Values extracted; writing results to Points...")
        pointsRowList = arcpy.UpdateCursor(points_fC)
        for pointsRow in pointsRowList: # write the values for every point
            pointID = pointsRow.getValue("PointID")
            for type in typeList:
                pointsRow.setValue("polygon_type%s_Sum" % type, pointsRow.getValue("polygon_type%s_Sum" % type) + pointsDataDict[pointID][type][0])
                pointsRow.setValue("polygon_type%s_Count" % type, pointsRow.getValue("polygon_type%s_Count" % type) + pointsDataDict[pointID][type][1])
 
            pointsRowList.updateRow(pointsRow)
            del pointsRow
 
        del pointsRowList
        # just make sure any locks are cleared...
        del calcPlatform, calcPlatform_input, calcTypeExplainDict, dataCheck, defaultCalcTpye, job, key, pointID, pointsDataDict, points_fC, polygons_fC, type, valid_points, valid_polygons, searchDist, typeList
 
def findPolygons(points_FC, polygons_FC, Type, search_dist):
    funcTempDict = {}
    arcpy.MakeFeatureLayer_management(polygons_FC, '%s_%s' % (polygons_FC, Type))
    arcpy.MakeFeatureLayer_management(points_FC, '%s_%s' % (points_FC, Type))
    pointsRowList = arcpy.SearchCursor('%s_%s' % (points_FC, Type))
    for pointRow in pointsRowList: # for every origin
        pointID = pointRow.getValue("PointID")
 
        try:
            funcTempDict[pointID][Type] = [0,0]
        except KeyError: # first time within row
            funcTempDict[pointID] = {}
            funcTempDict[pointID][Type] = [0,0]
 
        arcpy.SelectLayerByAttribute_management('%s_%s' % (points_FC, Type), 'NEW_SELECTION', '"PointID" = \'%s\'' % pointID)
        arcpy.SelectLayerByLocation_management('%s_%s' % (polygons_FC, Type), 'INTERSECT', '%s_%s' % (points_FC, Type), search_dist, 'NEW_SELECTION')
        arcpy.SelectLayerByAttribute_management('%s_%s' % (polygons_FC, Type), 'SUBSET_SELECTION', '"polyType" = %s' % Type)
        polygonsRowList = arcpy.SearchCursor('%s_%s' % (polygons_FC, Type))
        for polygonsRow in polygonsRowList:
            funcTempDict[pointID][Type][0] += polygonsRow.getValue("polyWeighting")
            funcTempDict[pointID][Type][1] += 1
 
    return funcTempDict

################################################################################
######### Main program ############
###################################
if __name__ == '__main__':
    # Read the parameter values:
    #  1: points feature class (string to location, e.g. c:\GIS\Data\points.gdb\points01)
    #  2: polygons feature class (string to location)
    #  3: search distance for polygons, integer, e.g 500
    #  4: calculation type ('mp' to use Multiprocessing library, 'pp' to use Parallel Python library (if available, otherwise defaults to mp))
    pointsFC = arcpy.GetParameterAsText(0) # required
    polygonsFC = arcpy.GetParameterAsText(1) # required
    search_Distance = arcpy.GetParameterAsText(2) # required
    calcType = arcpy.GetParameterAsText(3) # optional (will default to MP)
 
    t_start = time.clock()
 
    type_list = [1,2,3,4,5,6] # polygon types to search for...
 
    # run calculation
    if '' in [pointsFC, polygonsFC, search_Distance]:# if not running from Arc, the input parameters all come out as ''
        pointsFC = "c:\\Work\\GIS\\Data\\Points.gdb\\points01"
        polygonsFC = "c:\\Work\\GIS\\Data\\Polygons.gdb\\polygons01"
        search_Distance = 1000
        performCalculation(pointsFC, polygonsFC, search_Distance, type_list)
    else:
        performCalculation(pointsFC, polygonsFC, search_Distance, type_list, calcType)
 
    arcpy.AddMessage("      ... complete in %s seconds." % (time.clock() - t_start))
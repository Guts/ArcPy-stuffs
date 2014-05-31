import arcpy, os
# Provide folder path to loop through (first level only)
folderPath = r"D:\A_Ordenar\Julien\python\capacitacion_arcpy_IRD"
for filename in os.listdir(folderPath):
    fullpath = os.path.join(folderPath, filename)
    if os.path.isfile(fullpath):
        basename, extension = os.path.splitext(fullpath)
        if extension.lower() == ".mxd":
            mxd = arcpy.mapping.MapDocument(fullpath)
            print "creating thumbnail for " + fullpath
            mxd.makeThumbnail ()
            mxd.save()
del mxd

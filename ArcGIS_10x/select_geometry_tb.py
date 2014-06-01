import arcpy
import os

carpeta_inicial = arcpy.GetParameterAsText(0)

carpeta_salida = arcpy.GetParameterAsText(1)

nombre_archivo = arcpy.GetParameterAsText(2)




nombre_archivo = nombre_archivo + '.txt'

output = open(os.path.join(carpeta_salida, nombre_archivo), 'w')


for fuente, carpeta, archivo in os.walk(carpeta_inicial):

    arcpy.env.workspace = fuente

    for punto in arcpy.ListFeatureClasses('', 'Point'):
        output.write(punto+'\n')
        print punto


output.close()

import arcpy
import os


carpeta_busqueda = arcpy.GetParameterAsText(0)

shape_initial = arcpy.GetParameterAsText(1)

carpeta_save_select = arcpy.GetParameterAsText(2)


#campo = arcpy.GetParameterAsText(3)

#dist = arcpy.GetParameterAsText(4)

sql = arcpy.GetParameterAsText(3)

output_folder = arcpy.GetParameterAsText(4)




cadena_dist = sql.split(' = ')[1][1:-1].replace(' ', '_').lower()

out_shape = os.path.join(carpeta_save_select, cadena_dist)

# Creo un shape del objeto selecionado y lo guardo
arcpy.Select_analysis(shape_initial, out_shape, sql)
                      


for fuente, carpeta, archivo in os.walk(carpeta_busqueda):

    arcpy.env.workspace = fuente
    for shape in arcpy.ListFeatureClasses('', 'Point'):
        
        output_name = arcpy.Describe(shape).baseName+ '_' + cadena_dist
    
        arcpy.Intersect_analysis([shape, out_shape + ".shp"],\
                             os.path.join(output_folder, output_name))


        # Si la capa esta vacia, la suprimo
        if int(arcpy.GetCount_management(os.path.join(output_folder, output_name)+'.shp').getOutput(0)) ==0:
            arcpy.Delete_management(os.path.join(output_folder, output_name)+'.shp')

import arcpy
import os


num_punto = 0
num_linea = 0
num_poligono = 0


informe = open(r'C:\Python26\capacitacion\web\stats_BD.html', 'w')


informe.write('<!DOCTYPE html>\n')
informe.write('<html lang="en">\n')
informe.write('    <head>\n')
informe.write('        <meta charset="utf-8">\n')
informe.write('        <title>Estadisticas de la base de datos</title>\n')
informe.write('        <link rel="stylesheet" href="demo.css"media="screen">\n')
informe.write('        <link rel="stylesheet" href="demo-print.css"media="print">\n')
informe.write('        <script src="raphael-min.js"></script>\n')
informe.write('        <script src="jquery.js"></script>\n')
informe.write('        <script src="pie.js"></script>\n')
informe.write('        <style media="screen">\n')
informe.write('            #holder {\n')
informe.write('                margin: -350px 0 0 -350px;\n')
informe.write('                width: 700px;\n')
informe.write('                height: 700px;\n')
informe.write('            }\n')
informe.write('        </style>\n')
informe.write('    </head>\n')
informe.write('    <body>\n')
informe.write('		<div>\n')


                      
carpeta_busqueda = r'C:\Python26\capacitacion\SIRAD\BASE_ DATOS_ USO_LIBRE'

for fuente, carpeta, archivo in os.walk(carpeta_busqueda):



    arcpy.env.workspace = fuente
    num_punto = num_punto + len(arcpy.ListFeatureClasses('', 'Point'))
    num_linea = num_linea + len(arcpy.ListFeatureClasses('', 'Polyline'))
    num_poligono = num_poligono + len(arcpy.ListFeatureClasses('', 'Polygon'))
        
total = num_punto + num_linea + num_poligono

informe.write('La base de datos contiene '+ str(total) + 'archivos shapefiles:\n')
informe.write('		</div>\n')
informe.write('        <table>\n')
informe.write('            <tbody>\n')
informe.write('                <tr>\n')
informe.write('                    <th scope="row">Puntos (' + str(num_punto) + ')</th>\n')
informe.write('                    <td>'+ str(num_punto) + '</td>\n')
informe.write('                </tr>\n')
informe.write('                <tr>\n')
informe.write('                    <th scope="row">Lineas (' + str(num_linea) + ')</th>\n')
informe.write('                    <td>'+ str(num_linea) + '</td>\n')
informe.write('                </tr>\n')
informe.write('                <tr>\n')
informe.write('                    <th scope="row">Poligonos (' + str(num_poligono) + ')</th>\n')
informe.write('                    <td>'+ str(num_poligono) + '</td>\n')
informe.write('                </tr>\n')
informe.write('            </tbody>\n')
informe.write('        </table>\n')
informe.write('        <div id="holder"></div>\n')
informe.write('    </body>\n')
informe.write('</html>\n')



informe.close()

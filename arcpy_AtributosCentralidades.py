## Import librairies et fonctions
# Fonctions et outils ArcGIS basiques
from arcpy import env as enviro             # pour paramètres d'environnement
from arcpy import ListFeatureClasses        # pour lister les couches d'info
from arcpy import AddField_management       # pour créer un nouvel attribut
from arcpy import DeleteField_management    # pour supprimer nouvel attribut
from arcpy import CalculateField_management # pour calculer la valeur d'un champ

### Fonctions de l'extension Spatial Analyst
##from arcpy.sa import KernelDensity        # pour calculer la densité de points

# commentaire simple
## commentaire plus important comme une section

## Définition de l'environnement de travail (workspace)
enviro.workspace = r'D:\A_Ordenar\Julien\Centralidades\Centralidades.gdb\Temas'
enviro.overwriteOutput = True


## Programme
for capa in ListFeatureClasses():
    u""" Boucle qui parcourt les couches présentes dans le workspace.
    Pour chaque couche, on crée un champ 'CEN_TEMA' que l'on remplit avec
    le thème correspondant au préfixe de la couche.
    Par exemple EDUC = Educación
    On crée également le champ 'CEN_SuTEMA' qu'on remplit avec le nom (filtré)
    de la couche."""
    print u"Couche d'information active : " + capa
    if capa[:capa.find('_')] == 'EDUC':
        u""" Pour les couches d'éducation qui ont donc le préfixe EDUC """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = u"'Educación'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'BASE':
        u""" Pour les couches de base qui ont donc le préfixe BASE """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Datos básicos útiles para los procesos'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'COM':
        u""" Pour les couches de comunicación qui ont donc le préfixe COM """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Comunicación'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'COMERC':
        u""" Pour les couches de comerce qui ont donc le préfixe COMERC """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Comercio'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'ESPEC':
        u""" Pour les couches de Infraestructuras Especiales qui ont donc le préfixe ESPEC """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Infraestructuras Especiales'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'FINAN':
        u""" Pour les couches de Finanzas qui ont donc le préfixe FINAN """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Finanzas'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'INDUS':
        u""" Pour les couches de Industria qui ont donc le préfixe INDUS """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Industria'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'SALUD':
        u""" Pour les couches de Salud qui ont donc le préfixe SALUD """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Salud y atención médica'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'TRANS':
        u""" Pour les couches de Transporte qui ont donc le préfixe TRANS """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Transporte'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'RECREA':
        u""" Pour les couches de Recreación qui ont donc le préfixe RECREA """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Recreación'",
                                  expression_type = "PYTHON")
    elif capa[:capa.find('_')] == 'ADMIN':
        u""" Pour les couches de Administración qui ont donc le préfixe ADMIN """
        # création du champ
        AddField_management(in_table = capa,
                            field_name = 'CEN_TEMA',
                            field_type = 'TEXT',
                            field_length = 50)
        # mise à jour du champ
        CalculateField_management(in_table = capa,
                                  field = 'CEN_TEMA',
                                  expression = "'Administrativo'",
                                  expression_type = "PYTHON")
    print u'\tChamp CEN_TEMA créé et rempli'

    ## fin des champs par thèmes
    # Création du champ subtema
    AddField_management(in_table = capa,
                        field_name = 'CEN_SuTEMA',
                        field_type = 'TEXT',
                        field_length = 75)
    # mise à jour du champ
    subtema = "'" + capa[capa.find('_')+1:].replace('_', ' ').replace('GC', u'(fuente: Guía Calles)') + "'"
    CalculateField_management(in_table = capa,
                              field = 'CEN_SuTEMA',
                              expression = subtema,
                              expression_type = "PYTHON")
    print u'\tChamp CEN_SuTEMA créé et rempli\n'




##for capa in ListFeatureClasses():
##    u""" Supprime tous les champs créés par la boucle for ci-dessus.
##    Mettre en commentaire pour mener le programme à bien ou n'exécuter que
##    cette partie de code pour faire une remise à zéro (reset)."""
##    DeleteField_management(capa, ["CEN_TEMA", "CEN_SuTEMA"])



print u"\n\nProgramme terminé !"
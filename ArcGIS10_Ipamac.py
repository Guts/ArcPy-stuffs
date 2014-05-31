# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien Moura
#
# Created:     28/11/2013
# Copyright:   (c) enseignant 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

## Références ==================================================================
# environnement : http://help.arcgis.com/fr/arcgisdesktop/10.0/help/index.html#/na/001w0000003s000000/
# GéoDatabase : http://help.arcgis.com/fr/arcgisdesktop/10.0/help/index.html#//0017000000pw000000
# Dataset (jeu de classes d'entités) : http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//0017000000pv000000
# Lister les données :
# Importer (convertir) des shapes dans un dataset : http://resources.arcgis.com/fr/help/main/10.1/index.html#//001200000021000000
# Réparer les géométries (bourrin) : http://help.arcgis.com/fr/arcgisdesktop/10.0/help/index.html#//00170000003v000000
# Ajout d'un index spatial : http://help.arcgis.com/fr/arcgisdesktop/10.0/help/index.html#//001700000060000000





## Modules à importer ==========================================================
print 'top'
# standard library
from os import path, chdir
from time import clock, strftime, gmtime

tps_launch = clock()

# 3rd party (ArcPy = module pour manipuler ArcGIS)
from arcpy import env as enviro # paramètres d'environnement

from arcpy import CreateFileGDB_management as new_gdb
from arcpy import CreateFeatureDataset_management as add_dataset
from arcpy import CreateTable_management as new_table
from arcpy import FeatureClassToGeodatabase_conversion as import_shp

from arcpy import ListDatasets, ListFeatureClasses

from arcpy import SelectLayerByAttribute_management as sel_attr
from arcpy import Select_analysis as sel_analyz
from arcpy import Buffer_analysis as tampon
from arcpy import Union_analysis as union
from arcpy import Merge_management as combine
from arcpy import Dissolve_management as dissout
from arcpy import Clip_analysis as decoupe

from arcpy import AddField_management as add_field
from arcpy import CalculateField_management as calc_field

from arcpy import CheckGeometry_management as geom_check
from arcpy import RepairGeometry_management as geom_repair

from arcpy import MultipartToSinglepart_management as multi2single

from arcpy import GetCount_management as compter
from arcpy import Dissolve_management as groupby_attr

from arcpy import SearchCursor, InsertCursor

from arcpy import AddSpatialIndex_management as add_spatial_index

from arcpy import CalculateDefaultGridIndex_management as calc_grid_index
from arcpy import Rename_management as renom

tps_post_import = clock()
print 'top arcpy'
## Fonctions ===================================================================

def main():
    """ for standalone execution """
    pass

def calc_occurs(target, result, field_name, field_type, field_length):
    """
    Calculates frequencies on a field in target (table, feature, shp) and returns
    a table of results.
    """
    # création du dictionnaire (temporaire) des occurences/fréquences
    dico_freq = {}
    # création de la table résultat (= en sortie)
    new_table(path.split(result)[0], path.split(result)[1])
    # curseurs pour parcourir (r = read) et écrire (w = write) les données ligne par ligne
    curs_r = SearchCursor(target, "", "", field_name)
    curs_w = InsertCursor(result)
    # ajout des 2 champs dans la table résultat
    add_field(result, "OCCUR", field_type, "", "", field_length)
    add_field(result, "FREQ", "SHORT")
    # calcul et ajout au dictionnaire intermédiaire
    for obj in curs_r:
        value = obj.getValue(field_name)
        if dico_freq.has_key(value):
            dico_freq[value] = dico_freq.get(value)+1
        else:
            dico_freq[value] = 1
    del curs_r
    # mise à jour de la table résultats
    for occur in dico_freq.keys():
        row = curs_w.newRow()
        row.OCCUR = occur
        row.FREQ = dico_freq.get(occur)
        curs_w.insertRow(row)
    # nettoyage des curseurs (pour éviter le verrouillage des données = .lock)
    del row, curs_w
    # fin de fonction
    return dico_freq



## Programme ===================================================================
# définition des paramètres de base
espace_de_travail = r"E:\SILAT\TP_Meff_Ipamac\subset"
enviro.workspace = espace_de_travail    # espace de travail pour ArcGIS
enviro.overwriteOutput = True       # réécriture autorisée
chdir(espace_de_travail)        # espace de travail pour Python

gdb_name = 'Ipamac.gdb'
srs_ref_path = path.join(espace_de_travail, 'BD_carto_routes_2006.prj')


# données en entrée
bd_carthage = r"BD_carthage_reseau_hydro.shp"
bd_carto = r"BD_carto_routes_2006.shp"
clc = r"clc_2006.shp"
lim_admin = r"communes_ipamac.shp"
ferrov = r"voies_ferrees.shp"

li_data_in = (bd_carthage, bd_carto, clc, lim_admin, ferrov)

# paramètres en entrée
li_clc_nats = ('231', '243', '244', \
               '311', '312', '313', '321', '322', '323', '324', '331', '332', '333', '334', '335',\
               '411', '412', '421', '422', '423')



# si l'environnement de travail n'est pas en place, on le crée et on le paramètre
if path.isdir(gdb_name):
    print u'already exists'
else:
    new_gdb(espace_de_travail, gdb_name)    # création de la gdb

gdb_path = path.join(espace_de_travail, gdb_name)
enviro.workspace = gdb_path


if len(ListDatasets()) == 0:
    add_dataset(gdb_path, 'subset', srs_ref_path)   # ajout du dataset à la gdb
else:
    u'dataset already exists'


subset_path = path.join(gdb_path, 'subset') # chemin absolu du dataset
enviro.workspace = subset_path
li_data_subset = ListFeatureClasses()    # liste des classes d'entités présentes dans le dataset

if len(li_data_in) != li_data_subset:
    import_shp(li_data_in, subset_path)
    li_data_subset = ListFeatureClasses()    # liste des classes d'entités présentes dans le dataset

# renommage
for data in li_data_subset:
    renom(data, data[:-4])

bd_carthage = bd_carthage[:-4]
bd_carto = bd_carto[:-4]
clc = clc[:-4]
lim_admin = lim_admin[:-4]
ferrov = ferrov[:-4]

li_data_subset = ListFeatureClasses()


# check des géométries
result_check_geom = path.join(gdb_path, 'CheckGeometry_Resultats')
geom_check(li_data_subset, result_check_geom)
num_err_geom = compter(result_check_geom)
if num_err_geom > 0:
    print u'Houston, we have %s geometry problem !' % num_err_geom
    result_check_geom_group = path.join(gdb_path, 'CheckGeometry_Resultats_group')
    calc_occurs(result_check_geom, result_check_geom_group, "CLASS", "TEXT", 255)
    print u"Résultats de la vérification des géométries : %s" % result_check_geom
    print u"Nombre d'erreurs par source de données : %s" % result_check_geom_group

# nettoyage des géométries
curs_r = SearchCursor(result_check_geom_group)
for data in curs_r:
    data_path = data.getValue("OCCUR")
    data_num_err = data.getValue("FREQ")
    geom_repair(data_path)
    print u'Les %s erreurs de géométrie de %s ont été réparées' % (data_num_err, data_path)
del curs_r

# ajout d'un index spatial
print u"Création des index spatiaux"
for data in li_data_subset:
    calc_grid_index(data)
    add_spatial_index(data)


##########################################################################################
# sélection des milieux naturels dans la couche CLC
expr_sel_codes_nat = '"CODE_06" IN %s' % str(li_clc_nats)
clc_nat = clc + "_zones_nats"
sel_analyz(clc, clc_nat, expr_sel_codes_nat)
clc_nat_diss = clc_nat + "_dissolved"
dissout(clc_nat, clc_nat_diss)
print u"\n\t- ZONES NATURELLES -\nZones naturelles isolées et fusionnées"



# sélection des routes aux vocations voulues
expr_sel_routes_vocations = '"VOCATION" IN %s' % str(('1', '2', '6'))
routes_class = bd_carto + "_vocas"
sel_analyz(bd_carto, routes_class, expr_sel_routes_vocations)
print u"\n\t- RESEAU ROUTIER -\nRoutes isolées selon les vocations"

# ajout d'un champ destiné à la taille du tampon aux données de routes
add_field(routes_class, "buffer_siz", "SHORT")
print u"Champ pour les zones tampons créé"

# mise à jour du champ du buffer selon les types de route
expr_calc_buffer_routes = "buffer_size(!USAGE!, !NB_VOIES!)"
cb_routes_type_voies = """def buffer_size(usage, nb_voies):
    if usage == '2':
        return '10'
    elif usage == '3':
        return '8'
    elif usage == '1' and nb_voies != '5':
        return '25'
    elif usage == '1' and nb_voies == '5':
        return '15'
    elif usage == '1' and nb_voies == 'S':
        return '8'"""

calc_field(routes_class, "buffer_siz", expr_calc_buffer_routes, "PYTHON", cb_routes_type_voies)
print u"Champ pour les zones tampons mis à jour en fonction de l'usage et du nombre de voies"

# création de la zone tampon (= buffer)
routes_buffer = "routes_buffer"
tampon(routes_class, routes_buffer, "buffer_siz", "FULL", "ROUND", "ALL")
print u"Tampon autour des routes créé"




# sélection des voies ferrées en service et en construction
expr_sel_ferrov = '"CLASSE" IN %s' % str(('1', '2'))
ferrov_class = ferrov + "_class"
sel_analyz(ferrov, ferrov_class, expr_sel_ferrov)
print u"\n\t- VOIES FERREES -\nVoies ferrées en service et en construction isolées"

# ajout d'un champ destiné à la taille du tampon autour des voies ferrées
add_field(ferrov_class, "buffer_siz", "SHORT")
print u"Champ pour les zones tampons créé"

# mise à jour du champ du buffer selon les types de route
expr_calc_buffer_ferrov = "buffer_size(!NB_VOIES!)"
cb_ferrov_nbvoies = """def buffer_size(nb_voies):
    if nb_voies == '1':
        return '4'
    elif nb_voies >= '2':
        return '8'"""

calc_field(ferrov_class, "buffer_siz", expr_calc_buffer_ferrov, "PYTHON", cb_ferrov_nbvoies)
print u"Champ pour les zones tampons mis à jour en fonction du nombre de voies"

# création de la zone tampon (= buffer)
ferrov_buffer = "voies_ferrees_buffer"
tampon(ferrov_class, ferrov_buffer, "buffer_siz", "FULL", "ROUND", "ALL")
print u"Tampon autour des voies ferrées créé"





# sélection des cours d'eau supérieurs à 15m de largeur
expr_sel_hydro = '"LARGEUR" >= %s' % "'15'"
hydro_class = bd_carthage + "_class"
sel_analyz(bd_carthage, hydro_class, expr_sel_hydro)
print u"\n\t- RESEAU HYDROGRAPHIQUE -\nCours d'eau supérieurs à 15m de largeur isolés"

# ajout d'un champ destiné à la taille du tampon autour des voies ferrées
add_field(hydro_class, "buffer_siz", "SHORT")
print u"Champ pour les zones tampons créé"

# mise à jour du champ du buffer selon les types de route
expr_calc_buffer_hydro = "buffer_size(!LARGEUR!)"
cb_hydro_largeur = """def buffer_size(largeur):
    if largeur >= '15' and largeur <= '50':
        return '8'
    elif largeur > '50':
        return '25'
    else:
        return '8'"""

calc_field(hydro_class, "buffer_siz", expr_calc_buffer_hydro, "PYTHON", cb_hydro_largeur)
print u"Champ pour les zones tampons mis à jour en fonction de la largeur du cours d'eau"


# création de la zone tampon (= buffer)
hydro_buffer = "hydro_buffer"
tampon(hydro_class, hydro_buffer, "buffer_siz", "FULL", "ROUND", "ALL")
print u"Tampon autour des cours d'eau créé"



########################################################################################

# fusion (combinaison) des zones tampon créées
print u"\n\t- FUSION et DISSOLUTION DES TAMPONS -\n"
li_buffer = [hydro_buffer, ferrov_buffer, routes_buffer]
buffer_comb = "fragmentation_combined"
combine(li_buffer, buffer_comb)
buffer_diss = "fragmentation_dissolved"
dissout(buffer_comb, buffer_diss)


# découpage des zones naturelles avec les éléments de fragmentation (=buffers dissous)
print u"\n\t- DECOUPAGE DES ZONES NATURELLES AVEC LES TAMPONS -\n"
clc_nat_uni = clc_nat + "_ZN_unioned"
union([clc_nat_diss, buffer_diss], clc_nat_uni, "ALL")


# extraction des éléments présents dans la zone tampon
print u"\n\t- EXTRACTION DES ZONES NATURELLES CONCERNEES -\n"
fid_clc = "FID_" + clc_nat_diss
fid_frag = "FID_" + buffer_diss
clc_nat_finale = clc_nat + "_finale"
expr_sel_zn_buff = """ "%s" = 0 OR "%s" = -1 """ % (fid_clc, fid_frag)
sel_analyz(clc_nat_uni, clc_nat_finale, expr_sel_zn_buff)
    

# fusion des différentes zones
print u"\n\t- FUUUUUUUUUSION DES ZONES NATURELLES CONCERNEES -\n"
clc_fin_group = clc + "_final_diss"
dissout(clc_nat_finale, clc_fin_group)


# éclatement des polygones non contigus
print u"\n\t- Et là, gros kick dans les polygones : on les E-CLA-TE -\n"
clc_fin_eclat = clc + "_final_eclate"
multi2single(clc_fin_group, clc_fin_eclat)


# ajout d'un champ pour y mettre la surface effective des polygones et qui ne bouge plus par la suite
print u"\n\t- CALCUL des surfaces des polygones continues des zones naturelles et des limites administratives -\n"
fd_clc_surf = "clc_AiCpl"
fd_admin_surf = "adm_Atot"
add_field(clc_fin_eclat, fd_clc_surf, "DOUBLE")
add_field(lim_admin, fd_admin_surf, "DOUBLE")
calc_field(clc_fin_eclat, fd_clc_surf, "!shape.area!", "PYTHON")
calc_field(lim_admin, fd_admin_surf, "!shape.area!", "PYTHON")


# union des limites administratives et des zones naturelles continues
clc_admin_unioned = "clc_communes_unioned"
union([clc_fin_eclat, lim_admin], clc_admin_unioned)
fd_surf_compl = "Ai_Acpl"
add_field(clc_admin_unioned, fd_surf_compl, "DOUBLE")
expr_calc_surf = "!%s! * !Shape_Area!" % fd_clc_surf
calc_field(clc_admin_unioned, fd_surf_compl, expr_calc_surf, "PYTHON")



# fusion par communes
final_admin_Ai_Acompl = "FINAL_LimAdm_Ai_Acompl"
fd_fusionnes = ["COMMUNE", "CODEINSEE", fd_admin_surf]
fd_stats = [[fd_surf_compl, "SUM"]]
dissout(clc_admin_unioned, final_admin_Ai_Acompl, fd_fusionnes, fd_stats, "MULTI_PART")
add_field(final_admin_Ai_Acompl, "Meff", "DOUBLE")
expr_calc_meff = "!SUM_%s! / (!%s! * 1000000)" % (fd_surf_compl, fd_admin_surf,)
calc_field(final_admin_Ai_Acompl, "Meff", expr_calc_meff, "PYTHON")



#======================================================
tps_final = clock()

print u"\nIl s'est écoulé %s entre le début du script et la fin de l'import des modules arcpy" \
      % strftime('%H %M %S', gmtime(tps_post_import - tps_launch))

print u"\nIl s'est écoulé %s entre le début et la fin du script" \
      % strftime('%H %M %S', gmtime(tps_final - tps_launch))

##==============================================================================
if __name__ == '__main__':
    main()

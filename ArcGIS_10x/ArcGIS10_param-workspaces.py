# -*- coding: cp1252 -*-
#-------------------------------------------------------------------------------
# Name:        Param�trer les mxd
# Purpose:     Moulinette qui recherche les mxd pr�sents dans le dossier cible
#              et son arborescence pour �diter les propri�t�s donn�es en d�but
#              de programme.
#
# Author:      Julien Moura
#
# Created:     09/01/2012
# Copyright:   (c) 2012
# Licence:     Arcgis v10
#-------------------------------------------------------------------------------
#!/usr/bin/env python

### import des modules
import arcpy
import os

### variables de base
doss_cible = r'\\Compujulien\sig\Cartoteca\SIRAD_MAPAS'    # dossier cible
auteur = r'Pauline Gluski, Pierre Vernier'    # auteurs
cred = r'IRD - PACIVUR 2010'    # cr�dits
descr = r''    # description
lien = r'http://www.peru.ird.fr/spip.php?page=article_programmes_regionaux&id_article=2458&id_rubrique=459'
resume = r'Proyecto �Elaboraci�n de un Sistema de Informaci�n Geogr�fico y An�lisis de Recursos Esenciales para la Respuesta y Recuperaci�n Temprana ante la Ocurrencia de un sismo y/o Tsunami en el �rea Metropolitana de Lima y Callao� (Proyecto SIRAD Convocatoria PNUD/SDP-052/2009 / 22 de abril - 15 febrero 2011).'
motcles = r'riesgos, vulnerabilidades, planificaci�n preventiva, lima, callao, sismo, tsunami, SIRAD'


for source, dossier, fichiers in os.walk(doss_cible):
    for d in dossier:
        for i in fichiers:
            if os.path.splitext(i)[1] == '.mxd':
                mxd = arcpy.mapping.MapDocument(os.path.join(source, i))
                mxd.author = auteur
                mxd.credits = cred
                mxd.description = descr
                mxd.hyperlinkBase = lien
                mxd.summary = resume
                mxd.tags = motcles
                mxd.title = os.path.splitext(i)[0].replace('_', ' ')
                mxd.makeThumbnail ()
                mxd.save()
                print r'Mxd : ' + i + r' trait�.'
                del mxd

# -*- coding: iso8859-1 -*-
#-------------------------------------------------------------------------------
# Name: CreerOursinsReels.py
# Purpose: Permet de g�n�rer les oursins r�els issus d'une couche de centres et d'une couche d'extr�mit�s.
#          La couche des centres et la couche des extr�mit�s sont des couches de points dont les entit�s
#          sont reli�es via un identifiant commun (oursins r�els).
#
# Author: fpr - support esri France
#
# Created:     27 aout 2009
# Updated:      7 janv. 2013 for ArcGIS Desktop 10.0 et 10.0
#              - Ajout des 2 champs identifiants � la couche de lignes en sortie.
#              => permet de r�aliser des jointures
#              - Fonctionne � la fois sur des shapefile et des classes d'entit�s de G�odatabase   
#             
# Copyright:   (c) esri France
# ArcGIS Version:   10.0 et 10.1 SP1
# Python Version:   2.6
#-------------------------------------------------------------------------------
import os
import sys
import arcpy

def CreerPolyligne(PointDebut, PointFin):
    """Retourne un objet ligne � partir du point de d�but et d e fin.

    INPUTS:
    point de d�but et point de fin

    OUTPUT:
    objet ligne
    """

    # Cr�er une polyligne
    line = arcpy.Array()
    line.add(PointDebut)
    line.add(PointFin)
    
    return line

def CreerPolyligneSelonPoint(PointDebut, arcTan, longueurLigne):
    import math
    """Retourne un objet ligne � partir du point de d�but, un angle et une longueur.

    INPUTS:
    point de d�but, l'angle de la ligne, une longueur

    OUTPUT:
    objet ligne
    """

    # Cr�er une polyligne
    ligne = arcpy.Array()
    ligne.add(PointDebut)
    
    # D�termine le point de fin selon
    PointFin = arcpy.Point()
    PointFin.X = PointDebut.X - math.sin(arcTan)* longueurLigne
    PointFin.Y = PointDebut.Y - math.cos(arcTan)* longueurLigne

    ligne.add(PointFin)
    
    return ligne

def DistanceEntreDeuxPoints(PointDebut, PointFin):
    import math
    """Retourne la distance entre deux points.

    INPUTS:
    point de d�but et point de fin

    OUTPUT:
    distance
    """
    
    distance = math.sqrt((PointDebut.X - PointFin.X)**2 + (PointDebut.Y - PointFin.Y)**2)

    return distance

def ArcTanEntreDeuxPoints(PointDebut, PointFin):
    import math
    """Retourne l'arc tan entre deux points.

    INPUTS:
    point de d�but et point de fin

    OUTPUT:
    arcTan
    """
    
    arcTan = math.atan2((PointDebut.X - PointFin.X),(PointDebut.Y - PointFin.Y))
    
    return arcTan

def DistanceRelative(Distance, Pourcentage):
    """Retourne la distance issue du pourcentage souhait�e.

    INPUTS:
    distance

    OUTPUT:
    50 pourcent de la distance par exemple
    """
    distanceRel = (float((Distance)) * float(Pourcentage))/100
    
    return distanceRel

def DeterminerTypeChamp(inFeatureClass, inFieldName):
    """Retourne le type d'un champ Chaine ou chiffre

    INPUTS:
    Nom de la classe d'entit�s et du champ

    OUTPUT:
    Retourne String ppour une TXT et LONG pour des chiffres
    """
    # Process: D�termine le type du champ
    ListFieldString = ["String"]
    ListFieldFloat = ["SmallInteger", "Integer", "Single", "Double", "OID"]
    FieldType =""
    fields = arcpy.ListFields(inFeatureClass)
    for field in fields:
        if field.name == inFieldName:
            if field.type in ListFieldString:
                FieldType = "TEXT"
            elif field.type in ListFieldFloat:
                FieldType = "LONG"
    
        
    return FieldType


def do_analysis(inCenter,inFieldCenter,inBorder,inFieldBorder,inDimension,outFile):
    """TODO: Add documentation about this function here"""
    try:
        #TODO: Add analysis here
        arcpy.AddMessage("*"*10)
        arcpy.AddMessage("Processus : Cr�er des oursins ...")
        
        # Process: Obtenir la reference spatiale de la couche en entr�e
        sr = arcpy.Describe(inCenter).spatialreference
        
        # Process: Obtenir les champs OBJECTID des deux couches en entrants pour en faire r�f�rence sur la couche en sortie
        OIDCenter = arcpy.Describe(inCenter).OIDFieldName
        OIDBorder = arcpy.Describe(inBorder).OIDFieldName
        
        # Process: Obtenir les champs shape
        SHPCenter = arcpy.Describe(inCenter).shapeFieldName
        SHPBorder = arcpy.Describe(inBorder).shapeFieldName
        
        
        # Process: Cr�er la classe d'entit� de polylignes en sortie...
        arcpy.CreateFeatureclass_management(os.path.dirname(outFile), os.path.basename(outFile), "POLYLINE", "", "DISABLED", "DISABLED", sr, "", "0", "0", "0")
        
        # Process: Ajouter des champs
        inFieldType = DeterminerTypeChamp(inCenter, inFieldCenter)
        arcpy.AddField_management(outFile, "ID_CENTER", "LONG")
        arcpy.AddField_management(outFile, "ID_LINK", inFieldType)
        arcpy.AddField_management(outFile, "ID_BORDER", "LONG")
        
        # Process: Mise � jour de la couche de polylignes en sortie
        iCursors = arcpy.InsertCursor(outFile, sr)
        
        # Process: Rechercher les points de centre
        sCursorsCen = arcpy.SearchCursor(inCenter)
        for sCursorCen in sCursorsCen:
            
            # Process: R�cup�rer le point de d�but
            featCenter = sCursorCen.getValue(SHPCenter)
            pntCenter = featCenter.getPart()
            #gp.AddMessage("Xd %s - Yd %s" % (str(pntCenter.x), str(pntCenter.y)))
                    
            # Process: D�termine le type de FC pour gestion de la requete
            delimitedfield = arcpy.AddFieldDelimiters(inBorder, inFieldBorder)
            sCursorsSel = arcpy.SearchCursor(inBorder, delimitedfield + " = " + str(sCursorCen.getValue(inFieldCenter)))
    
            for sCursorSel in sCursorsSel:
                # Process: R�cup�rer le point de fin
                featBorder = sCursorSel.getValue(SHPBorder)
                pntBorder = featBorder.getPart()
                #gp.AddMessage("Xf %s - Yf %s" % (str(pntBorder.x), str(pntBorder.y)))
                    
                # Process: Cr�er la polyligne
                iCursor = iCursors.newRow()
                
                if int(inDimension) != 100:
                    # Process: R�cup�re la longueur de la ligne
                    dist = DistanceEntreDeuxPoints(pntCenter, pntBorder)
                    
                    # Process: R�cup�re x pourcentage de la longueur
                    distBranche = DistanceRelative(dist, int(inDimension))
                    
                    # Process: R�cup�re l'arc tan de la ligne
                    valeurArcTan = ArcTanEntreDeuxPoints(pntCenter, pntBorder)
                    
                    # Process: Cr�er la ligne
                    iLine = CreerPolyligneSelonPoint(pntCenter, valeurArcTan, distBranche)
                else:
                    # Process: Cr�er la ligne
                    iLine = CreerPolyligne(pntCenter, pntBorder)
                
                # Process: stocker la ligne
                iCursor.setValue("Shape",iLine)
                iCursor.setValue("ID_CENTER",sCursorCen.getValue(OIDCenter))
                iCursor.setValue("ID_LINK",sCursorCen.getValue(inFieldCenter))
                iCursor.setValue("ID_BORDER",sCursorSel.getValue(OIDBorder))
                iCursors.insertRow(iCursor)
                iLine.removeAll()
        
        # Vide les variables
        del iCursors, sCursorsCen, sCursorCen, sCursorsSel, sCursorSel
    
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    finally:
        arcpy.AddMessage("Processus : Fin du traitement")
        arcpy.AddMessage("*"*10)
# End do_analysis function

if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    print argv
    do_analysis(*argv)

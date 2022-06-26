# -*- coding: cp1252 -*-
""" 
ExtraireCentres.py

Auteur : Support ESRI France

Date: 27/08/2009

Description : Permet de g�n�rer les oursins r�els issus d'une couche de centres et d'une couche d'extr�mit�s.
              La couche des centres et la couche des extr�mit�s sont des couches de points dont les entit�s
              sont reli�es via un identifiant commun (oursins r�els). 
               
Liste des param�tres :
                                Propri�t�s des param�tres
           Nom complet                   Type de donn�es   Type      Direction Valeur multiple Default    Filtre    Obtenu par
argv[1]   Centre des oursins             Couche d'entit�s  Required  Input     No              
argv[2]   Champ identifiant              Champ             Required  Input     No                         Yes       Centre des oursins
argv[3]   Extr�mit� des oursins          Couche d'entit�s  Required  Input     No                         Yes       Extr�mit� des oursins
argv[4]   Champ identifiant le centre    Champ             Required  Input     No
argv[5]   Dimension des branches en %    Classe d'entit�s  Required  Input     No               100       plage de 1� 100
argv[6]   Couche de polylignes en sortie Classe d'entit�s  Required  Output    No
 ----------------------------------------------------------------------
"""
# Import system modules
import os

def CreerPolyligne(PointDebut, PointFin):
    """Retourne un objet ligne � partir du point de d�but et d e fin.

    INPUTS:
    point de d�but et point de fin

    OUTPUT:
    objet ligne
    """

    #Cr�er une polyligne
    line = gp.createObject("array")
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

    #Cr�er une polyligne
    ligne = gp.createObject("array")
    ligne.add(PointDebut)
    
    # D�termine le point de fin selon
    PointFin = gp.createObject("Point")
    PointFin.x = PointDebut.x - math.sin(arcTan)* longueurLigne
    PointFin.y = PointDebut.y - math.cos(arcTan)* longueurLigne

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
    
    distance = math.sqrt((PointDebut.x - PointFin.x)**2 + (PointDebut.y - PointFin.y)**2)

    return distance

def ArcTanEntreDeuxPoints(PointDebut, PointFin):
    import math
    """Retourne l'arc tan entre deux points.

    INPUTS:
    point de d�but et point de fin

    OUTPUT:
    arcTan
    """
    
    arcTan = math.atan2((PointDebut.x - PointFin.x),(PointDebut.y - PointFin.y))
    
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

def DeterminerTypeChamp(inFeatureClass, fieldName):
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
    fields = gp.listfields(inBorder)
    field = fields.next()
    while field:
        if field.name == inFieldBorder:
            if field.type in ListFieldString:
                FieldType = "TEXT"
            elif field.type in ListFieldFloat:
                FieldType = "LONG"
        field = fields.next()
    
        
    return FieldType

def isShapeFile(inputFC):
    """Returns whether the input feature class is a shapefile.

    INPUTS:
    inputFC (str): catalogue path to the feature class

    OUTPUT:
    return (bool): is the inputFC a shapefile?
    """

    shpFileBool = 0
    baseFile = os.path.basename(inputFC)
    try:
        splitBase = baseFile.split(".")
        if splitBase[-1].upper() == "SHP":
            shpFileBool = 1
    except:
        pass

    return shpFileBool

try:
    #pour les utilisateurs ArcGIS 9.2/9.3
    import arcgisscripting
    gp = arcgisscripting.create()
    print "\n" + "Utilisation de ArcGIS 9.2 ou sup�rieure avec arcgisscripting..." + "\n"
    gp.AddMessage("\n" + "Utilisation de ArcGIS 9.2 ou sup�rieure avec arcgisscripting..." + "\n")
except:
    #pour les utilisateurs ArcGIS 9.0/9.1
    import win32com.client
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
    print "\n" + "Utilisation de ArcGIS 9.0/9.1 ou sup�rieure avec win32com.client.Dispatch..." + "\n"
    gp.AddMessage("\n" + "Utilisation de ArcGIS 9.0/9.1 ou sup�rieure avec win32com.client.Dispatch..." + "\n")
    
gp.overwriteoutput = 1

# Param�tre en entr�e
inCenter = gp.GetParameterAsText(0)             ## A CHANGER ##
inFieldCenter = gp.GetParameterAsText(1)        ## A CHANGER ##
inBorder = gp.GetParameterAsText(2)             ## A CHANGER ##
inFieldBorder = gp.GetParameterAsText(3)        ## A CHANGER ##
inDimension = gp.GetParameterAsText(4)              ## A CHANGER ##
outFile = gp.GetParameterAsText(5)              ## A CHANGER ##

try:
    gp.AddMessage("*"*10)
    gp.AddMessage("Processus : Cr�er des oursins ...")
    
    # Process: Obtenir la reference spatiale de la couche en entr�e
    sr = gp.describe(inCenter).spatialreference
    
    # Process: Cr�er la classe d'entit� de polylignes en sortie...
    gp.CreateFeatureclass_management(os.path.dirname(outFile), os.path.basename(outFile), "POLYLINE", "", "DISABLED", "DISABLED", sr, "", "0", "0", "0")
    
    # Process: Ajouter des champs
    inFiledType = DeterminerTypeChamp(inCenter, inFieldCenter)
    gp.AddField(outFile, "ID_CENTRE", inFiledType)
    
    # Process: Mise � jour de la couche de polylignes en sortie
    iCursors = gp.insertcursor(outFile)
    
    # Process: Rechercher les points de centre
    sCursorsCen = gp.searchcursor(inCenter)
    sCursorCen = sCursorsCen.next()
    while sCursorCen:
        # Process: R�cup�rer le point de d�but
        featCenter = sCursorCen.GetValue("Shape")
        pntCenter = featCenter.GetPart()
        #gp.AddMessage("Xd %s - Yd %s" % (str(pntCenter.x), str(pntCenter.y)))
                
        # Process: D�termine le type de FC pour gestion de la requete
        inFCType = isShapeFile(gp.describe(inBorder).CatalogPath)
        try: 
            if inFCType == 1:
                # Process: D�termine le type du champ
                if DeterminerTypeChamp(inBorder, inFieldBorder) == "TEXT":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
                elif DeterminerTypeChamp(inBorder, inFieldBorder) == "LONG":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + str(sCursorCen.GetValue(inFieldCenter)))
                else:
                    gp.AddMessage("Erreur type du champ en SHP")
            elif inFCType == 0:
                if DeterminerTypeChamp(inBorder, inFieldBorder) == "TEXT":             
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
                elif DeterminerTypeChamp(inBorder, inFieldBorder) == "LONG":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + str(sCursorCen.GetValue(inFieldCenter)))
                else:
                    gp.AddMessage("Erreur type du champ en GeoDatabase")
        except:
            if DeterminerTypeChamp(inBorder, inFieldBorder) == "TEXT":             
                sCursorsSel = gp.searchcursor(inBorder, '[' + inFieldBorder + '] = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
            elif DeterminerTypeChamp(inBorder, inFieldBorder) == "LONG":
                sCursorsSel = gp.searchcursor(inBorder, '[' + inFieldBorder + '] = ' + str(sCursorCen.GetValue(inFieldCenter)))
            else:
                gp.AddMessage("Erreur type du champ pour version 9.1")
                    
#        # version 9.3
#        delimitedfield = gp.AddFieldDelimiters(inBorder, inFieldBorder)
#        sCursorsSel = gp.searchcursor(inBorder, delimitedfield + " = " + str(sCursorCen.GetValue(inFieldCenter)))

        sCursorSel = sCursorsSel.next()
        while sCursorSel:
            # Process: R�cup�rer le point de fin
            featBorder = sCursorSel.GetValue("Shape")
            pntBorder = featBorder.GetPart()
            #gp.AddMessage("Xf %s - Yf %s" % (str(pntBorder.x), str(pntBorder.y)))
                
            # Process: Cr�er la polyligne
            iCursor = iCursors.newrow()
            
            if inDimension != 100:
                # Process: R�cup�re la longueur de la ligne
                dist = DistanceEntreDeuxPoints(pntCenter, pntBorder)
                
                # Process: R�cup�re x pourcentage de la longueur
                distBranche = DistanceRelative(dist, inDimension)
                
                # Process: R�cup�re l'arc tan de la ligne
                valeurArcTan = ArcTanEntreDeuxPoints(pntCenter, pntBorder)
                
                # Process: Cr�er la ligne
                iLine = CreerPolyligneSelonPoint(pntCenter, valeurArcTan, distBranche)
            else:
                # Process: Cr�er la ligne
                iLine = CreerPolyligne(pntCenter, pntBorder)
            
            # Process: stocker la ligne
            iCursor.shape = iLine
            iCursor.ID_CENTRE = sCursorCen.GetValue(inFieldCenter)
            iCursors.insertrow(iCursor)
            iLine.removeall()
            sCursorSel = sCursorsSel.next()
           
        sCursorCen = sCursorsCen.next()
    
    # Vide les variables
    del iCursors, sCursorsCen, sCursorCen, sCursorsSel, sCursorSel
    
    gp.AddMessage("Processus : Fin du traitement")
    gp.AddMessage("*"*10)
    
except:
    gp.AddMessage(gp.GetMessages(2))
    print gp.GetMessages(2)

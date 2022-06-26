# -*- coding: cp1252 -*-
""" 
ExtraireCentres.py

Auteur : Support ESRI France

Date: 27/08/2009

Description : Permet de générer les oursins réels issus d'une couche de centres et d'une couche d'extrémités.
              La couche des centres et la couche des extrémités sont des couches de points dont les entités
              sont reliées via un identifiant commun (oursins réels). 
               
Liste des paramètres :
                                Propriétés des paramètres
           Nom complet                   Type de données   Type      Direction Valeur multiple Default    Filtre    Obtenu par
argv[1]   Centre des oursins             Couche d'entités  Required  Input     No              
argv[2]   Champ identifiant              Champ             Required  Input     No                         Yes       Centre des oursins
argv[3]   Extrémité des oursins          Couche d'entités  Required  Input     No                         Yes       Extrémité des oursins
argv[4]   Champ identifiant le centre    Champ             Required  Input     No
argv[5]   Dimension des branches en %    Classe d'entités  Required  Input     No               100       plage de 1à 100
argv[6]   Couche de polylignes en sortie Classe d'entités  Required  Output    No
 ----------------------------------------------------------------------
"""
# Import system modules
import os

def CreerPolyligne(PointDebut, PointFin):
    """Retourne un objet ligne à partir du point de début et d e fin.

    INPUTS:
    point de début et point de fin

    OUTPUT:
    objet ligne
    """

    #Créer une polyligne
    line = gp.createObject("array")
    line.add(PointDebut)
    line.add(PointFin)
    
    return line

def CreerPolyligneSelonPoint(PointDebut, arcTan, longueurLigne):
    import math
    """Retourne un objet ligne à partir du point de début, un angle et une longueur.

    INPUTS:
    point de début, l'angle de la ligne, une longueur

    OUTPUT:
    objet ligne
    """

    #Créer une polyligne
    ligne = gp.createObject("array")
    ligne.add(PointDebut)
    
    # Détermine le point de fin selon
    PointFin = gp.createObject("Point")
    PointFin.x = PointDebut.x - math.sin(arcTan)* longueurLigne
    PointFin.y = PointDebut.y - math.cos(arcTan)* longueurLigne

    ligne.add(PointFin)
    
    return ligne

def DistanceEntreDeuxPoints(PointDebut, PointFin):
    import math
    """Retourne la distance entre deux points.

    INPUTS:
    point de début et point de fin

    OUTPUT:
    distance
    """
    
    distance = math.sqrt((PointDebut.x - PointFin.x)**2 + (PointDebut.y - PointFin.y)**2)

    return distance

def ArcTanEntreDeuxPoints(PointDebut, PointFin):
    import math
    """Retourne l'arc tan entre deux points.

    INPUTS:
    point de début et point de fin

    OUTPUT:
    arcTan
    """
    
    arcTan = math.atan2((PointDebut.x - PointFin.x),(PointDebut.y - PointFin.y))
    
    return arcTan

def DistanceRelative(Distance, Pourcentage):
    """Retourne la distance issue du pourcentage souhaitée.

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
    Nom de la classe d'entités et du champ

    OUTPUT:
    Retourne String ppour une TXT et LONG pour des chiffres
    """
    # Process: Détermine le type du champ
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
    print "\n" + "Utilisation de ArcGIS 9.2 ou supérieure avec arcgisscripting..." + "\n"
    gp.AddMessage("\n" + "Utilisation de ArcGIS 9.2 ou supérieure avec arcgisscripting..." + "\n")
except:
    #pour les utilisateurs ArcGIS 9.0/9.1
    import win32com.client
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
    print "\n" + "Utilisation de ArcGIS 9.0/9.1 ou supérieure avec win32com.client.Dispatch..." + "\n"
    gp.AddMessage("\n" + "Utilisation de ArcGIS 9.0/9.1 ou supérieure avec win32com.client.Dispatch..." + "\n")
    
gp.overwriteoutput = 1

# Paramètre en entrée
inCenter = gp.GetParameterAsText(0)             ## A CHANGER ##
inFieldCenter = gp.GetParameterAsText(1)        ## A CHANGER ##
inBorder = gp.GetParameterAsText(2)             ## A CHANGER ##
inFieldBorder = gp.GetParameterAsText(3)        ## A CHANGER ##
inDimension = gp.GetParameterAsText(4)              ## A CHANGER ##
outFile = gp.GetParameterAsText(5)              ## A CHANGER ##

try:
    gp.AddMessage("*"*10)
    gp.AddMessage("Processus : Créer des oursins ...")
    
    # Process: Obtenir la reference spatiale de la couche en entrée
    sr = gp.describe(inCenter).spatialreference
    
    # Process: Créer la classe d'entité de polylignes en sortie...
    gp.CreateFeatureclass_management(os.path.dirname(outFile), os.path.basename(outFile), "POLYLINE", "", "DISABLED", "DISABLED", sr, "", "0", "0", "0")
    
    # Process: Ajouter des champs
    inFiledType = DeterminerTypeChamp(inCenter, inFieldCenter)
    gp.AddField(outFile, "ID_CENTRE", inFiledType)
    
    # Process: Mise à jour de la couche de polylignes en sortie
    iCursors = gp.insertcursor(outFile)
    
    # Process: Rechercher les points de centre
    sCursorsCen = gp.searchcursor(inCenter)
    sCursorCen = sCursorsCen.next()
    while sCursorCen:
        # Process: Récupèrer le point de début
        featCenter = sCursorCen.GetValue("Shape")
        pntCenter = featCenter.GetPart()
        #gp.AddMessage("Xd %s - Yd %s" % (str(pntCenter.x), str(pntCenter.y)))
                
        # Process: Détermine le type de FC pour gestion de la requete
        inFCType = isShapeFile(gp.describe(inBorder).CatalogPath)
        try: 
            if inFCType == 1:
                # Process: Détermine le type du champ
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
            # Process: Récupèrer le point de fin
            featBorder = sCursorSel.GetValue("Shape")
            pntBorder = featBorder.GetPart()
            #gp.AddMessage("Xf %s - Yf %s" % (str(pntBorder.x), str(pntBorder.y)))
                
            # Process: Créer la polyligne
            iCursor = iCursors.newrow()
            
            if inDimension != 100:
                # Process: Récupère la longueur de la ligne
                dist = DistanceEntreDeuxPoints(pntCenter, pntBorder)
                
                # Process: Récupère x pourcentage de la longueur
                distBranche = DistanceRelative(dist, inDimension)
                
                # Process: Récupère l'arc tan de la ligne
                valeurArcTan = ArcTanEntreDeuxPoints(pntCenter, pntBorder)
                
                # Process: Créer la ligne
                iLine = CreerPolyligneSelonPoint(pntCenter, valeurArcTan, distBranche)
            else:
                # Process: Créer la ligne
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

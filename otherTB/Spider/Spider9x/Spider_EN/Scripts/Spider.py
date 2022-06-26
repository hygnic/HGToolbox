# -*- coding: cp1252 -*-
""" 
Spider.py

Auteur : esri France fprally

Date: 08/27/2009

Description : Create line from Fclass center (origin) to Fclass border (destination) using ID field.
               
Parameters list :
                                Parameters properties
           Name                         Data type          Type      Direction Multiple value Default    Filter    Obtain from
argv[1]   Input center                  Feature layer      Required  Input     No              
argv[2]   ID Field center               Field              Required  Input     No                         Yes       center
argv[3]   Input borber                  Feature layer      Required  Input     No
argv[4]   ID Field borber               Field              Required  Input     No                         Yes       borber
argv[5]   Relative length of the line %                    Required  Input     No               100       range 1 to 100
argv[6]   Output line                   Feature class      Required  Output    No
 ----------------------------------------------------------------------
"""
# Import system modules
import os

def CreateLine(firstPoint, endPoint):
    """Create line object using first point and end point

    INPUTS:
    first point, end point

    OUTPUT:
    line object
    """

    #Create line
    line = gp.createObject("array")
    line.add(firstPoint)
    line.add(endPoint)
    
    return line

def CreateLineUsingPoint(firstPoint, arcTan, lineLength):
    import math
    """Retourne un objet ligne à partir du point de début, un angle et une longueur.

    INPUTS:
    first point, end point, length

    OUTPUT:
    line object
    """

    #Create line
    line = gp.createObject("array")
    line.add(firstPoint)
    
    #Calculate end point
    endPoint = gp.createObject("Point")
    endPoint.x = firstPoint.x - math.sin(arcTan)* lineLength
    endPoint.y = firstPoint.y - math.cos(arcTan)* lineLength

    line.add(endPoint)
    
    return line

def DistanceBetween2Points(firstPoint, endPoint):
    import math
    """Calculate distance between two points.

    INPUTS:
    first point, end point

    OUTPUT:
    distance
    """
    
    distance = math.sqrt((firstPoint.x - endPoint.x)**2 + (firstPoint.y - endPoint.y)**2)

    return distance

def ArcTanBetween2points(firstPoint, endPoint):
    import math
    """Calculate arc tan between two points.

    INPUTS:
    first point, end point

    OUTPUT:
    arcTan
    """
    
    arcTan = math.atan2((firstPoint.x - endPoint.x),(firstPoint.y - endPoint.y))
    
    return arcTan

def RelativeDistance(Distance, Percent):
    """Calculate relative distance using percent.

    INPUTS:
    distance

    OUTPUT:
    50 percent of the distance
    """
    RelativeDistance = (float((Distance)) * float(Percent))/100
    
    return RelativeDistance

def GetFieldType(inFeatureClass, fieldName):
    """Return field type: text or numeric

    INPUTS:
    Feature class and field

    OUTPUT:
    Return String for field TXT and LONG for numeric
    """
    # Process: get field type
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
    #for ArcGIS 9.2/9.3 users
    import arcgisscripting
    gp = arcgisscripting.create()
    print "\n" + "For ArcGIS 9.2 or higher using arcgisscripting..." + "\n"
    gp.AddMessage("\n" + "For ArcGIS 9.2 or higher using arcgisscripting..." + "\n")
except:
    #for ArcGIS 9.0/9.1 users
    import win32com.client
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
    print "\n" + "For ArcGIS 9.0/9.1 or higher using win32com.client.Dispatch..." + "\n"
    gp.AddMessage("\n" + "For ArcGIS 9.0/9.1 or higher using win32com.client.Dispatch..." + "\n")
    
gp.overwriteoutput = 1

# Input parameters
inCenter = gp.GetParameterAsText(0)             
inFieldCenter = gp.GetParameterAsText(1)       
inBorder = gp.GetParameterAsText(2)            
inFieldBorder = gp.GetParameterAsText(3)        
inDimension = gp.GetParameterAsText(4)             
outFile = gp.GetParameterAsText(5)             

try:
    gp.AddMessage("*"*10)
    gp.AddMessage("Process: Spider ...")
    
    # Process: Get input spatial reference
    sr = gp.describe(inCenter).spatialreference
    
    # Process: Create output feature class...
    gp.CreateFeatureclass_management(os.path.dirname(outFile), os.path.basename(outFile), "POLYLINE", "", "DISABLED", "DISABLED", sr, "", "0", "0", "0")
    
    # Process: Add fields
    inFiledType = GetFieldType(inCenter, inFieldCenter)
    gp.AddField(outFile, "ID_CENTER", inFiledType)
    
    # Process: Insert geometry in line layer
    iCursors = gp.insertcursor(outFile)
    
    # Process: Search center points
    sCursorsCen = gp.searchcursor(inCenter)
    sCursorCen = sCursorsCen.next()
    while sCursorCen:
        # Process: Get first point
        featCenter = sCursorCen.GetValue("Shape")
        pntCenter = featCenter.GetPart()
        #gp.AddMessage("Xd %s - Yd %s" % (str(pntCenter.x), str(pntCenter.y)))
                
        # Process: Prepare sql query
        inFCType = isShapeFile(gp.describe(inBorder).CatalogPath)
        try: 
            if inFCType == 1:
                # Process: Search field type
                if GetFieldType(inBorder, inFieldBorder) == "TEXT":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
                elif GetFieldType(inBorder, inFieldBorder) == "LONG":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + str(sCursorCen.GetValue(inFieldCenter)))
                else:
                    gp.AddMessage("Error field type is SHP")
            elif inFCType == 0:
                if GetFieldType(inBorder, inFieldBorder) == "TEXT":             
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
                elif GetFieldType(inBorder, inFieldBorder) == "LONG":
                    sCursorsSel = gp.searchcursor(inBorder, '"' + inFieldBorder + '" = ' + str(sCursorCen.GetValue(inFieldCenter)))
                else:
                    gp.AddMessage("Error field type is GeoDatabase")
        except:
            if GetFieldType(inBorder, inFieldBorder) == "TEXT":             
                sCursorsSel = gp.searchcursor(inBorder, '[' + inFieldBorder + '] = ' + "'" + sCursorCen.GetValue(inFieldCenter) + "'")
            elif GetFieldType(inBorder, inFieldBorder) == "LONG":
                sCursorsSel = gp.searchcursor(inBorder, '[' + inFieldBorder + '] = ' + str(sCursorCen.GetValue(inFieldCenter)))
            else:
                gp.AddMessage("Error field type for version 9.1")
              
#        # version 9.3
#        delimitedfield = gp.AddFieldDelimiters(inBorder, inFieldBorder)
#        sCursorsSel = gp.searchcursor(inBorder, delimitedfield + " = " + str(sCursorCen.GetValue(inFieldCenter)))
        
        sCursorSel = sCursorsSel.next()
        while sCursorSel:
            # Process: Get end point
            featBorder = sCursorSel.GetValue("Shape")
            pntBorder = featBorder.GetPart()
            #gp.AddMessage("Xf %s - Yf %s" % (str(pntBorder.x), str(pntBorder.y)))
                
            # Process: Create line
            iCursor = iCursors.newrow()
            
            if inDimension != 100:
                # Process: Get line length
                dist = DistanceBetween2Points(pntCenter, pntBorder)
                
                # Process: Get x percent of length
                distBranche = RelativeDistance(dist, inDimension)
                
                # Process: get arc tan of the line
                valeurArcTan = ArcTanBetween2points(pntCenter, pntBorder)
                
                # Process: Create relative line
                iLine = CreateLineUsingPoint(pntCenter, valeurArcTan, distBranche)
            else:
                # Process: Create line
                iLine = CreateLine(pntCenter, pntBorder)
            
            # Process: store line
            iCursor.shape = iLine
            iCursor.ID_CENTER = sCursorCen.GetValue(inFieldCenter)
            iCursors.insertrow(iCursor)
            iLine.removeall()
            sCursorSel = sCursorsSel.next()
            
        sCursorCen = sCursorsCen.next()
    
    # Vide les variables
    del iCursors, sCursorsCen, sCursorCen, sCursorsSel, sCursorSel
    
    gp.AddMessage("end process")
    gp.AddMessage("*"*10)
    
except:
    gp.AddMessage(gp.GetMessages(2))
    print gp.GetMessages(2)

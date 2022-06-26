'''----------------------------------------------------------------------------------
 Tool Name:   Network Sampling
 Source Name: networksamp.py
 Author:      Vini Indriasari
 Required Arguments:
              Input line feature class
              Output sample points feature class
              Spacing between sample points
              Direction to generate sample points
 Description: Generate sample points along the lines on a network.
 Date:        January 2014
----------------------------------------------------------------------------------'''

import arcpy

# workspace for temporary fc
from arcpy import env
env.workspace = "C:/temp"
#env.workspace = arcpy.GetSystemEnvironment("TEMP")
env.overwriteOutput = True

#####################################################################################
# Parameters
#####################################################################################

# Input feature class containing linear features
infc = arcpy.GetParameterAsText(0)

# Output feature class to store sample points
sampfc = arcpy.GetParameterAsText(1)

# Spacing between sample points
sp = arcpy.GetParameter(2)

# Direction to generate sample points: FT, TF
flow = arcpy.GetParameterAsText(3)
# FT (From-To): in digitized direction of the line
# TF (To-From): against digitized direction of the line

#####################################################################################
# Generate sample points
#####################################################################################

samp = []

# Create cursor to search stream features
cur = arcpy.da.SearchCursor(infc, (["SHAPE@"]))

for row in cur:
  # Get stream geometry from cursor
  stream = row[0] # Polyline
  
  if flow.upper() == "FT":
    # Define a position on the stream where to stop generating cross points
    dmax = stream.length
    d = 0 # distance d starts from the start point of the line
      
    # Create cross points along the stream at regular interval
    while d < dmax:
      # Get position of a point at distance d
      cross = stream.positionAlongLine(d) # PointGeometry
      samp.append(cross) # add cross point into the list
      d += sp # increase the distance by spacing
      
  else: # flow = TF
    # Define a position on the stream where to stop generating cross points
    dmin = 0
    d = stream.length # distance d starts from the end point of the line
      
    # Create cross points along the stream at regular interval
    while d > dmin:
      # Get position of a point at distance d
      cross = stream.positionAlongLine(d) # PointGeometry
      samp.append(cross) # add cross point into the list
      d -= sp # decrease the distance by spacing
      
del cur # delete cursor

if any(samp):
  arcpy.CopyFeatures_management(samp, sampfc)
else:
  arcpy.AddError("No sample points created.")
  

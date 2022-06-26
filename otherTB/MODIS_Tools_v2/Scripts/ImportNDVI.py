#Import modules
import ftplib
import re
import arcpy
arcpy.CheckOutExtension("spatial")
from arcpy import env
from arcpy.sa import *
from os import path
import sys
import calendar
import datetime
from datetime import date
import tempfile
import urllib2
import ALFlib
import shutil

#Set Parameters
date_string = arcpy.GetParameterAsText(0)  #MM/YYYY
save_path = arcpy.GetParameterAsText(1)    #output location and filename
tile_name = arcpy.GetParameterAsText(2)    #hXXvYY
area = arcpy.GetParameter(3)               #area of interest
sat_name = arcpy.GetParameterAsText(4)     #Terra or Aqua
scratch = tempfile.mkdtemp()
home = path.realpath(__file__).split('Scripts')[0]

#Parse Date
d = date_string.split("/")
m = d[0].rjust(2,'0')                                       #month
yr = d[1]                                                   #year
f = date(int(yr),int(m),1)
DOY = str(f.timetuple().tm_yday).rjust(3,'0')               #day of year

#Convert into NASA terminology
if sat_name == "Terra":
        sat_prefix = "MOD"
        sat_folder = "MOLT"
        s = "T"
elif sat_name == "Aqua":
        sat_prefix = "MYD"
        sat_folder = "MOLA"
        s= "A"

def DownloadRoutine(tile):
    """Downloads files"""
    hdf_pattern = re.compile(sat_prefix + '13A3.A'+yr+DOY+'.'+ tile +'.006.*.hdf$', re.IGNORECASE)

    matched_file = ''

    for f in files:
    	if re.match(hdf_pattern,f):
    		matched_file = f
    		break
    if matched_file == '':
            arcpy.AddMessage("\n[ERROR] No data for that tile\n")
            sys.exit(0)     #Quit if there is an error in tile or date

    arcpy.AddMessage("Found: " + matched_file)

    ALFlib.getDownload(path.join(source,matched_file), path.join(scratch, matched_file), userName='MODIS_Toolbox',
                       password='E1rthData', authentication="https://urs.earthdata.nasa.gov" )

    #Extract the correct variable
    return arcpy.ExtractSubDataset_management(path.join(scratch, matched_file), path.join(scratch, tile+m+yr), "0")


#Get List of files avilable for that date
source = "http://e4ftl01.cr.usgs.gov/"+sat_folder+"/"+sat_prefix+"13A3.006/" +yr+ "." +m+ ".01/"
webFile = path.join(scratch, "earthdata.html")

files = []

try:
    if ALFlib.getDownload(source, webFile):
        page = open( webFile).read()
        files = []
        for url in page.split( '<a href="'):
            link = url.split( '">', 1)[0]
            if link.endswith( 'hdf'):
                files.append( link.split("/")[-1])
except urllib2.HTTPError:
    arcpy.AddMessage("\n[ERROR] No data for that date\n")
    sys.exit()


#Figure out which tiles overlap area of interest
tiles = []
tiffs = []

if tile_name:
    tiles.append(tile_name)
elif str(area):
    grid = arcpy.MakeFeatureLayer_management(path.join(home, 'Documentation',
                                                            'Ref.gdb','Grid.'))
    overlap = arcpy.SelectLayerByLocation_management(grid, 'INTERSECT', area)
    with arcpy.da.SearchCursor(overlap, '*') as intersection:
        for tile in intersection:
            tiles.append(tile[2])
else:
    arcpy.AddMessage('\n[ERROR] You must specify either a tile or area of interest\n')
    sys.exit()

#Download HDF files
arcpy.AddMessage("\nDownloading Files...")

for tile in tiles:
    tiffs.append(DownloadRoutine(tile))

#Stitch Them To gether
arcpy.AddMessage("\nStitching Tiles Together...")
if len(tiffs) > 1:
    temp1 = arcpy.MosaicToNewRaster_management(tiffs, scratch, 'temp1',
                                          pixel_type='16_BIT_SIGNED',
                                          number_of_bands = 1)

else:
    temp1 = tiffs[0]

#Extract area of interest
if str(area):
    try:
        temp2 = arcpy.sa.ExtractByMask(temp1, area)

    except arcpy.ExecuteError:
        arcpy.AddMessage("\n[ERROR] Specified tile does not overlap area of interest\n")
        sys.exit()

else:
    temp2 = Raster(temp1)

#Multiply by Scale Factor
temp3 = temp2*.0001
del temp2


#Reproject into Global Coordinate System
# I really wish there was a better way of doing this, but Project Raster tool
# can't seem to deal with the sinusoidal projection.
arcpy.AddMessage("\nProjecting into Goode Homolosine...\n")

gdb = arcpy.CreateFileGDB_management(scratch, "temp")
tempM = arcpy.CreateMosaicDataset_management(gdb, 'temp_mosaic',
                                     "PROJCS['World_Goode_Homolosine_Land',GEOGCS['GCS_WGS_1984',\
                                     DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                                     PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                                     PROJECTION['Goode_Homolosine'],PARAMETER['False_Easting',0.0],\
                                     PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],\
                                     PARAMETER['Option',1.0],UNIT['Meter',1.0]];-20037700 -8683400 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;\
                                     IsHighPrecision", '#', '#', 'NONE', '#')

arcpy.AddRastersToMosaicDataset_management(tempM, 'Raster Dataset', temp3, 'UPDATE_CELL_SIZES', 'UPDATE_BOUNDARY', 'NO_OVERVIEWS', '#', '0', '1500', '#', '#', 'SUBFOLDERS', 'ALLOW_DUPLICATES', 'NO_PYRAMIDS', 'CALCULATE_STATISTICS', 'NO_THUMBNAILS', '#', 'NO_FORCE_SPATIAL_REFERENCE', 'ESTIMATE_STATISTICS', '#')
output = arcpy.CopyRaster_management(tempM, save_path)

shutil.rmtree(scratch)
arcpy.SetParameter(1, output)

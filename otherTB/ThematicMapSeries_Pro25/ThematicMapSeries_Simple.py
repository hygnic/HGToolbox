# Author:  Esri
# Date:    July 2020
# Version: ArcGISPro 2.5
# Purpose: This script represents the basic steps to automate a Thematic
#          Map Series.  It toggles the visibility of group layers for each
#          page in the series and combines all pages into a single, multi
#          page PDF.
# Notes:   - The script was designed to be run from within the application
#            either loaded into the Python Window or run from a script tool
#            provided in the project.
#          - If you do NOT install into the folder below, you MUST change
#            the path.
#          - Review the README.docx for more detailed information.


import arcpy, os

#Filepath variables are machine specific. May need to change to execute sample
outputFolder = 'C:\Temp\ThematicMapSeries_Pro25'   #CHANGE if needed
pdfFileName = 'ThematicMapSeries.pdf'              #CHANGE if needed

#Reference the current project, MUST be run in the ArcGIS Pro application
p = arcpy.mp.ArcGISProject('current')

#Reference the appropriate map and layout
m = p.listMaps('Thematic Map')[0]
lyt = p.listLayouts("Thematic Map Series")[0]

#Create a new PDF pages will be appended into
#First remove the file if it already exists
if os.path.exists(os.path.join(outputFolder, pdfFileName)):
  os.remove(os.path.join(outputFolder, pdfFileName))
pdf = arcpy.mp.PDFDocumentCreate(os.path.join(outputFolder, pdfFileName))

#Create a list the represents the order of pages in the final output
#Each item in the list is the name of a group layer (page) to be exported
pageGroupList = ['Parcel Use', 'Public Lands', 'Rural Lands',
                 'Improved Structures', 'Improved Structure Values',
                 'Land Value', 'Tax Exempt Property', 'Mineral Lands']

#Iterate through each page in the list
for pageName in pageGroupList:

  #Iterate through each layer in the map
  for l in m.listLayers():

    #Group layer check. Only toggle visibility of group layers
    #This means the Parcels layer and the basemap layers at the
    #root level of the contents pane will always be visible
    if l.isGroupLayer:

      #If the group layer name is the correct pageName, then make visible
      #Otherwise toggle all other gropu layers off
      if l.name == pageName:     
        l.visible = True
      else:
        l.visible = False
  #Export each page and append into the new PDF document
  print('Exporting and appending: ' + pageName)
  lyt.exportToPDF(os.path.join(outputFolder, pageName +  '.pdf'))
  pdf.appendPages(os.path.join(outputFolder, pageName +  '.pdf'))

  #Remove the single, exported page after appended into final PDF
  os.remove(os.path.join(outputFolder, pageName + '.pdf'))

#Complete the creation of the PDF and commit to file
pdf.saveAndClose()

#Open the resulting file
os.startfile(os.path.join(outputFolder, pdfFileName))

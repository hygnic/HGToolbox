Create Triangular graph in ArcGIS
- contains two scripts to create and classify data and one script to create a grid in triangular

Requirements:
- ArcGIS 10 or 10.1
- basic knowledges of GIS
- advanced knowledges of input data and triangular graph

How to use:

1. run first script (1. Plot Points)
 - choose your data in Input layer box (supported: Shapefile, Feature Class)
 - choose three parts of phenomenon
 - set output point layer
 - Optionaly set base triangle (recommended for first usage) and auxiliary lines (for average percentage values, can be used in next step)

2. Set a zone polygon layer
Important step for classification. Zone layer defines a inner structure of triangle.
The second script (2. Classification) uses this polygon layer to classify input data.
There are 3 ways to determine zone layer:
 - choose from created templates
 - create new polygon layer based on auxiliary lines from first script, you can use snapping features
 - create new polygon layer based on own knowledge

Note: 	If you create your own zones it's recommended to use Create grid script,
that generates a grid layer for snapping purpose.
	If you create your own zones it's also necessary to create new "class" field in new zone layer.

3. run second script (2. Classification)
 - choose a zone layer that contains zones and "class" field
 - choose "class" field into Category field dropdown menu
 - set plotted point created in step 1
 - set name of new field to write classification data to original layer (it's recommended to use same name as "class" field from zones layer)
 - choose your original data used in Input layer box in first script

You data are classified and you can use new field to set Symbology color.
To set triangular graph as legend insert new Data Frame into project and move triangular graph layers to new Data Frame.
It's recommended to set color in triangle zones first then import color scheme to your layer based on same field name.


--
2014
Sukhdorj Ganbaatar | s.ganbaatar@seznam.cz
Zdena Dobešová | zdena.dobesova@upol.cz
Department of Geoinformatics, Olomouc CZ
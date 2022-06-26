# ArcGis Toolbox: Generate Cross Section
# Converts the 2D image of a cross section into a 3D oject that can be displayed in ArcScene
# Autor: Riccardo Rocca - riccardo.rocca@hotmail.com - 2014

import arcpy, os, Image, sys

# Generates the "geometry" portion of the COLLADA model
def geometry_model(I, X1, X2, Y1, Y2, Z_top, Z_bottom):
  model = (
          '		<geometry id="ID_1.dae%s">\n'
          '			<mesh>\n'
          '				<source id="ID_1.dae%s-positions">\n'
          '					<float_array id="ID_1.dae%s-positions-array" count="12">%s %s %s %s %s %s %s %s %s %s %s %s</float_array>\n'
          '					<technique_common>\n'
          '						<accessor count="4" source="#ID_1.dae%s-positions-array" stride="3">\n'
          '							<param name="X" type="float"/>\n'
          '							<param name="Y" type="float"/>\n'
          '							<param name="Z" type="float"/>\n'
          '						</accessor>\n'
          '					</technique_common>\n'
          '				</source>\n'
          '				<source id="ID_1.dae%s-normals">\n'
          '					<float_array id="ID_1.dae%s-normals-array" count="3">0 0 1</float_array>\n'
          '					<technique_common>\n'
          '						<accessor count="1" source="#ID_1.dae%s-normals-array" stride="3">\n'
          '							<param name="X" type="float"/>\n'
          '							<param name="Y" type="float"/>\n'
          '							<param name="Z" type="float"/>\n'
          '						</accessor>\n'
          '					</technique_common>\n'
          '				</source>\n'
          '				<source id="ID_1.dae%s-uv">\n'
          '					<float_array id="ID_1.dae%s-uv-array" count="8">1 1 0 1 1 0 0 0</float_array>\n'
          '					<technique_common>\n'
          '						<accessor count="4" source="#ID_1.dae%s-uv-array" stride="2">\n'
          '							<param name="S" type="float"/>\n'
          '							<param name="T" type="float"/>\n'
          '						</accessor>\n'
          '					</technique_common>\n'
          '				</source>\n'
          '				<vertices id="ID_1.dae%s-vertices">\n'
          '					<input semantic="POSITION" source="#ID_1.dae%s-positions"/>\n'
          '				</vertices>\n'
          '				<triangles count="2" material="ID_1.dae%smaterial">\n'
          '					<input offset="0" semantic="VERTEX" source="#ID_1.dae%s-vertices" set="0"/>\n'
          '					<input offset="1" semantic="NORMAL" source="#ID_1.dae%s-normals" set="0"/>\n'
          '					<input offset="2" semantic="TEXCOORD" source="#ID_1.dae%s-uv" set="0"/>\n'
          '					<p>1 0 1 0 0 0 2 0 2 2 0 2 3 0 3 1 0 1</p>\n'
          '				</triangles>\n'
          '			</mesh>\n'
          '		</geometry>\n'
          ) % (I, I, I, X2, Y2, Z_top, X1, Y1, Z_top, X2, Y2, Z_bottom, X1, Y1, Z_bottom, I, I, I, I, I, I, I, I, I, I, I, I, I)
  return model

# Generates the "image" portion of the COLLADA model
def image_model(I, image):
  model = (
          '		<image id="ID_1.dae%simg" height="0" width="0">\n'
          '			<init_from>%s</init_from>\n'
          '		</image>\n'
          ) % (I, image)
  return model

# Generates the "effect" portion of the COLLADA model
def effect_model(I):
  model = (
          '		<effect id="ID_1.dae%seffect">\n'
          '			<profile_COMMON>\n'
          '				<newparam sid="surface">\n'
          '					<surface type="2D">\n'
          '						<init_from>ID_1.dae%simg</init_from>\n'
          '					</surface>\n'
          '				</newparam>\n'
          '				<newparam sid="sampler">\n'
          '					<sampler2D>\n'
          '						<source>surface</source>\n'
          '						<minfilter>LINEAR_MIPMAP_LINEAR</minfilter>\n'
          '						<magfilter>LINEAR</magfilter>\n'
          '					</sampler2D>\n'
          '				</newparam>\n'
          '				<technique sid="common">\n'
          '					<phong>\n'
          '						<diffuse>\n'
          '							<texture texture="sampler" texcoord="uv0"/>\n'
          '						</diffuse>\n'
          '					</phong>\n'
          '				</technique>\n'
          '			</profile_COMMON>\n'
          '		</effect>\n'
          ) % (I, I)
  return model

# Generates the "material" portion of the COLLADA model
def material_model(I):
  model = (
          '		<material id="ID_1.dae%smaterial">\n'
          '			<instance_effect url="#ID_1.dae%seffect"/>\n'
          '		</material>\n'
          ) % (I, I)
  return model

# Generates the "instance" portion of the COLLADA model
def instance_model(I):
  model = (
          '				<instance_geometry url="#ID_1.dae%s">\n'
          '					<bind_material>\n'
          '						<technique_common>\n'
          '							<instance_material symbol="ID_1.dae%smaterial" target="#ID_1.dae%smaterial">\n'
          '								<bind_vertex_input semantic="uv0" input_semantic="TEXCOORD" input_set="0"/>\n'
          '							</instance_material>\n'
          '						</technique_common>\n'
          '					</bind_material>\n'
          '				</instance_geometry>\n'
          ) % (I, I, I)
  return model

try:
  # Get the input parameters
  input_line = arcpy.GetParameterAsText(0)
  line_ID = arcpy.GetParameterAsText(1)
  image_file = arcpy.GetParameterAsText(2)
  orientation = arcpy.GetParameterAsText(3)
  crop = arcpy.GetParameterAsText(4)
  margin_left = int(arcpy.GetParameterAsText(5))
  margin_right = int(arcpy.GetParameterAsText(6))
  margin_top = int(arcpy.GetParameterAsText(7))
  margin_bottom = int(arcpy.GetParameterAsText(8))
  Z_top = float(arcpy.GetParameterAsText(9))
  Z_bottom = float(arcpy.GetParameterAsText(10))
  output_section = arcpy.GetParameterAsText(11)

  if (Z_bottom - Z_top) == 0:
    arcpy.AddError("Cannot proceed. Z range = 0")
    exit()

  fileExtension = os.path.splitext(image_file)[1]

  # Extracts the X,Y coordinates of the baseline with the selected FID
  X = []
  Y = [] 
  for row in arcpy.da.SearchCursor(input_line, ["OID@", "SHAPE@"]):
    if row[0] == int(line_ID):
      for part in row[1]:
        for pnt in part:
          if pnt:
            X.append(pnt.X)
            Y.append(pnt.Y)
        break
      break

  # Calculates:
  # - the total length of the baseline
  # - the distance of the start and end of each baseline segment from the beginning of the baseline
  baseline_length = 0
  segment_start = []
  segment_end = []
  for i in xrange(len(X)-1):
    segment_length = math.hypot((X[i] - X[i+1]), (Y[i] - Y[i+1]))
    segment_start.append(baseline_length)
    baseline_length += segment_length
    segment_end.append(baseline_length)
  if baseline_length == 0:
    arcpy.AddError("Cannot proceed. Baseline length = 0")
    exit()
  if (segment_end[0] - segment_start[0]) == 0:
    arcpy.AddError("Cannot proceed. Baseline first segment = 0")
    exit()
  if (segment_end[-1] - segment_start[-1]) == 0:
    arcpy.AddError("Cannot proceed. Baseline last segment = 0")
    exit()

  # Opens the image and calculates hight and width
  image = Image.open(image_file)
  image_w, image_h = image.size
  if (image_w - margin_left - margin_right) == 0:
    arcpy.AddError("Cannot proceed. Image width within margins = 0")
    exit()
  if (image_h - margin_top - margin_bottom) == 0:
    arcpy.AddError("Cannot proceed. Image height within margins = 0")
    exit()
  ratio_w = baseline_length / (image_w - margin_left - margin_right)
  ratio_h = (Z_bottom - Z_top) / (image_h - margin_top - margin_bottom)

  # Crops the image if the "crop" option is set
  if crop == "crop":
    image = image.crop((margin_left, margin_top, image_w - margin_right, image_h - margin_bottom))
    image_w, image_h = image.size
    margin_left = 0
    margin_right = 0
    margin_top = 0
    margin_bottom = 0


  # Flips the image depending on its orientation
  Xmid = (X[0] + X[-1]) / 2
  Ymid = (Y[0] + Y[-1]) / 2
  Radius = math.hypot((X[0] - X[-1]), (Y[0] - Y[-1])) / 2
  RadiusProjected = Radius * math.sqrt(2)
  if orientation == "N-S":
    Xorientation = Xmid
    Yorientation = Ymid + Radius
  elif orientation == "NW-SE":
    Xorientation = Xmid - RadiusProjected
    Yorientation = Ymid + RadiusProjected
  elif orientation == "W-E":
    Xorientation = Xmid - Radius
    Yorientation = Ymid
  elif orientation == "SW-NE":
    Xorientation = Xmid - RadiusProjected
    Yorientation = Ymid - RadiusProjected
  elif orientation == "S-N":
    Xorientation = Xmid
    Yorientation = Ymid - Radius
  elif orientation == "SE-NW":
    Xorientation = Xmid + RadiusProjected
    Yorientation = Ymid - RadiusProjected
  elif orientation == "E-W":
    Xorientation = Xmid + Radius
    Yorientation = Ymid
  elif orientation == "NE-SW":
    Xorientation = Xmid + RadiusProjected
    Yorientation = Ymid + RadiusProjected
  if (math.hypot((Xorientation - X[0]), (Yorientation - Y[0])) > math.hypot((Xorientation - X[-1]), (Yorientation - Y[-1]))):
    margin_left, margin_right = margin_right, margin_left
    image = image.transpose(Image.FLIP_LEFT_RIGHT)

  # Extends X,Y of first and last point, up to the image left and right edges
  X[0] = X[0] + (X[0] - X[1]) * margin_left * ratio_w / (segment_end[0] - segment_start[0])
  Y[0] = Y[0] + (Y[0] - Y[1]) * margin_left * ratio_w / (segment_end[0] - segment_start[0])
  X[-1] = X[-1] + (X[-1] - X[-2]) * margin_right * ratio_w / (segment_end[-1] - segment_start[-1])
  Y[-1] = Y[-1] + (Y[-1] - Y[-2]) * margin_right * ratio_w / (segment_end[-1] - segment_start[-1])

  # Recalculates Z_top and Z_bottom
  Z_top = Z_top - margin_top * ratio_h
  Z_bottom = Z_bottom + margin_bottom * ratio_h

  # Generates a series of temporary images corresponding to the series of segments in the baseline
  for i in xrange(len(X)-1):
    if i == 0:
      image_start = 0
    else:
      image_start = margin_left + int(round(segment_start[i] / ratio_w))
    if i == len(X)-2:
      image_end = image_w
    else:
      image_end = margin_left + int(round(segment_end[i] / ratio_w))
    image.crop((image_start, 0, image_end, image_h)).save("./tmp.dae"+str(i)+fileExtension)

  # Generates the various portions of the COLLADA model, one for each baseline segment
  geometry_library = ""
  image_library = ""
  effect_library = ""
  material_library = ""
  instance_library = ""
  for i in xrange(len(X)-1):
    geometry_library += geometry_model(str(i), X[i], X[i+1], Y[i], Y[i+1], Z_top, Z_bottom)
    image_library += image_model(str(i), "./tmp.dae"+str(i)+fileExtension)
    effect_library += effect_model(str(i))
    material_library += material_model(str(i))
    instance_library += instance_model(str(i))

  # Merges the various portions and generate the complete COLLADA model
  model = (
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">\n'
          '	<asset>\n'
          '		<up_axis>Z_UP</up_axis>\n'
          '	</asset>\n'
          '\n'
          '	<library_geometries>\n'
          '             %s\n'
          '	</library_geometries>\n'
          '\n'
          '	<library_images>\n'
          '             %s\n'
          '	</library_images>\n'
          '\n'
          '	<library_effects>\n'
          '             %s\n'
          '	</library_effects>\n'
          '\n'
          '	<library_materials>\n'
          '             %s\n'
          '	</library_materials>\n'
          '\n'
          '	<library_visual_scenes>\n'
          '		<visual_scene id="Multipatch-Converted-Scene">\n'
          '			<node id="ID_1.dae">\n'
          '				<translate>0 0 0</translate>\n'
          '                             %s\n'
          '			</node>\n'
          '		</visual_scene>\n'
          '	</library_visual_scenes>\n'
          '\n'
          '	<scene>\n'
          '		<instance_visual_scene url="#Multipatch-Converted-Scene"/>\n'
          '	</scene>\n'
          '</COLLADA>\n'
          ) % (geometry_library, image_library, effect_library, material_library, instance_library)

  # Saves the COLLADA model in a temporary file "tmp.dae"
  f = open("./tmp.dae","w")
  f.write(model)
  f.close()

  # Load the COLLADA model, including the coordinate system of the baseline 
  spatial_ref = arcpy.Describe(input_line).spatialReference
  arcpy.Import3DFiles_3d("./tmp.dae", output_section, "", spatial_ref)

  # Deletes all the temporary files
  os.remove("./tmp.dae")
  for i in xrange(len(X)-1):
    os.remove("./tmp.dae"+str(i)+fileExtension)

  # Report a success message    
  arcpy.AddMessage("All done!")
 
except:
  # Report an error messages
  arcpy.AddError("Could not complete the script")
  #arcpy.AddMessage(arcpy.GetMessages())



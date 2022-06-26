using System;
using System.Collections;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Editor;
using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Geodatabase;

namespace CutPolygonsWithoutSelection
{
  public partial class CutPolygonsWithoutSelectionTool : ESRI.ArcGIS.Desktop.AddIns.Tool, IShapeConstructorTool, ISketchTool
  {
    private IEditor3 m_editor;
    private IEditEvents_Event m_editEvents;
    private IEditEvents5_Event m_editEvents5;
    private IEditSketch3 m_edSketch;
    private IEditLayers m_editLayers;
    private IShapeConstructor m_csc;

    public CutPolygonsWithoutSelectionTool()
    {
      // Get the editor
      m_editor = ArcMap.Editor as IEditor3;
      m_editEvents = m_editor as IEditEvents_Event;
      m_editEvents5 = m_editor as IEditEvents5_Event;
      m_editLayers = m_editor as IEditLayers;
    }

    protected override void OnUpdate()
    {
      Enabled = m_editor.EditState == esriEditState.esriStateEditing;
    }

    protected override void OnActivate()
    {
      m_edSketch = m_editor as IEditSketch3;

      //set edit task to null
      m_editor.CurrentTask = null;

      //set the edit sketch geometry to line to force line shape consructors.
      m_edSketch.GeometryType = esriGeometryType.esriGeometryPolyline;

      // Activate a shape constructor based on the current sketch geometry
      if (m_edSketch.GeometryType == esriGeometryType.esriGeometryPoint | m_edSketch.GeometryType == esriGeometryType.esriGeometryMultipoint)
        m_csc = new PointConstructorClass();
      else
        m_csc = new StraightConstructorClass();

      m_csc.Initialize(m_editor);
      m_edSketch.ShapeConstructor = m_csc;
      m_csc.Activate();

      // Setup events
      m_editEvents.OnSketchModified += OnSketchModified;
      m_editEvents5.OnShapeConstructorChanged += OnShapeConstructorChanged;
      m_editEvents.OnSketchFinished += OnSketchFinished;

    }

    protected override bool OnDeactivate()
    {
      m_editEvents.OnSketchModified -= OnSketchModified;
      m_editEvents5.OnShapeConstructorChanged -= OnShapeConstructorChanged;
      m_editEvents.OnSketchFinished -= OnSketchFinished;
      return true;
    }

    protected override void OnDoubleClick()
    {
      if (Control.ModifierKeys == Keys.Shift)
      {
        // Finish part
        ISketchOperation pso = new SketchOperation();
        pso.MenuString_2 = "Finish Sketch Part";
        pso.Start(m_editor);
        m_edSketch.FinishSketchPart();
        pso.Finish(null);
      }
      else
        m_edSketch.FinishSketch();
    }

    private void OnSketchModified()
    {
      m_csc.SketchModified();
    }

    private void OnShapeConstructorChanged()
    {
      // Activate a new constructor
      m_csc.Deactivate();
      m_csc = null;
      m_csc = m_edSketch.ShapeConstructor;
      if (m_csc != null)
        m_csc.Activate();
    }

    private void OnSketchFinished()
    {
      bool hasCutPolygons = false;
      try
      {
        //Get the geometry that performs the cut from the edit sketch.
        IGeometry cutGeometry = m_edSketch.Geometry;

        //The sketch geometry is simplified to deal with a multi-part sketch as well
        //as the case where the sketch loops back over itself.
        ITopologicalOperator2 topoOperator = cutGeometry as ITopologicalOperator2;
        topoOperator.IsKnownSimple_2 = false;
        topoOperator.Simplify();

        //Create the spatial filter to search for features in the target feature class.
        //The spatial relationship we care about is whether the interior of the line 
        //intersects the interior of the polygon.
        ISpatialFilter spatialFilter = new SpatialFilterClass();
        spatialFilter.Geometry = m_edSketch.Geometry;
        spatialFilter.SpatialRel = esriSpatialRelEnum.esriSpatialRelIntersects;

        //Find the polygon features that cross the sketch.
        IFeatureClass featureClass = m_editLayers.CurrentLayer.FeatureClass;
        IFeatureCursor featureCursor = featureClass.Search(spatialFilter, false);

        //Only do work if there are features that intersect the edit sketch.
        IFeature origFeature = featureCursor.NextFeature();
        if (origFeature != null)
        {
          //Check the first feature to see if it is ZAware and if it needs to make the
          //cut geometry ZAware.
          IZAware zAware = origFeature.Shape as IZAware;
          if (zAware.ZAware)
          {
            zAware = cutGeometry as IZAware;
            zAware.ZAware = true;
          }

          ArrayList comErrors = new ArrayList();

          //Start an edit operation so we can have undo/redo.
          m_editor.StartOperation();

          //Cycle through the features, cutting with the sketch.
          while (origFeature != null)
          {
            try
            {
              //Split the feature. Use the IFeatureEdit::Split method which ensures
              //the attributes are correctly dealt with.
              IFeatureEdit featureEdit = origFeature as IFeatureEdit;
              //Set to hold the new features that are created by the Split.            
              ISet newFeaturesSet = featureEdit.Split(cutGeometry);

              //New features have been created.
              if (newFeaturesSet != null)
              {
                newFeaturesSet.Reset();
                hasCutPolygons = true;
              }
            }
            catch (COMException comExc)
            {
              //comErrors.Add(String.Format("OID: {0}, Error: {1} , {2}", origFeature.OID.ToString(), comExc.ErrorCode, comExc.Message));
            }
            finally
            {
              //Continue to work on the next feature if it fails to split the current one.
              origFeature = featureCursor.NextFeature();
            }
          }
          //If any polygons were cut, refresh the display and stop the edit operation.
          if (hasCutPolygons)
          {
            //Clear the map's selection.
            m_editor.Map.ClearSelection();

            //Refresh the display including modified layer and any previously selected component. 
            IActiveView activeView = m_editor.Map as IActiveView;
            activeView.PartialRefresh(esriViewDrawPhase.esriViewGeography | esriViewDrawPhase.esriViewGeoSelection, null, activeView.Extent);

            //Complete the edit operation.
            m_editor.StopOperation("Cut Polygons Without Selection");
          }
          else
          {
            m_editor.AbortOperation();
          }

          //report any errors that have arisen while splitting features
          if (comErrors.Count > 0)
          {
            StringBuilder stringBuilder = new StringBuilder("The following features could not be split: \n", 200);
            foreach (string comError in comErrors)
            {
              stringBuilder.AppendLine(comError);
            }

            MessageBox.Show(stringBuilder.ToString(), "Cut Errors");
          }
        }
      }
      catch (Exception e)
      {
        MessageBox.Show("Unable to perform the cut task.\n" + e.Message);
        m_editor.AbortOperation();
      }
    }
  }
}

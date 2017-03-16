# uncomment the import when running the Script standalone
import arcpy

Verbose = True

def findGoodBBSS(inputFC = r"D:\CSP7300\ModelBuilder\FER_Exercise\brwca_project.gdb\bbs_stops_2000",
                 inputGDBforOutput = r"D:\CSP7300\ModelBuilder\FER_Exercise\Scratch.gdb",
                 inputField = "hay1200",
                 Verbose = True):
    #global settings
    outWS = inputGDBforOutput
    arcpy.env.workspace = outWS
    arcpy.env.overwriteOutput = True
    # # # 1)  Open Catalog, Map, and Idle
    # # #     add the PtsBBSS, and 'brwca_rough'
    # For writing Paths...
    #   Use r"..."  for python 2
    #   Use u"..."  for python 3.  Py3 is unicode by default.
    #
    # let's make and set an output GDB
    # make it in Catalog, and then paste the path into the below
    # inputs

    ptsBBSS = inputFC

    # pull arcpy documentation for Describe object arcpy 10.4
    #  http://desktop.arcgis.com/en/arcmap/10.4/analyze/arcpy-functions/describe.htm
    #     and the FC describe properties:
    #  http://desktop.arcgis.com/en/arcmap/10.4/analyze/arcpy-functions/featureclass-properties.htm

    descBBSS = arcpy.Describe(ptsBBSS)

    descBBSS.featureType

    #print what's in fields
    descBBSS.fields

    listObjBBSSFields = descBBSS.fields

    # field Object attributes
    #  http://desktop.arcgis.com/en/arcmap/10.4/analyze/arcpy-classes/field.htm
    for fields in listObjBBSSFields:
        print fields.name

    for fields in listObjBBSSFields:
        print fields.name, fields.type

    # We are interested in the Proportions of Grass and Hay

    minGrass1200 = 999999.
    maxGrass1200 = -1.

    # we SHOULD use the DA (new skool) data access tools
    cur = arcpy.da.SearchCursor(ptsBBSS,[inputField])
    
    if Verbose:
        for rows in cur:
            print rows
        cur.reset()  #reset the reader

    # what happened?
    
    for rows in cur:

        thisGrass = rows[0]
        
        if thisGrass < minGrass1200:
            minGrass1200 = thisGrass
            if Verbose: print "Found a new min:",minGrass1200
        if thisGrass > maxGrass1200:
            maxGrass1200 = thisGrass
            if Verbose: print "Found a new max:",maxGrass1200

    midPointGrass = (maxGrass1200 - minGrass1200) * 0.5


    # # # 2)  Make the selections for our "good sites"
    #
    # we decide we are interested in the interaction of grass & hay
    # let's buffer on the sum of those
    # select layer by attribute:
    #  http://desktop.arcgis.com/en/arcmap/10.4/tools/data-management-toolbox/select-layer-by-attribute.htm
    #    from the help:
    #  The input must be a feature layer or a table view.
    #  The input __cannot be a feature class or table__.
    #  This tool works on layers or table views in the ArcMap table of contents,
    #  and also on layers or table views created in a scripts using the Make Feature Layer or Make Table View tools.
    #
    #  ??? arcpy.MakeFeatureLayer_management(ptsBBSS, "lyrPtBBSS") 
    #  try it in Map
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "bbs_stops_2000"
    # whereClause]

    where = inputField+" >"+str(midPointGrass)
    
    if Verbose: print where

    goodName = inputField[:-4]

    if Verbose:  print goodName

    goodLyr = "ptBBSS_"+goodName
    
    arcpy.MakeFeatureLayer_management(in_features=ptsBBSS,
                                      out_layer=goodLyr,
                                      where_clause=where)

    # # # 3)  Now let's save it out
    #  
    #  http://desktop.arcgis.com/en/arcmap/10.4/tools/data-management-toolbox/copy-features.htm
    #  CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
    try:
        arcpy.CopyFeatures_management(goodLyr, goodLyr)
    except:
        pass
    return goodLyr
goodlLyr = findGoodBBSS()

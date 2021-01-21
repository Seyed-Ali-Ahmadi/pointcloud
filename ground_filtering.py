import pdal

# This code extracts ground points without any errors.
# It means that the ground modification process is no longer required.
# CONGRATS! ;)

# This piece of code only requires to enter the in/out-put file names.

json = """
{
  "pipeline":[
    "PointCloud.las",
    {
      "type":"filters.smrf",
      "scalar":1.2,
      "slope":0.2,
      "threshold":0.45,
      "window":16.0
    },
    {
      "type":"filters.range",
      "limits":"Classification[2:2]"
    },
    "ground.las"
  ]
}"""
pipeline = pdal.Pipeline(json)
pipeline.validate()
pipeline.execute()


import ee
import json
import os
class LoadRegionMetadata:
    def __init__(self, region):
        if os.path.exists(region):
        

            if region.endswith('.json'):
                with open(region) as f:
                    geometry_file = json.load(f)
                self.area = ee.Geometry.Polygon(
                    geometry_file['features'][0]['geometry']['coordinates'])
            else:

                try:
                    self.area = ee.Geometry.Rectangle(*region)
                except ee.ee_exception.EEException:
                    print("Must Specify either 2 coordinates (lon,lat) like "
                          ":(175.570433, -37.76523, 175.589782,-37.687828) or"
                          "four pairs of coordinates")
        else:
            raise FileNotFoundError("GeoJSON geometry file does not exist")




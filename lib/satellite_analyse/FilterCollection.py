

import ee
from lib.satellite_analyse.collection_mappings import ndvi_landsat, ndvi_sentinel
from lib.satellite_analyse.LoadRegionMetadata import LoadRegionMetadata

# Note that this code has further potential to analyse EVI and NDVI
# fields from the LandSat Collection, which are commented in the code.

class FilterCollection(LoadRegionMetadata):
    def __init__(self, collection, start_date, end_date, cloud_threshold, region_metadata_dir):
        cloud_threshold = max(0, cloud_threshold)

        super(FilterCollection, self).__init__(region_metadata_dir)
        # Inherit attributes from the region metadata class
        self.start_date = ee.Date.fromYMD(*start_date)
        self.end_date = ee.Date.fromYMD(*end_date)

        if 'sentinel' in collection:
            # Filter Collection based on contraints
            self.collection = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(
                self.start_date,self.end_date). \
                filterBounds(self.area).filterMetadata("CLOUDY_PIXEL_PERCENTAGE","less_than",
                                                       cloud_threshold)

            self.collection_ndvi = self.collection.map(ndvi_sentinel)
            print(" number of image: ", self.collection.size().getInfo())

        elif 'landsat7' in collection:
            self.collection = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').filterDate(
                self.start_date,self.end_date). \
                filterBounds(self.area).filterMetadata("CLOUD_COVER", "less_than",
                                                       cloud_threshold)
            self.collection_ndvi = self.collection.map(ndvi_landsat)
            print(" number of image: ", self.collection.size().getInfo())

        elif 'landsat8' in collection:

            self.collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR").filterDate(
                self.start_date,self.end_date). \
                filterBounds(self.area).filterMetadata("CLOUD_COVER","less_than",
                                                       cloud_threshold)
            self.collection_ndvi = self.collection.map(ndvi_landsat)
            print(" number of image: ", self.collection.size().getInfo())
        else:
            raise NameError("No Collection Present, use keywords landsat7, landsat8 or sentinel")


        # elif 'EVI' in collection:
        #     self.collection_ndvi = ee.ImageCollection("LANDSAT/LC08/C01/T1_8DAY_EVI").filterDate(
        #         self.start_date,self.end_date). \
        #         filterBounds(self.area)
        #
        # elif 'NDVI' in collection:
        #     self.collection_ndvi = ee.ImageCollection("LANDSAT/LC08/C01/T1_8DAY_NDVI"). \
        #         filterDate(self.start_date,self.end_date).filterBounds(self.area)



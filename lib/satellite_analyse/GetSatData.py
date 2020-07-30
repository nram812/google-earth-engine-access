import ee
import cv2
from lib.satellite_analyse.FilterCollection import FilterCollection
from lib.satellite_analyse.GetBandsMeta import GetBandsMetaData
from lib.satellite_analyse.grid_and_attribute import grid_arrays, get_array_attr

try:
    ee.Initialize()
except ee.EEException:
    # google login and paste authorisation code is required
    ee.Authenticate()

class GetSatData(GetBandsMetaData, FilterCollection):

    def __init__(self, satellite_name, region_metadata_dir,
                 start_date, end_date, cloud_threshold = 5):
        """
        :param satellite_name: the name of the satellite use
        "sentinel for sentinel2 or landsat8 or landsat7.
        :param region_metadata_dir: the directory of the GeoJSON file
        :param start_date: start date must be in the format year,month ,day
        :param end_date: end date also in the same format as above
        :param cloud_threshold: the cloud fraction threshold for selecting images. Note
        that this appears to be broken for LandSat7 and LandSat8
        """

        GetBandsMetaData.__init__(self, satellite_name)
        FilterCollection.__init__(self, satellite_name, start_date, end_date, cloud_threshold, region_metadata_dir)
        self.bands = ee.List(self.bands_list)
        self.start_date = ee.Date.fromYMD(*start_date)
        self.end_date = ee.Date.fromYMD(*end_date)

    def load_color_image(self, img = "mosaic"):
        if self.collection.size().getInfo() > 0:

            if img == "mosaic":
                img = ee.Image(self.collection.mosaic()).clip(clip_geometry=self.area)
            elif img == "first":
                img = ee.Image(self.collection.first()).clip(clip_geometry=self.area)
            elif img == "median":
                img = ee.Image(self.collection.median()).clip(clip_geometry=self.area)
            else:
                try:    
                    img = img.clip(clip_geometry=self.area)
                except AttributeError:
                    raise KeyError("Wrong Image type or string name used, Image must be an "
                                   "ee.Image() (not a collection) or mosaic, first or median")
                                    
            # Selecting relevant bands for visuals imagery
        
            img_full = img.select(ee.List(["B2", "B3", "B4"]))
            
            latlon = ee.Image.pixelLonLat().addBands(img_full)
            latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(),
                                             geometry=self.area,
                                             maxPixels=1e10,
                                             scale=30)

            # Obtain the numpy arrays of the mosiac
            B = get_array_attr(latlon_new, "B2")
            G = get_array_attr(latlon_new, "B3")
            R = get_array_attr(latlon_new, "B4")
            lats = get_array_attr(latlon_new, "latitude")
            lons = get_array_attr(latlon_new, "longitude")
            im, lons, lats = grid_arrays(lats, lons, [R,G,B])

            #  Rescale the pixel intensities
            im = cv2.convertScaleAbs(im.transpose(1,2,0),
                                     alpha=(255.0/4000))

            return im, lons, lats


    def load_ndvi_image(self, img):
        print('fuck')
        if self.collection_ndvi.size().getInfo() > 0:

            if img == "mosaic":
                img = ee.Image(self.collection_ndvi.mosaic()).clip(clip_geometry=self.area)
            elif img == "median":
                img = ee.Image(self.collection_ndvi.first()).clip(clip_geometry=self.area)
            elif img == "first":
                img = ee.Image(self.collection_ndvi.median()).clip(clip_geometry=self.area)
            else:
                try:
                    img = img.clip(clip_geometry=self.area)
                except AttributeError:
                    raise KeyError("Wrong Image type or string name used, Image must be an "
                                   "ee.Image() (not a collection) or mosaic, first or median")



            img_full = img.select('ndvi')
            latlon = ee.Image.pixelLonLat().addBands(img_full)
            latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(),
                                             geometry=self.area,
                                             maxPixels=1e20,
                                             scale=20)

            lats = get_array_attr(latlon_new, "latitude")
            lons = get_array_attr(latlon_new, "longitude")
            B = get_array_attr(latlon_new, "ndvi")

            return grid_arrays(lats, lons, [B])
        else:
            return None

    def load_sequence_color_images(self):
        """
        Note this analysis only works with LandSat8 and Sentinel 2
        This script retrieves a colour image for every selected image, alongside
        with the latitude and longitude grid.

        There is also an ability to extract the time-series from this signal aswell.

        :return:
        """

        images = [item.get('id') for item in self.collection.getInfo().get('features')]
        times = [pd.to_datetime(image.split('_')[-2], format = '%Y%m%dT%H%M%S') for image in images ]
        # times = [image.strip("COPERNICUS/S2") for image in images ]
        im1 = []
        for image in images:
            print(image)
            img = ee.Image(image)
            im, lons, lats = self.load_color_image(img)
            im1.append(im)
        return im1 , lons, lats

    


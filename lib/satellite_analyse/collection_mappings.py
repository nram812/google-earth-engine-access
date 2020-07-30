
import ee
def ndvi_sentinel(img):
    ndvi = ee.Image(img.normalizedDifference(['B8', 'B4'])).rename(["ndvi"])
    return ndvi
def ndvi_landsat(img):
    ndvi = ee.Image(img.normalizedDifference(['B5', 'B4'])).rename(["ndvi"])
    return ndvi

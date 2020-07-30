
import pytest
import sys
import os
import numpy as np
args = sys.argv[-1]
sys.path.append(args)
os.chdir(args)
from lib.satellite_analyse.GetSatData import GetSatData


def test_sat_data():
    # Note
    with pytest.raises(NameError) as e:

        # BAD satellite data name
        region = r'satellite_data\region_coordinates\polygon_true.json'
        sentinel_object = GetSatData('sent', region, [2020,1,10], [2020,1,19], 5)
        assert str(e) == "NameError"
    with pytest.raises(FileNotFoundError) as e:

        # bad region JSON file (only name error)
        region = r'satellite_data\region_coordinates\polygon_true.json1'
        sentinel_object = GetSatData('sentinel', region, [2020,1,10], [2020,1,19], 5)
        assert str(e) == "FileNotFoundError"
    with pytest.raises(KeyError) as e:

        # Bad image style key word entered
        region = r'satellite_data\region_coordinates\polygon_true.json'
        sentinel_object = GetSatData('sentinel', region, [2020,1,10], [2020,1,19], 5)
        # Wrong key entered
        ndvi, lon, lat = sentinel_object.load_ndvi_image(img = "first1")
        assert str(e) == "KeyError"
    with pytest.raises(KeyError) as e:

        # wrong keyword enetered again
        region = r'satellite_data\region_coordinates\polygon_true.json'
        sentinel_object = GetSatData('sentinel', region, [2020,1,15], [2020,1,19], 5)
        # Wrong key entered
        ndvi, lon, lat = sentinel_object.load_ndvi_image(img = "mosaic")
        assert str(e) == "KeyError"



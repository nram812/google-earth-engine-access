import os
import matplotlib.pyplot as plt
import argparse
import ee
import sys
from scipy.interpolate import griddata
import numpy as np
ee.Initialize()
parser = argparse.ArgumentParser()
parser.add_argument("repo_dir")
args = parser.parse_args()
sys.path.append(args)

# Initialise google earth engine, add this python
# path to import the moudles

try:

    from lib.satellite_analyse.GetSatData import GetSatData
    os.chdir(args)
except FileNotFoundError:
    print("Incorrent Parent/Repository Directoy Selected")
    sys.exit(1)


region = r'satellite_data\region_coordinates\polygon_true.json'


# Note
sentinel_object = GetSatData('sentinel', region, [2020,1,10], [2020,1,19], cloud_threshold= 5 )

# Other datasets that you can use. 

#sentinel_object = GetSatData('landsat8', region, [2020,1,10], [2020,1,19], cloud_threshold= 5 )
#sentinel_object = GetSatData('landsat7', region, [2020,1,10], [2020,1,19], cloud_threshold= 5 )

ndvi, lon, lat = sentinel_object.load_ndvi_image(img = "first")
cs = ax.pcolormesh(lon.T, lat.T, ndvi[0] , zorder =0, cmap = 'viridis')
ax4 = fig.add_axes([0.15,0.03,0.5, 0.02])
cbar = fig.colorbar(cs,cax = ax4, orientation = 'horizontal')
cbar.set_label('NDVI')


# Plotting a colour image
fig, ax = plt.subplots()
ax.imshow(sentinel_object.load_color_image(img = "mosaic")[0])


ax.set_xticklabels([])
ax.set_yticklabels([])


# Resampling_data on the C-DAX path, excluding the end points of the grid

lat_samples = lat.T[:-1,:-1].ravel()
lon_samples = lon.T[:-1,:-1].ravel()
image_flattened = ndvi[0].ravel()
lons_resample, lats_resample =apc_interp[:2]


resample_ndvi = griddata(points = (lon_samples, lat_samples),
             values = image_flattened, xi = (lons_resample, lats_resample))




apc = apc_interp[-1].ravel()
plt.figure()
plt.plot(resample_ndvi.ravel(), apc, 'rx')
plt.xlabel('NDVI')
plt.ylabel("Average Pasture Cover (kg/ha)")

# Ideally we want a relationship between APC and NDVI estimates, there are ambiguities at this stage
# as the grid size is large and zones outside the paddock are also interfering with the results
# Ideally further double check of the data should be done.\



# To observe the metadata from the files use the following command.
print(sentinel_object.band_metadata)



import numpy as np
import ee
from scipy.stats import binned_statistic_2d


# Note it is possible that the statistic in binned_statistic_2d
# should be changed to np.nanmean
def get_array_attr(img, obj):
    return np.array((ee.Array(img.get(obj)).getInfo()))
def grid_arrays(lats, lons, array):
    """

    :param lats: all latitude coordinates shape: (N,)
    :param lons: all longitude coordinates shape: (N,)
    :param array: shape (D,N) where D is dimnesion
    :return: Image shape: (D,n,m) where (n*m) = N
    """
    uniqueLats = np.unique(lats)
    uniqueLons = np.unique(lons)
    image, lat_bins, lon_bins, bincount = binned_statistic_2d(
        x=lats,
        y=lons,
        values=array,
        bins=[uniqueLats,
              uniqueLons],
        statistic='mean')
    mesh_lons, mesh_lats = np.meshgrid(uniqueLons, uniqueLats)
    return image, mesh_lons.T, mesh_lats.T
